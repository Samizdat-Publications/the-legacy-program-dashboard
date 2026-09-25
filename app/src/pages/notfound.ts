/* The not-found page. It names the route it was given, and lists the scheme, so a
 * broken link tells the reader what was asked for rather than blanking. */
import { h, clear } from '../dom';
import { setTitle } from '../router';

const SCHEME: [string, string][] = [
  ['#/', 'home'],
  ['#/n/<id>', 'node page'],
  ['#/n/<id>/map', 'the map, centred on that node'],
  ['#/n/<id>/hood', 'its neighbourhood (also #/hood/<id>)'],
  ['#/hood', 'the neighbourhood with nothing selected'],
  ['#/map', 'the program map (?cell=<band>.<era>)'],
  ['#/t/<id>', 'a thread (#/t/<id>/map for its steps on the map)'],
  ['#/timeline', 'the timeline (?era= ?scope=n:<id>|t:<id>)'],
  ['#/patents/<number>', 'a patent (?sheet=<k>)'],
  ['#/evidence', 'the evidence explorer (?tier= &cls= &cluster= &domain= &denied=1 &open=1)'],
  ['#/report/n/<id>', 'a node report (#/report/t/<id> for a thread)'],
];

export function notFound(view: HTMLElement, raw: string, why?: string): void {
  setTitle('Route not found');
  clear(view);
  const box = h('section', { class: 'notice' });
  box.append(h('h2', null, 'No such route: ', h('span', { class: 'red' }, raw)));
  if (why) box.append(h('p', null, why));
  box.append(h('p', null, 'The scheme this terminal answers on:'));
  const ul = h('ul');
  for (const [r, d] of SCHEME) {
    ul.append(h('li', null, h('code', { class: 'cyan' }, r), ': ' + d));
  }
  box.append(ul);
  box.append(h('p', { style: 'margin-top:10px' }, h('a', { href: '#/' }, 'Back to Home')));
  view.append(box);
}
