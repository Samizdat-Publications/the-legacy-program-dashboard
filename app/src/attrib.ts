/* attrib.ts: which Tier 1 claims record that something was SAID.
 *
 * Tier 1 means "a primary record says so". For most claims the record is the
 * fact. For some it is not: a hearing transcript documents that a witness said a
 * thing under oath, and an office's statement documents that the office said it.
 * Those are Tier 1 as records of speech, and a reader who takes "T1" to mean the
 * thing said is established has been misled (blind critic, round 0, item 2).
 *
 * This file does not move a tier. It decides, from the claim alone, whether a
 * Tier 1 claim is a record of speech, so every surface that prints a claim can
 * say so beside the tier. The rule, in order, first match wins:
 *
 *   said   1. the claim text OPENS with an attribution: Sworn, Under oath,
 *             Testified, In testimony, Stated, States:, Said, Told, According to,
 *             Asked, Answering, Attributed, Elicited, Claimed, Alleged;
 *          2. a named SPEAKER then a speech verb within the first six words
 *             ("Grusch testified", "Navy spokesman Joseph Gradisher stated"),
 *             where the word before the verb is not an article or possessive
 *             ("The stated purpose" is not speech) and the subject is not a
 *             document ("The Charter states" is a record's content, not speech);
 *          3. the SOURCE, URLs aside, is a record of speech: sworn, testimony,
 *             deposition, affidavit, a spokesperson, an opening / written /
 *             prepared / emailed / joint / departmental statement, a statement
 *             for the record, remarks, a press conference, a media roundtable or
 *             engagement; unless the claim text is about the record itself
 *             ("Held 13 November 2024 as a joint hearing", "Listed in ...");
 *          4. the text is a QUOTATION (opens with a quote mark) and the source is
 *             a transcript, hearing, statement or interview;
 *   office 5. the source is the interested party itself: a URL on aaro.mil,
 *             defense.gov or war.gov, or a source string that begins with AARO.
 *             The board caps such claims at Tier 2 unless they are about what the
 *             office said, so a Tier 1 claim here is, by the board's own rule,
 *             the office's own account.
 *
 * app/checks/run.mjs C31 restates this rule in its own words and requires the
 * marked rows on the Grusch page, the evidence table and the report to be
 * exactly the rows the rule picks from the record.
 */

import { h } from './dom';

export type Said = 'said' | 'office' | null;

const OPEN = /^['"‘“]?(?:Sworn\b|Under oath\b|Testif(?:ied|ies|ying)\b|In (?:sworn |his |her |their |written )?testimony\b|Stated\b|States:|Said\b|Says\b|Told\b|Tells\b|According to\b|Asked\b|Answering\b|Attributed\b|Elicited\b|Claimed\b|Claims\b|Alleged\b|Alleges\b)/i;
const SPEAKER = /^(?:[A-Z][\w.'’&()-]*\s){0,4}(?!(?:The|A|An|Its|Their|His|Her|This|That|These|Those)\s)[A-Z][\w.'’&()-]*\s(?:said|says|stated|states|testified|testifies|told|tells|swore|alleged|alleges|claimed|claims|asserted|asserts|declared|declares|responded|replied|answered)\b/;
const DOC_SUBJECT = /\b(?:Report|Paper|Assessment|Memo|Memorandum|Brief|Charter|Act|Volume|Document|Instruction|Directive|Manual|Order|FAQ|JANAP|Condon|NSDD|DIA-\d)/;
const SPEECH_SOURCE = /\b(?:sworn|testimony|testified|deposition|affidavit|spokes(?:man|woman|person)|(?:opening|written|prepared|emailed|joint|DoD|Navy|NASA|Pentagon|federal) statement|statement (?:for the record|to|following|by|attributed)|remarks|press conference(?! photographs)|media roundtable|media engagement)\b/i;
const ABOUT_THE_RECORD = /^(?:Held\b|Official hearing record|The (?:hearing|transcript|document|record|report|letter|memo)\b|Its core|Page \d|Sole witness|Witness of record|Called as|Appeared as|Listed in|Written testimony filed)/i;
const QUOTE_SOURCE = /\b(?:transcript|hearing|statement(?! of work)|interview)\b/i;
const OFFICE_DOMAIN = /(^|\.)(?:aaro\.mil|defense\.gov|war\.gov)$/i;
const OFFICE_SOURCE = /^(?:AARO|All-domain Anomaly Resolution Office)\b/i;

function firstHost(s: string): string {
  const m = s.match(/https?:\/\/([^/?#:\s)\]]+)/i);
  return m ? m[1].toLowerCase() : '';
}

export function saidKind(tier: number, text: string, sourceText: string, url?: string | null): Said {
  if (Number(tier) !== 1) return null;
  const t = text || '';
  const src = sourceText || '';
  const s = src.replace(/https?:\/\/\S+/g, ' ');
  if (OPEN.test(t)) return 'said';
  const m = SPEAKER.exec(t);
  if (m && !DOC_SUBJECT.test(m[0])) return 'said';
  if (!ABOUT_THE_RECORD.test(t) && SPEECH_SOURCE.test(s)) return 'said';
  if (/^['"‘“]/.test(t) && QUOTE_SOURCE.test(s)) return 'said';
  if (OFFICE_DOMAIN.test(firstHost(url || src)) || OFFICE_SOURCE.test(s.trim())) return 'office';
  return null;
}

export const SAID_LABEL: Record<'said' | 'office', string> = {
  said: 'said on the record',
  office: "the office's own account",
};

export const SAID_TITLE: Record<'said' | 'office', string> = {
  said: 'Tier 1 here means it is documented that this was said. It is not a finding that what was said is true.',
  office: "Tier 1 here means it is documented that the office said or published this. The office is an interested party; it is not a finding that what it says is true.",
};

/* The mark itself: one element, the same on every surface, at the label size.
   `data-said` carries the kind so a check can read it without parsing words. */
export function saidMark(kind: Said): HTMLElement | null {
  if (!kind) return null;
  return h('span', { class: 'said-mark', 'data-said': kind, title: SAID_TITLE[kind] }, SAID_LABEL[kind]);
}
