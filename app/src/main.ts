/* main.ts: the entry point. Loads the index once, paints the frame, dispatches
 * the route. Phase 1b of notes/APP-SPEC-2026-09-02.md.
 *
 * Runtime requests, all of them: /data/*, /fonts/* (by the stylesheet) and the
 * analyst Worker. Nothing else, ever.
 */
import './styles/tokens.css';
import './styles/app.css';

import { startRouter, setTitle, type Route } from './router';
import { renderFrame, refreshFrameStatus, refreshFrameBack } from './frame';
import { initHistory, noteHere } from './history';
import { primeSearch } from './search';
import { loadIndex, registerClasses } from './data';
import { renderHome } from './pages/home';
import { renderNode } from './pages/node';
import { mapPage } from './pages/map';
import { renderNodeReport, renderThreadReport } from './pages/report';
import { notFound } from './pages/notfound';
import { h, clear } from './dom';
import { mountAnalyst, refreshAnalyst } from './analyst/panel';

const frameHost = document.getElementById('frame') as HTMLElement;
const view = document.getElementById('view') as HTMLElement;
const analystHost = document.getElementById('analyst') as HTMLElement;

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
    case 'node-map': return void mapPage(view, { node: r.id });
    case 'node-hood': return void import('./pages/hood').then((m) => m.renderHood(view, r.id));
    case 'hood': return void import('./pages/hood').then((m) => m.renderHood(view, null));
    case 'map': return void mapPage(view, { cell: r.cell });
    case 'thread': return (await import('./pages/thread')).renderThread(view, r.id);
    case 'thread-map': return void mapPage(view, { thread: r.id });
    case 'timeline': return (await import('./pages/timeline')).renderTimeline(view, r.era, r.scope, r.strand, r.topic);
    case 'patents': return (await import('./pages/patents')).renderPatents(view, r.number, r.sheet);
    case 'evidence': return (await import('./pages/evidence')).renderEvidence(view, r.q);
    case 'report-node': return void renderNodeReport(view, r.id);
    case 'report-thread': return renderThreadReport(view, r.id);
    case 'atlas': return (await import('./pages/atlas')).renderAtlas(view);
    case 'topic': return (await import('./pages/topic')).renderTopic(view, r.id);
    case 'directory': return (await import('./pages/directory')).renderDirectory(view, r.dir, r.q);
    case 'library': return (await import('./pages/library')).renderLibrary(view, r.q);
    case 'source': return (await import('./pages/source')).renderSource(view, r.id);
    case 'questions': return (await import('./pages/questions')).renderQuestions(view);
    case 'question': return (await import('./pages/questions')).renderQuestion(view, r.id);
    case 'connect': return (await import('./pages/connect')).renderConnect(view, r.a, r.b);
    case 'notfound': return notFound(view, r.raw);
  }
}

/* The depth stamp has to be on the entry before the first route is dispatched,
   and its hashchange listener has to run before the router's. */
initHistory();

/* The analyst is painted once and re-chipped per route, so it is mounted before
   the first dispatch and never again. */
mountAnalyst(analystHost);

startRouter(async (r) => {
  window.scrollTo(0, 0);
  await dispatch(r);
  noteHere();
  refreshFrameBack();
  void refreshAnalyst(r);
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
