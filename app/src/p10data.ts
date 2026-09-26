/* p10data.ts: the data redesign phase 10 adds, and its loaders.
 *
 * Kept apart from data.ts so the phases working beside this one do not collide
 * in one file. Same cache discipline: one fetch per path per page load.
 *
 *   /data/questions.json            the questions, in reading order
 *   /data/questions/<id>.json       one question, every cited id resolved
 *   /data/nodes/<id>.json           now carries `claimsMade` and each claim's `meta`
 */
import type { TopicCite, TopicItem } from './data';

const BASE = import.meta.env.BASE_URL;
const cache = new Map<string, Promise<unknown>>();
function get<T>(path: string): Promise<T> {
  let p = cache.get(path) as Promise<T> | undefined;
  if (!p) {
    p = fetch(BASE + 'data/' + path).then((r) => {
      if (!r.ok) throw new Error(path + ' -> HTTP ' + r.status);
      return r.json() as Promise<T>;
    });
    cache.set(path, p as Promise<unknown>);
  }
  return p;
}

/* who made a claim, when, and by what route (research/_claim_meta.json) */
export interface ClaimMeta {
  claimant: string | null; claimantLabel?: string | null; speaker?: string | null;
  artefactDate: string | null; eventDate: string | null; route: string; via?: string | null;
}
export interface ClaimMade {
  id: string; text: string; tier: number;
  source: { text: string; url: string | null; domain?: string | null };
  node: string; nodeLabel: string;
  artefactDate: string | null; eventDate: string | null; route: string; via: string | null;
  topic: string | null;
}

/* the route a claim reached the record by, in words */
export const ROUTE_WORDS: Record<string, string> = {
  hearing: 'at a hearing', broadcast: 'in a broadcast', interview: 'in an interview', book: 'in a book',
  filing: 'in a filing', press: 'in the press', document: 'in a document',
};

export interface QuestionRow {
  id: string; title: string; order: number; status: string; lead: string | null;
  counts: { answer: number; for: number; against: number; open: number; threads: number };
  threads: string[]; topics: string[];
}
export interface QuestionsFile { generated: string; source: string; questions: QuestionRow[]; }
export interface QuestionThread extends TopicItem { id: string; }
export interface QuestionRecord {
  id: string; title: string; order: number; status: string;
  lead: TopicItem | null; answer: TopicItem[]; for: TopicItem[]; against: TopicItem[];
  open: string[]; threads: QuestionThread[]; topics: string[];
  cites: Record<string, TopicCite>;
}
export const loadQuestions = () => get<QuestionsFile>('questions.json');
export const loadQuestion = (id: string) => get<QuestionRecord>('questions/' + id + '.json');
