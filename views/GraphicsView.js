/* globals d3 */
import { View } from '../node_modules/uki/dist/uki.esm.js';

class GraphicsView extends View {
  setup () {
    this.doc = this.d3el.select('#doc');
    this.overlay = this.d3el.select('#overlay');
    this.emptyState = this.d3el.select('#emptyState');
  }
  draw () {

  }
}

export default GraphicsView;
