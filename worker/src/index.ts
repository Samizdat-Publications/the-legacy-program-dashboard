/* The analyst endpoint.
 *
 * WHY THIS EXISTS
 * ---------------
 * The board shipped with the analyst calling api.anthropic.com directly from the
 * browser, with the reader's own key in localStorage. That is correct for a file
 * you double-click and wrong for a URL you send to someone: nobody you share this
 * with has a Console key, so every one of them gets the fifteen scripted branches
 * and the line "no API key configured".
 *
 * This Worker holds the key as a Cloudflare secret and answers on the same origin,
 * so the analyst works for every reader and no reader ever holds a key.
 *
 * THE THING TO BE CAREFUL ABOUT
 * -----------------------------
 * This endpoint spends the owner's tokens and its URL is public. So it does NOT
 * forward what the client asks for. The model, the token ceiling, the effort and
 * the history depth are pinned HERE; the client supplies only the system prompt
 * and the conversation. A proxy that forwards `model` and `max_tokens` from the
 * body is an open account.
 *
 * ADDED 1 SEPTEMBER 2026 AFTER THE AUDIT
 * --------------------------------------
 * 1. Rate limits, in code. Per IP (20 a minute) and across everyone (60 a
 *    minute), as `ratelimits` bindings in wrangler.toml -- the same
 *    infrastructure as a WAF rule, but here where a reader of this file can see
 *    it exists. The global one is the ceiling on what a botnet can spend.
 *
 * 2. The origin. `Access-Control-Allow-Origin: *` let any page on the internet
 *    call this from its visitors' browsers. Only the board's origin and a local
 *    preview get a CORS answer now; anything else is refused by the browser.
 *
 * 3. The system prompt may arrive as an array of text blocks. The board sends
 *    its case index as a block marked cache_control so every turn after the
 *    first reads it from the API's cache; the volatile state follows uncached.
 */
import Anthropic from "@anthropic-ai/sdk";

export interface Env {
  ANTHROPIC_API_KEY: string;
  ANALYST_LIMITER?: RateLimit;
  ANALYST_GLOBAL_LIMITER?: RateLimit;
}

/* Pinned server-side. The client may not raise any of them. */
const MODEL = "claude-opus-5";
/* Thinking tokens count against max_tokens; 16000 is the documented shape for
   adaptive thinking at this effort. */
const MAX_TOKENS = 16_000;
const EFFORT = "high";
const MAX_TURNS = 10;
const MAX_CHARS = 24_000;          // per conversation turn
const MAX_SYSTEM_CHARS = 300_000;  // the whole system prompt, all blocks together

/* Origins allowed to call this from a browser. */
const ALLOWED_ORIGINS = new Set([
  "https://the-program-zxz.pages.dev",
  // the new shell (app/), 2 September 2026: its review project and the Vite
  // dev and preview servers. Pages preview deployments get their own subdomain
  // per branch, so those are matched by suffix below.
  "https://the-program-next.pages.dev",
  "http://127.0.0.1:8899",
  "http://localhost:8899",
  "http://127.0.0.1:4173",
  "http://localhost:4173",
  "http://127.0.0.1:5173",
  "http://localhost:5173",
]);
const ALLOWED_SUFFIXES = [".the-program-next.pages.dev", ".the-program-zxz.pages.dev"];

function cors(req: Request): Record<string, string> {
  const origin = req.headers.get("origin") ?? "";
  if (!ALLOWED_ORIGINS.has(origin) && !ALLOWED_SUFFIXES.some(sfx => origin.endsWith(sfx))) return {};
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    Vary: "Origin",
  };
}

const json = (req: Request, body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...cors(req) },
  });

type Turn = { role: "user" | "assistant"; content: string };

function clean(raw: unknown): Turn[] | null {
  if (!Array.isArray(raw)) return null;
  const out: Turn[] = [];
  for (const m of raw.slice(-MAX_TURNS)) {
    if (!m || typeof m !== "object") return null;
    const { role, content } = m as Record<string, unknown>;
    if (role !== "user" && role !== "assistant") return null;
    if (typeof content !== "string" || !content.trim()) return null;
    out.push({ role, content: content.slice(0, MAX_CHARS) });
  }
  /* The API rejects an empty conversation and one that does not end on the user,
     and both are cheaper to catch here than as a 400 round trip. */
  if (!out.length || out[out.length - 1].role !== "user") return null;
  return out;
}

