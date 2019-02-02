/* globals d3 */
import { View } from '../node_modules/uki/dist/uki.esm.js';

class SettingsView extends View {
  setup () {
    this.d3el.select('#collapseButton').on('click', () => {
      this.d3el.classed('expanded', !this.d3el.classed('expanded'));
      window.controller.renderAllViews();
    });
  }
  draw () {
    
  }
}

export default SettingsView;
