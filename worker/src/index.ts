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
 */
import Anthropic from "@anthropic-ai/sdk";

export interface Env {
  ANTHROPIC_API_KEY: string;
}

/* Pinned server-side. The client may not raise any of them. */
const MODEL = "claude-opus-5";
const MAX_TOKENS = 4000;
const EFFORT = "high";
const MAX_TURNS = 10;
const MAX_CHARS = 24_000;

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type",
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...CORS },
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
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    const { pathname } = new URL(req.url);

    /* The board asks this before showing the analyst as live, so it can fall back
       to scripted replies rather than failing at the moment someone types. */
    if (pathname === "/api/analyst/health") {
      return json({ ok: true, live: !!env.ANTHROPIC_API_KEY, model: MODEL });
    }
    if (pathname !== "/api/analyst") return json({ error: "not found" }, 404);
    if (req.method !== "POST") return json({ error: "POST only" }, 405);
    if (!env.ANTHROPIC_API_KEY) {
      return json({ error: "the analyst is not configured on this deployment" }, 503);
    }

    let body: Record<string, unknown>;
    try {
      body = (await req.json()) as Record<string, unknown>;
    } catch {
      return json({ error: "body is not JSON" }, 400);
    }

    const messages = clean(body.messages);
    if (!messages) return json({ error: "messages is not a usable conversation" }, 400);
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
      return json({ content: msg.content, stop_reason: msg.stop_reason });
    } catch (e: unknown) {
      const status = (e as { status?: number })?.status ?? 502;
      const message = (e as { message?: string })?.message ?? "upstream error";
      /* 429 is the one the reader can do something about, so it keeps its code. */
      return json({ error: message.slice(0, 300) }, status === 429 ? 429 : 502);
    }
  },
};
