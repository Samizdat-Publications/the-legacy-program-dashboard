/* analyst/state.ts: the CURRENT STATE block, one per route kind.
 *
 * Decision 4 of notes/ANALYST-PLAN-2026-09-03.md: the block that says what is on
 * screen has to be route aware, or a chip offered on the timeline page is a chip
 * the model cannot answer from what it was sent.
 *
 * It is built out of the SAME tools the model can call, so there is one
 * implementation of "what is in this cell" rather than two that drift. What this
 * block buys over letting the model call the tool itself is one round trip on
 * the commonest question, the one about the thing the reader is looking at.
 *
 * This block is sent second and UNCACHED, because it changes on every route. The
 * case index block before it must stay byte-stable; nothing here may leak into it.
 */
import { loadIndex, loadTopic } from '../data';
import { runTool } from './tools';
import type { Route } from '../router';

const FOCUS_CAP = 60000;

function cap(s: string): string {
  return s.length > FOCUS_CAP ? s.slice(0, FOCUS_CAP) + '\n[state truncated at ' + FOCUS_CAP + ' characters]' : s;
}

/* The id the route is about, for the routes that are about one. */
export function routeNode(r: Route): string | null {
  switch (r.kind) {
    case 'node': case 'node-map': case 'node-hood': case 'report-node': return r.id;
    default: return null;
  }
}

async function topTen(): Promise<string> {
  return await runTool('nodes', { sort: 'degree', limit: 10 });
}

export async function caseState(r: Route): Promise<string> {
  const head = 'CURRENT STATE. The reader is on route ' + (location.hash || '#/') +
    ' (' + r.kind + '). What follows is what is on their screen, sent so you do not have to ' +
    'fetch it. Everything else on the board is behind the tools.\n\n';

  const body = await build(r).catch((e: Error) =>
    'The screen state could not be assembled (' + e.message + '). Use the tools instead.');
  return cap(head + body);
}

async function build(r: Route): Promise<string> {
  switch (r.kind) {
    case 'node':
    case 'report-node':
      return 'NODE IN VIEW, in full.\n' + await runTool('node', { ids: [r.id] });

    case 'node-map':
      return 'MAP, centred on one node. That node in full:\n' + await runTool('node', { ids: [r.id] });

    case 'node-hood':
      return 'NEIGHBOURHOOD of one node. Its ring is its sourced edges:\n' +
        await runTool('node', { ids: [r.id], sections: ['dossier', 'edges'], max_edges: 80 });

    case 'hood':
      return 'NEIGHBOURHOOD page with nothing selected. It opens on the start-here flags.\n' +
        await runTool('overview', {});

    case 'map': {
      if (r.cell) {
        return 'PROGRAM MAP with the cell ' + r.cell + ' open. Its members:\n' +
          await runTool('map', { cell: r.cell });
      }
      return 'PROGRAM MAP at fit, no cell open. The grid:\n' + await runTool('map', {});
    }

    case 'thread':
    case 'thread-map':
    case 'report-thread':
      return 'THREAD IN VIEW, every step and the edge that joins it to the one before:\n' +
        await runTool('thread', { id: r.id });

    case 'timeline': {
      const parts: string[] = [];
      if (r.era) {
        parts.push('TIMELINE, filtered to era ' + r.era + '. Its events by year:');
        parts.push(await runTool('timeline', { era: r.era, group_by: 'year' }));
        parts.push('');
        parts.push('The earliest 60 of them:');
        parts.push(await runTool('timeline', { era: r.era, limit: 60 }));
      } else if (r.scope && r.scope.startsWith('n:')) {
        const id = r.scope.slice(2);
        parts.push('TIMELINE, scoped to node ' + id + ':');
        parts.push(await runTool('timeline', { node: id, limit: 80 }));
      } else {
        parts.push('TIMELINE, whole, by decade:');
        parts.push(await runTool('timeline', { group_by: 'decade' }));
        parts.push('');
        parts.push('And by strand:');
        parts.push(await runTool('timeline', { group_by: 'strand' }));
      }
      return parts.join('\n');
    }

    case 'patents':
      return 'PATENT IN VIEW:\n' + await runTool('patent', { number: r.number });

    case 'evidence': {
      const f: Record<string, unknown> = {};
      const on: string[] = [];
      const tier = r.q.get('tier'), cls = r.q.get('cls'), cluster = r.q.get('cluster');
      const domain = r.q.get('domain'), denied = r.q.get('denied'), open = r.q.get('open');
      if (tier) { f.tier = Number(tier); on.push('tier=' + tier); }
      if (cls) { f.cls = cls; on.push('cls=' + cls); }
      if (cluster) { f.cluster = cluster; on.push('cluster=' + cluster); }
      if (domain && domain !== 'none') { f.source_contains = domain; on.push('domain=' + domain); }
      if (denied) { f.denied = denied === '1'; on.push('denied=' + denied); }
      if (open) { f.open = open === '1'; on.push('open=' + open); }
      const head = on.length
        ? 'EVIDENCE table, filtered: ' + on.join(' · ') + '.\n'
        : 'EVIDENCE table, no filter on. Every claim on the board.\n';
      return head + await runTool('claims', { ...f, group_by: 'tier' }) + '\n\n' +
        'The strongest 30 of them:\n' + await runTool('claims', { ...f, limit: 30 });
    }

    case 'home':
      return 'HOME. Nothing is open. The board in summary:\n' + await runTool('overview', {});

    case 'atlas':
      return 'THE ATLAS: every topic of the board by section and era. The board in summary:\n' +
        await runTool('overview', {});

    case 'topic':
      return 'TOPIC IN VIEW, as its page shows it:\n' + await topicState(r.id);

    case 'directory':
      return 'DIRECTORY of ' + r.dir + (r.q.toString() ? ', filtered by ' + r.q.toString() : '') +
        ': a table of every node of that class. The board in summary:\n' + await runTool('overview', {});

    case 'notfound':
      return 'A route that does not resolve (' + r.raw + '). Nothing is open. ' +
        'The ten most connected nodes:\n' + await topTen();
  }
}

