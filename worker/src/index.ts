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
 *
 * CHANGED 11 SEPTEMBER 2026: TOOLS
 * --------------------------------
 * The analyst can now read the whole board rather than only what is on the
 * reader's screen, and it does that by calling tools. The tools do NOT run
 * here. They run in the reader's browser, against the same /data files the
 * pages read (app/src/analyst/tools.ts), so this Worker still holds no copy of
 * the board and still executes nothing on anyone's behalf.
 *
 * What that costs this file is three things:
 *
 * 1. `messages` content is no longer only a string. A tool exchange is an
 *    assistant turn carrying `thinking` and `tool_use` blocks and a user turn
 *    carrying `tool_result` blocks, and the API requires the thinking blocks
 *    back with their signatures INTACT. So blocks of a known type are passed
 *    through untouched; only text and tool_result strings are capped, and a
 *    thinking block is never rewritten.
 *
 * 2. `tools` is read from the body, but the NAMES are pinned here. A caller
 *    cannot add a tool, so this endpoint stays a board endpoint rather than a
 *    general agent proxy. The descriptions arrive from the page because that is
 *    where the implementations are, and one file owning both is one file that
 *    cannot drift. TOOLS_VERSION is the handshake: the page refuses to ask a
 *    question if the two builds disagree.
 *
 * 3. MAX_TURNS had to rise. One question is now many round trips, two messages
 *    each. The per-IP and global rate limits are unchanged and are still the
 *    ceiling on spend, so a question costing more round trips costs more of
 *    one caller's allowance rather than more of everyone's.
 *
 * AND: BRING YOUR OWN KEY. A caller may send `x-analyst-key`. If they do, that
 * key is used instead of the owner's secret and the rate limits do not apply,
 * because they are spending their own money. The model, the effort and the
 * ceilings stay pinned either way. The key is never logged and never stored.
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
/* A tool loop is two messages a round, so this is round trips times two plus
   the reader's own turns. The page trims its wire history to 40. */
const MAX_TURNS = 60;
const MAX_CHARS = 40_000;          // per text or tool_result block
const MAX_SYSTEM_CHARS = 300_000;  // the whole system prompt, all blocks together
const MAX_MESSAGE_CHARS = 1_200_000; // the whole conversation, serialised
const MAX_TOOL_CHARS = 80_000;     // the whole tool catalogue, serialised

/* The tool names this endpoint will pass to the model. The implementations are
   in app/src/analyst/tools.ts and run in the reader's browser; this list exists
   so a caller cannot turn the endpoint into a general agent proxy by defining
   tools of their own. Both files carry TOOLS_VERSION and the page compares them
   against /api/analyst/health before it asks anything. */
const TOOLS_VERSION = "2026-09-11.1";
const TOOL_NAMES = new Set([
  "overview", "find", "nodes", "node", "claims", "timeline",
  "edges", "path", "thread", "patent", "foia", "map",
]);

/* Content block types this endpoint will relay, by who sends them. Anything
   else is refused rather than forwarded. */
const ASSISTANT_BLOCKS = new Set(["text", "thinking", "redacted_thinking", "tool_use"]);
const USER_BLOCKS = new Set(["text", "tool_result"]);

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
/* Pages gives every preview branch its own subdomain, so those are matched by
   suffix. A CUSTOM DOMAIN goes in ALLOWED_ORIGINS above, as a full origin with
   its scheme and no trailing slash, and the Worker must be redeployed before
   the new address will get an answer. Nothing else needs changing. */
const ALLOWED_SUFFIXES = [".the-program-next.pages.dev", ".the-program-zxz.pages.dev"];

function cors(req: Request): Record<string, string> {
  const origin = req.headers.get("origin") ?? "";
  if (!ALLOWED_ORIGINS.has(origin) && !ALLOWED_SUFFIXES.some(sfx => origin.endsWith(sfx))) return {};
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, x-analyst-key",
    Vary: "Origin",
  };
}

const json = (req: Request, body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...cors(req) },
  });

type Turn = Anthropic.MessageParam;

/* One content block. A block whose type this endpoint does not relay makes the
   whole conversation unusable, which is the right answer: half a tool exchange
   is a 400 from the API anyway, and a silent drop would be one of those.

   A thinking block is returned UNTOUCHED. Its signature covers its text, so
   capping it would invalidate it and the API would reject the turn. */
function cleanBlock(b: unknown, allowed: Set<string>): unknown | null {
  if (!b || typeof b !== "object") return null;
  const o = b as Record<string, unknown>;
  const type = o.type;
  if (typeof type !== "string" || !allowed.has(type)) return null;

  if (type === "thinking" || type === "redacted_thinking") return o;

  if (type === "text") {
    if (typeof o.text !== "string") return null;
    return { ...o, text: o.text.slice(0, MAX_CHARS) };
  }
  if (type === "tool_use") {
    if (typeof o.id !== "string" || typeof o.name !== "string") return null;
    if (!TOOL_NAMES.has(o.name)) return null;
    return o;
  }
  if (type === "tool_result") {
    if (typeof o.tool_use_id !== "string") return null;
    const c = o.content;
    if (typeof c === "string") return { ...o, content: c.slice(0, MAX_CHARS) };
    if (Array.isArray(c)) {
      const inner = c.map((x) => cleanBlock(x, new Set(["text"]))).filter(Boolean);
      return inner.length ? { ...o, content: inner } : null;
    }
    return null;
  }
  return null;
}

