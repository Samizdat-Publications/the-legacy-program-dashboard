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

/* ---- the relationship families (redesign phase 7) --------------------------
   Families replace the layers as the grouping on the page. The family is the
   reliable unit of the classification (notes/plans/P7-classification-record.md);
   a predicate's own label shows only where its confidence is high, and the
   generator has already put the right words in each connection's `verb`. The
   families are read from schema/vocab.json; check C22 restates them. */
export interface FamilyName { id: string; label: string; blurb: string; phrase: string; }

export const FAMILIES: FamilyName[] = vocab.predicateFamilies.map((f) => ({
  id: f.id, label: f.label, blurb: f.blurb, phrase: f.phrase,
}));

export function familyName(id: string | null | undefined): FamilyName {
  return FAMILIES.find((f) => f.id === id) || { id: id || 'other', label: 'Other links', blurb: '', phrase: 'is connected to' };
}

/* the reading order of predicates inside a family: the vocabulary's own order */
export const PREDICATE_ORDER: string[] = vocab.predicates.map((p) => p.id);

/* each predicate's two labels, for reading a link from the far end (the ring) */
export interface PredicateName { id: string; family: string; forward: string; inverse: string; symmetric: boolean; }
export const PREDICATES: Map<string, PredicateName> = new Map(vocab.predicates.map((p) => [p.id, {
  id: p.id, family: p.family, forward: p.forward, inverse: p.inverse, symmetric: !!(p as { symmetric?: boolean }).symmetric,
}]));
