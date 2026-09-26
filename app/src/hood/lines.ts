/* hood/lines.ts: the orthogonal lines of the grouped neighbourhood.
 *
 * One line per family column, from the entity in the centre to the head of the
 * column, drawn only in horizontal and vertical runs through the gutters, so a
 * line never crosses a name. Every name on the page is DOM text; the SVG draws
 * no text at all, so nothing here can be an anonymous mark.
 *
 * The lines move (a dash offset, away from the centre), which is the treatment
 * the owner kept from the old board: motion ONLY on the selected node's own
 * links. The motion stops for a reader who asks for reduced motion (hood.css).
 * The family colours the line: denial red, custody and money amber, the rest
 * cyan.
 */
import { familyColour } from './model';

const NS = 'http://www.w3.org/2000/svg';

export function drawLines(stage: HTMLElement, svg: SVGSVGElement): void {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const centre = stage.querySelector('.gn-centre') as HTMLElement | null;
  if (!centre) return;
  const sr = stage.getBoundingClientRect();
  const W = Math.ceil(stage.scrollWidth), H = Math.ceil(stage.scrollHeight);
  svg.setAttribute('width', String(W));
  svg.setAttribute('height', String(H));
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

  const rel = (el: Element) => {
    const r = el.getBoundingClientRect();
    return { l: r.left - sr.left, t: r.top - sr.top, r: r.right - sr.left, b: r.bottom - sr.top };
  };
  const c = rel(centre);
  const anchor = centre.querySelector('.gn-anchor');
  const y0 = anchor ? (rel(anchor).t + rel(anchor).b) / 2 : c.t + 16;
  const blocks = Array.prototype.slice.call(stage.querySelectorAll('.gn-fam')) as HTMLElement[];
  const left = blocks.filter((b) => rel(b).r <= c.l + 1);
  const right = blocks.filter((b) => rel(b).l >= c.r - 1);
  const leftEdge = left.length ? Math.max(...left.map((b) => rel(b).r)) : 0;
  const rightEdge = right.length ? Math.min(...right.map((b) => rel(b).l)) : 0;

  for (const b of blocks) {
    const br = rel(b);
    const head = b.querySelector('.gn-fhead');
    const hr = head ? rel(head) : br;
    const hy = Math.round((hr.t + hr.b) / 2) + 0.5;
    let d: string;
    if (left.includes(b)) {
      const sx = Math.round((leftEdge + c.l) / 2) + 0.5;
      d = 'M' + c.l + ' ' + y0 + ' H' + sx + ' V' + hy + ' H' + br.r;
    } else if (right.includes(b)) {
      const sx = Math.round((rightEdge + c.r) / 2) + 0.5;
      d = 'M' + c.r + ' ' + y0 + ' H' + sx + ' V' + hy + ' H' + br.l;
    } else {
      /* stacked under the centre (a phone): down the left gutter, then in */
      const sx = Math.round(br.l - 8) + 0.5;
      d = 'M' + sx + ' ' + c.b + ' V' + hy + ' H' + br.l;
    }
    const p = document.createElementNS(NS, 'path');
    const fam = b.getAttribute('data-family') || '';
    p.setAttribute('d', d);
    p.setAttribute('class', 'gn-line');
    p.setAttribute('data-family', fam);
    p.setAttribute('style', 'stroke:' + familyColour(fam));
    svg.appendChild(p);
  }
}
