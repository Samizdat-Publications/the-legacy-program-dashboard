/* The routes that resolve but whose screens belong to a later phase.
 *
 * These are NOT placeholders in the CLAUDE.md section 2 sense: nothing here
 * asserts a source, a figure or a quotation. The route resolves, the page says
 * which phase builds it and which section of the Design response specifies it,
 * and it offers the routes that do work.
 */
import { h, clear } from '../dom';
import { setTitle } from '../router';

interface Pending { title: string; phase: string; design: string; note: string; }

const PAGES: Record<string, Pending> = {
  map: {
    title: 'The program map',
    phase: 'phase 2',
    design: 'Design response 1.4, 2.2, 2.3 and 4',
    note: 'Label mode and cell mode, 7 bands by 5 eras, chips fitted to their text.',
  },
  hood: {
    title: 'The neighbourhood',
    phase: 'phase 2',
    design: 'Design response 1.5',
    note: 'The selected node at the centre, hop 1 on a ring, hop 2 in two outer columns.',
  },
  thread: {
    title: 'Threads',
    phase: 'phase 3',
    design: 'Design response 1.6, and research/threads.json from phase 1c',
    note: 'Eight threads, each step joined to the last by an edge the board already carries.',
  },
  timeline: {
    title: 'The timeline',
    phase: 'phase 3',
    design: 'Design response 1.7',
    note: 'Four strand lanes across five era columns, the open era packed by year.',
  },
  patents: {
    title: 'Patents',
    phase: 'phase 4',
    design: 'Design response 1.8',
    note: 'Five patents, their drawing sheets and the file-wrapper prosecution timeline.',
  },
  evidence: {
    title: 'The evidence explorer',
    phase: 'phase 4',
    design: 'Design response 1.9',
    note: 'Every claim, filterable by tier, class, cluster, source domain, denied and open.',
  },
};

const WORKING: [string, string][] = [
  ['#/', 'Home'],
  ['#/n/aawsap', 'A node page'],
  ['#/report/n/aawsap', 'A node report'],
];

export function renderPending(view: HTMLElement, key: string, detail?: string): void {
  const p = PAGES[key];
  setTitle(p ? p.title : 'Not built yet');
  clear(view);
  const box = h('section', { class: 'notice' });
  box.append(h('h2', null, p ? p.title : key));
  box.append(h('p', null,
    'This route resolves and is specified, and its screen is built in ' +
    (p ? p.phase : 'a later phase') + '. ' + (p ? p.design : '') + '.'));
  if (p) box.append(h('p', null, p.note));
  if (detail) box.append(h('p', { class: 'cyan' }, detail));
  box.append(h('p', null, 'Built and working now:'));
  const ul = h('ul');
  for (const [href, label] of WORKING) {
    ul.append(h('li', null, h('a', { href }, href), ' — ' + label));
  }
  box.append(ul);
  view.append(box);
}