/* A string, or an array of text blocks. Only `type: "text"`, only an ephemeral
   cache_control, and a ceiling on the total -- the client does not get to
   choose what else goes in a system block. */
function cleanSystem(raw: unknown): Anthropic.TextBlockParam[] | undefined {
  if (typeof raw === "string") {
    return raw.trim() ? [{ type: "text", text: raw.slice(0, MAX_SYSTEM_CHARS) }] : undefined;
  }
  if (!Array.isArray(raw)) return undefined;
  const out: Anthropic.TextBlockParam[] = [];
  let budget = MAX_SYSTEM_CHARS;
  for (const b of raw) {
    if (!b || typeof b !== "object") return undefined;
    const { type, text, cache_control } = b as Record<string, unknown>;
    if (type !== "text" || typeof text !== "string") return undefined;
    const t = text.slice(0, Math.max(0, budget));
    budget -= t.length;
    if (!t) continue;
    const block: Anthropic.TextBlockParam = { type: "text", text: t };
    if (cache_control && typeof cache_control === "object"
        && (cache_control as Record<string, unknown>).type === "ephemeral") {
      block.cache_control = { type: "ephemeral" };
    }
    out.push(block);
  }
  return out.length ? out : undefined;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    if (req.method === "OPTIONS") return new Response(null, { headers: cors(req) });
    const { pathname } = new URL(req.url);

    /* The board asks this before showing the analyst as live, so it can fall back
       to scripted replies rather than failing at the moment someone types. */
    if (pathname === "/api/analyst/health") {
      return json(req, { ok: true, live: !!env.ANTHROPIC_API_KEY, model: MODEL });
    }
    if (pathname !== "/api/analyst") return json(req, { error: "not found" }, 404);
    if (req.method !== "POST") return json(req, { error: "POST only" }, 405);
    if (!env.ANTHROPIC_API_KEY) {
      return json(req, { error: "the analyst is not configured on this deployment" }, 503);
    }

    /* Per-IP, then global. Both bindings are optional in the type so a deployment
       without them still answers; a missing limiter is logged, not fatal. */
    const ip = req.headers.get("cf-connecting-ip") ?? "unknown";
    if (env.ANALYST_LIMITER) {
      const { success } = await env.ANALYST_LIMITER.limit({ key: "analyst:" + ip });
      if (!success) return json(req, { error: "too many requests from this address; try again in a minute" }, 429);
    } else {
      console.warn("ANALYST_LIMITER binding is not configured; no per-IP limit");
    }
    if (env.ANALYST_GLOBAL_LIMITER) {
      const { success } = await env.ANALYST_GLOBAL_LIMITER.limit({ key: "analyst:all" });
      if (!success) return json(req, { error: "the analyst is busy; try again in a minute" }, 429);
    }

    let body: Record<string, unknown>;
    try {
      body = (await req.json()) as Record<string, unknown>;
    } catch {
      return json(req, { error: "body is not JSON" }, 400);
    }

    const messages = clean(body.messages);
    if (!messages) return json(req, { error: "messages is not a usable conversation" }, 400);
    const system = cleanSystem(body.system);

    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
    try {
      const msg = await client.messages.create({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system,
        messages,
        thinking: { type: "adaptive" },
        output_config: { effort: EFFORT },
      });
      /* Return the API's own shape. The board already parses it, and translating
         here would mean two places to keep in step. usage is passed through so a
         reader of the network tab can see the cache working. */
      return json(req, { content: msg.content, stop_reason: msg.stop_reason, usage: msg.usage });
    } catch (e: unknown) {
      const status = (e as { status?: number })?.status ?? 502;
      const message = (e as { message?: string })?.message ?? "upstream error";
      /* 429 is the one the reader can do something about, so it keeps its code. */
      return json(req, { error: message.slice(0, 300) }, status === 429 ? 429 : 502);
    }
  },
};