function clean(raw: unknown): Turn[] | null {
  if (!Array.isArray(raw)) return null;
  let slice = raw.slice(-MAX_TURNS);
  /* Slicing can orphan a tool_result whose tool_use is now gone, so drop from
     the front until the first message is a plain question again. */
  while (slice.length) {
    const m = slice[0] as Record<string, unknown> | null;
    if (m && m.role === "user" && typeof m.content === "string") break;
    slice = slice.slice(1);
  }

  const out: Turn[] = [];
  for (const m of slice) {
    if (!m || typeof m !== "object") return null;
    const { role, content } = m as Record<string, unknown>;
    if (role !== "user" && role !== "assistant") return null;

    if (typeof content === "string") {
      if (!content.trim()) return null;
      out.push({ role, content: content.slice(0, MAX_CHARS) });
      continue;
    }
    if (!Array.isArray(content) || !content.length) return null;
    const allowed = role === "assistant" ? ASSISTANT_BLOCKS : USER_BLOCKS;
    const blocks: unknown[] = [];
    for (const b of content) {
      const ok = cleanBlock(b, allowed);
      if (!ok) return null;
      blocks.push(ok);
    }
    out.push({ role, content: blocks as Anthropic.ContentBlockParam[] });
  }
  /* The API rejects an empty conversation and one that does not end on the user,
     and both are cheaper to catch here than as a 400 round trip. */
  if (!out.length || out[out.length - 1].role !== "user") return null;
  if (JSON.stringify(out).length > MAX_MESSAGE_CHARS) return null;
  return out;
}

/* The tool catalogue. The names are pinned above; everything else comes from
   the page, because the page is what runs them. */
function cleanTools(raw: unknown): Anthropic.Tool[] | undefined {
  if (raw == null) return undefined;
  if (!Array.isArray(raw) || !raw.length) return undefined;
  if (JSON.stringify(raw).length > MAX_TOOL_CHARS) return undefined;
  const seen = new Set<string>();
  const out: Anthropic.Tool[] = [];
  for (const t of raw) {
    if (!t || typeof t !== "object") return undefined;
    const { name, description, input_schema } = t as Record<string, unknown>;
    if (typeof name !== "string" || !TOOL_NAMES.has(name) || seen.has(name)) return undefined;
    if (typeof description !== "string" || !description.trim()) return undefined;
    if (!input_schema || typeof input_schema !== "object") return undefined;
    if ((input_schema as Record<string, unknown>).type !== "object") return undefined;
    seen.add(name);
    out.push({ name, description, input_schema } as Anthropic.Tool);
  }
  return out.length ? out : undefined;
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
      /* The board asks for the one hour TTL on its case index: a reader who
         wanders between pages for half an hour otherwise pays the full price
         for it again every five minutes, and with a tool loop the prefix is
         re-sent on every round trip rather than once a question. */
      const ttl = (cache_control as Record<string, unknown>).ttl;
      block.cache_control = ttl === "1h" || ttl === "5m"
        ? { type: "ephemeral", ttl: ttl as "1h" | "5m" }
        : { type: "ephemeral" };
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
      /* `tools` is the handshake: the page will not ask a question if its own
         TOOLS_VERSION differs, because the tools run there and a name this
         endpoint has never heard of would come back as a dead answer. */
      return json(req, {
        ok: true, live: !!env.ANTHROPIC_API_KEY, model: MODEL,
        tools: TOOLS_VERSION, toolNames: [...TOOL_NAMES], byok: true,
      });
    }
    if (pathname !== "/api/analyst") return json(req, { error: "not found" }, 404);
    if (req.method !== "POST") return json(req, { error: "POST only" }, 405);

    /* Bring your own key. A caller spending their own money is not rate limited
       here, because the limits exist to cap the OWNER's spend. Never logged. */
    const byok = (req.headers.get("x-analyst-key") ?? "").trim();
    const apiKey = byok || env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return json(req, { error: "the analyst is not configured on this deployment" }, 503);
    }

    /* Per-IP, then global. Both bindings are optional in the type so a deployment
       without them still answers; a missing limiter is logged, not fatal. */
    if (!byok) {
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
    const tools = cleanTools(body.tools);
    if (body.tools != null && !tools) {
      return json(req, {
        error: "tools must be a subset of this endpoint's own: " + [...TOOL_NAMES].join(", "),
      }, 400);
    }

    const client = new Anthropic({ apiKey });
    try {
      const msg = await client.messages.create({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system,
        messages,
        ...(tools ? { tools } : {}),
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