/* A topic page's state, from its own file: the tools do not reach topics until
   phase 12, so the reader's screen is sent as it is. */
async function topicState(id: string): Promise<string> {
  const t = await loadTopic(id);
  const out: string[] = [t.title + ' (' + t.kind + ', section ' + t.section + ')'];
  if (t.researchGap) out.push('RESEARCH GAP: ' + String(t.researchGap));
  if (t.lead) out.push('Lead: ' + t.lead.text);
  const block = (name: string, items: { text: string; cite: string[] }[]) => {
    if (!items.length) return;
    out.push('', name + ':');
    for (const it of items) {
      out.push('- ' + it.text + ' [' + it.cite.map((c) => {
        const x = t.cites[c];
        return c + (x ? ' T' + x.tier : '');
      }).join(', ') + ']');
    }
  };
  block('Summary', t.summary);
  block('What the record shows', t.record);
  block('What is claimed', t.claimed);
  block('What is contested', t.contested);
  out.push('', 'Members: ' + t.members.map((m) => m.id + ' (' + m.role + ')').join(', '));
  if (t.questions.length) out.push('', 'Open questions:', ...t.questions.map((q) => '- ' + q));
  return out.join('\n');
}

/* Used by the panel's health line, so a reader can see the analyst knows where
   they are without opening the network tab. */
export async function stateSummary(r: Route): Promise<string> {
  const id = routeNode(r);
  if (id) {
    const idx = await loadIndex().catch(() => null);
    const n = idx && idx.nodes.find((x) => x.id === id);
    return n ? 'reading ' + (n.short || n.label) : 'reading ' + id;
  }
  switch (r.kind) {
    case 'map': return r.cell ? 'reading map cell ' + r.cell : 'reading the program map';
    case 'thread': case 'thread-map': case 'report-thread': return 'reading the ' + r.id + ' thread';
    case 'timeline': return r.era ? 'reading timeline era ' + r.era : 'reading the timeline';
    case 'patents': return 'reading patent ' + r.number;
    case 'evidence': return 'reading the evidence table';
    case 'hood': return 'reading the neighbourhood';
    case 'atlas': return 'reading the Atlas';
    case 'topic': return 'reading the topic ' + r.id;
    case 'directory': return 'reading the ' + r.dir + ' directory';
    default: return 'reading the board';
  }
}
