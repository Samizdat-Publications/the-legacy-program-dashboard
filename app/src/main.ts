/* main.ts — the entry point. Loads the index once, paints the frame, dispatches
 * the route. Phase 1b of notes/APP-SPEC-2026-09-02.md.
 *
 * Runtime requests, all of them: /data/*, /fonts/* (by the stylesheet) and the
 * analyst Worker. Nothing else, ever.
 */
import './styles/tokens.css';
import './styles/app.css';

import { startRouter, setTitle, type Route } from './router';
import { renderFrame, refreshFrameStatus } from './frame';
import { primeSearch } from './search';
import { loadIndex, registerClasses } from './data';
import { renderHome } from './pages/home';
import { renderNode } from './pages/node';
import { renderNodeReport, renderThreadReport } from './pages/report';
import { renderPending } from './pages/pending';
import { notFound } from './pages/notfound';
import { h, clear } from './dom';

const frameHost = document.getElementById('frame') as HTMLElement;
const view = document.getElementById('view') as HTMLElement;

let ready: Promise<void> | null = null;
function boot(): Promise<void> {
  if (!ready) {
    ready = loadIndex()
      .then((idx) => { registerClasses(idx.classes); })
      .then(() => primeSearch());
  }
  return ready;
}

async function dispatch(r: Route): Promise<void> {
  renderFrame(frameHost, r);
  refreshFrameStatus();

  try {
    await boot();
  } catch (e) {
    clear(view);
    view.append(h('section', { class: 'notice' },
      h('h2', null, 'The board data is not being served'),
      h('p', null, 'data/index.json could not be read: ' + (e as Error).message),
      h('p', null, 'The generator is tools/build_app_data.py. Until it has run, ' +
        'app/scripts/dev-fixture.mjs writes a development subset.'),
    ));
    setTitle('Data not served');
    return;
  }

  switch (r.kind) {
    case 'home': return void renderHome(view);
    case 'node': return void renderNode(view, r.id);
    case 'node-map': return renderPending(view, 'map', 'Opening at #/n/' + r.id + '/map: the map scrolls to that chip and draws all of its edges.');
    case 'node-hood': return renderPending(view, 'hood', 'Opening at #/hood/' + r.id + ': that node at the centre.');
    case 'hood': return renderPending(view, 'hood', 'With nothing selected the ring carries the fourteen start-here nodes.');
    case 'map': return renderPending(view, 'map', r.cell ? 'Requested cell: ' + r.cell : undefined);
    case 'thread': return renderPending(view, 'thread', 'Requested thread: ' + r.id);
    case 'thread-map': return renderPending(view, 'map', 'The map with the steps of thread ' + r.id + ' highlighted.');
    case 'timeline': return renderPending(view, 'timeline',
      [r.era ? 'era ' + r.era : '', r.scope ? 'scope ' + r.scope : ''].filter(Boolean).join(' · ') || undefined);
    case 'patents': return renderPending(view, 'patents',
      'Requested patent: ' + r.number + (r.sheet ? ', sheet ' + r.sheet : ''));
    case 'evidence': return renderPending(view, 'evidence',
      r.q.toString() ? 'Requested filters: ' + r.q.toString() : undefined);
    case 'report-node': return void renderNodeReport(view, r.id);
    case 'report-thread': return renderThreadReport(view, r.id);
    case 'notfound': return notFound(view, r.raw);
  }
}

startRouter((r) => {
  window.scrollTo(0, 0);
  return dispatch(r);
});

/* `/` focuses the search field, as the Home hint says it does. */
document.addEventListener('keydown', (e) => {
  const ke = e as KeyboardEvent;
  const tag = (document.activeElement && document.activeElement.tagName) || '';
  if (ke.key === '/' && tag !== 'INPUT' && tag !== 'TEXTAREA') {
    const f = document.querySelector('.searchbox input') as HTMLInputElement | null;
    if (f) { ke.preventDefault(); f.focus(); }
  }
});
