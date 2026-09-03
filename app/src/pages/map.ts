/* The program map page. Design response 1.4, 2.2, 2.3, 2.4 and 4.
 *
 *   #/map                     at fit, in the mode the viewport allows
 *   #/map?cell=<band>.<era>   that cell expanded (cell mode) or highlighted
 *   #/n/<id>/map              scrolled to that chip, white border, all its edges
 *   #/t/<id>/map              the thread's steps highlighted
 *
 * The renderer is in src/map/: model.ts reads map.json, layout.ts is the label
 * rule, links.ts draws the orthogonal edges, render.ts builds the DOM.
 */
import '../styles/map.css';
import { renderMap, type MapRequest } from '../map/render';

export function mapPage(view: HTMLElement, req: MapRequest): Promise<void> {
  return renderMap(view, req).catch((e: Error) => {
    view.textContent = '';
    const p = document.createElement('section');
    p.className = 'notice';
    const hd = document.createElement('h2');
    hd.textContent = 'The map could not be drawn';
    const msg = document.createElement('p');
    msg.textContent = 'data/map.json could not be read: ' + e.message;
    p.append(hd, msg);
    view.append(p);
  });
}
