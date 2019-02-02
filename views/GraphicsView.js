/* globals d3 */
import { View } from '../node_modules/uki/dist/uki.esm.js';

class GraphicsView extends View {
  constructor () {
    super(...arguments);
    window.addEventListener('resize', () => {
      this.render();
    });
  }
  setup () {
    this.doc = this.d3el.select('#doc');
    this.overlay = this.d3el.select('#overlay');
    this.spinner = this.d3el.select('#spinner');
  }
  draw () {
    const bounds = this.d3el.node()
      .getBoundingClientRect();
    this.doc.attr('width', bounds.width)
      .attr('height', bounds.height);
    this.overlay.attr('width', bounds.width)
      .attr('height', bounds.height);
    this.spinner.style('display', window.data ? 'none' : null);
  }
}

export default GraphicsView;
