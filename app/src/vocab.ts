/* vocab.ts: reader names for the board's twelve edge types, in reading order.
 *
 * The backbone comes first (what the record says a thing is and did), then the
 * assertion layer (who says so, who denies it), then context. The split is
 * measured, not chosen: notes/redesign-2026-09-24/B-GRAPH-STRUCTURE.md section 4.
 *
 * Since redesign phase 3 the table lives in schema/vocab.json, the one vocabulary
 * the pipeline (merge.py, build_app_data.py, verify.py) reads as well. It is
 * imported here at BUILD time, so the page and the pipeline cannot disagree, and
 * build_app_data.py also publishes the same file as /data/vocab.json.
 * app/checks/run.mjs restates these names in C22 rather than importing them.
 */
import vocab from '../../schema/vocab.json';

export type Layer = 'backbone' | 'assertion' | 'context';
export interface EdgeTypeName { id: string; label: string; blurb: string; layer: Layer; }

export const EDGE_TYPES: EdgeTypeName[] = vocab.edgeTypes.map((t) => ({
  id: t.id, label: t.label, blurb: t.blurb, layer: t.layer as Layer,
}));

export const LAYER_HEAD: Record<Layer, string> = vocab.layerHeads;

export const NO_SENTENCE: string = vocab.noSentence;

export function edgeTypeName(id: string): EdgeTypeName {
  return EDGE_TYPES.find((t) => t.id === id) || { id, label: id, blurb: '', layer: 'context' };
}
