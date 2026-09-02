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
 * TWO MORE THINGS, ADDED 1 SEPTEMBER 2026 AFTER THE AUDIT
 * ------------------------------------------------------
 * 1. A rate limit, in code. Until now the only limit was a dashboard WAF rule
 *    that DEPLOY.md described as "worth adding", which is to say nothing in
 *    version control could prove it existed. The `ANALYST_LIMITER` binding in
 *    wrangler.toml is the same infrastructure as a WAF rate-limiting rule, and it
 *    is here where a reader of this file can see it. 20 calls per minute per IP
 *    is generous for a person and useless to a script.
 *
 * 2. The origin. `Access-Control-Allow-Origin: *` let any page on the internet
 *    call this from its visitors' browsers and spend the account. The board is
 *    served from one origin and the worker is routed on that same origin, so
 *    the only cross-origin caller a browser should ever be is a local preview.
 *    Anything else gets no CORS header, which a browser treats as a refusal.
 *    (curl still gets through -- that is what the rate limit is for.)
 */
import Anthropic from "@anthropic-ai/sdk";

export interface Env {
  ANTHROPIC_API_KEY: string;
  ANALYST_LIMITER?: RateLimit;
}

/* Pinned server-side. The client may not raise any of them. */
const MODEL = "claude-opus-5";
/* Thinking tokens count against max_tokens. At 4000 with effort "high" the model
   could spend the whole budget thinking and return stop_reason "max_tokens" with
   no visible answer; 16000 is the documented shape for this configuration. */
const MAX_TOKENS = 16_000;
const EFFORT = "high";
const MAX_TURNS = 10;
const MAX_CHARS = 24_000;

/* Origins allowed to call this from a browser. The live board, plus a local
   preview of the same file. Add a custom domain here when one exists. */
const ALLOWED_ORIGINS = new Set([
  "https://the-program-zxz.pages.dev",
  "http://127.0.0.1:8899",
  "http://localhost:8899",
]);

function cors(req: Request): Record<string, string> {
  const origin = req.headers.get("origin") ?? "";
  if (!ALLOWED_ORIGINS.has(origin)) return {};
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

    /* Per-IP limit. The binding is optional in the type so a deployment that has
       not configured it still answers; a missing limiter is logged, not fatal. */
    if (env.ANALYST_LIMITER) {
      const ip = req.headers.get("cf-connecting-ip") ?? "unknown";
      const { success } = await env.ANALYST_LIMITER.limit({ key: "analyst:" + ip });
      if (!success) {
        return json(req, { error: "too many requests; try again in a minute" }, 429);
      }
    } else {
      console.warn("ANALYST_LIMITER binding is not configured; no per-IP limit");
    }

    let body: Record<string, unknown>;
    try {
      body = (await req.json()) as Record<string, unknown>;
    } catch {
      return json(req, { error: "body is not JSON" }, 400);
    }

    const messages = clean(body.messages);
    if (!messages) return json(req, { error: "messages is not a usable conversation" }, 400);
    const system = typeof body.system === "string" ? body.system.slice(0, MAX_CHARS) : undefined;

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
         here would mean two places to keep in step. */
      return json(req, { content: msg.content, stop_reason: msg.stop_reason });
    } catch (e: unknown) {
      const status = (e as { status?: number })?.status ?? 502;
      const message = (e as { message?: string })?.message ?? "upstream error";
      /* 429 is the one the reader can do something about, so it keeps its code. */
      return json(req, { error: message.slice(0, 300) }, status === 429 ? 429 : 502);
    }
  },
};
