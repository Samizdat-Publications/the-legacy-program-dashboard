/* vocab.ts: reader names for the board's twelve edge types, in reading order.
 *
 * The backbone comes first (what the record says a thing is and did), then the
 * assertion layer (who says so, who denies it), then context. The split is
 * measured, not chosen: notes/redesign-2026-09-24/B-GRAPH-STRUCTURE.md section 4.
 * app/checks/run.mjs restates these names in C22 rather than importing them.
 * Phase 3 moves this table into schema/vocab.json, read by the pipeline too.
 */
export type Layer = 'backbone' | 'assertion' | 'context';
export interface EdgeTypeName { id: string; label: string; blurb: string; layer: Layer; }

export const EDGE_TYPES: EdgeTypeName[] = [
  { id: 'custody', label: 'Custody', blurb: 'who is said to hold material, or to have handed it on', layer: 'backbone' },
  { id: 'funding', label: 'Money', blurb: 'who paid, contracted or was paid', layer: 'backbone' },
  { id: 'programmatic', label: 'Programme links', blurb: 'what ran, produced, succeeded or absorbed what', layer: 'backbone' },
  { id: 'institutional', label: 'Institutional ties', blurb: 'posts, roles, memberships and parent bodies', layer: 'backbone' },
  { id: 'legislative', label: 'Law and oversight', blurb: 'what created, governs, amended or must report to what', layer: 'backbone' },
  { id: 'research', label: 'Research and authorship', blurb: 'who studied, wrote or co-wrote what', layer: 'backbone' },
  { id: 'investigative', label: 'Investigations', blurb: 'who examined, analysed or looked into what', layer: 'assertion' },
  { id: 'witness-chain', label: 'Testimony', blurb: 'who said what about whom, and how it reached the record', layer: 'assertion' },
  { id: 'behavioral', label: 'Conduct', blurb: 'actions and moves, including career moves and reprisal', layer: 'assertion' },
  { id: 'denial', label: 'Denials', blurb: 'dated, attributable statements that something is not so', layer: 'assertion' },
  { id: 'temporal', label: 'Sequence in time', blurb: 'what followed, answered or was caused by what', layer: 'context' },
  { id: 'geographic', label: 'Place', blurb: 'where something was, happened or was based', layer: 'context' },
];

export const LAYER_HEAD: Record<Layer, string> = {
  backbone: 'What the record says it is and did',
  assertion: 'Who says so, and who denies it',
  context: 'Time and place',
};

export const NO_SENTENCE = 'no sentence recorded for this link';

export function edgeTypeName(id: string): EdgeTypeName {
  return EDGE_TYPES.find((t) => t.id === id) || { id, label: id, blurb: '', layer: 'context' };
}
