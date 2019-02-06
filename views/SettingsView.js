import { View } from '../node_modules/uki/dist/uki.esm.js';
import layoutFunctions from '../layouts/allLayouts.js';

class SettingsView extends View {
  setup () {
    this.setupCollapseButton();
    this.setupExamplePicker();
    this.setupLayoutOptions();
  }
  setupCollapseButton () {
    this.d3el.select('#collapseButton').on('click', () => {
      this.d3el.classed('expanded', !this.d3el.classed('expanded'));
      window.controller.renderAllViews();
    });
  }
  setupExamplePicker () {
    this.d3el.select('#examplePicker').on('change', () => {
      window.controller.loadExampleData(this.d3el.select('#examplePicker').node().value);
    });
  }
  setupLayoutOptions () {
    const layoutPicker = this.d3el.select('#layoutPicker');

    const layoutList = [null].concat(Object.keys(layoutFunctions));
    const layoutOptions = layoutPicker.selectAll('option')
      .data(layoutList, d => d);
    layoutOptions.enter().append('option')
      .attr('value', d => d)
      .property('disabled', d => d === null)
      .text(d => d === null ? 'Select a layout' : layoutFunctions[d].interfaceLabel);
    layoutPicker.on('change', async function () {
      let temp = window.data;
      delete window.data;
      window.controller.renderAllViews();
      temp = await layoutFunctions[this.value](temp);
      window.data = temp;
      window.controller.renderAllViews();
    });
  }
  draw () {}
}

export default SettingsView;
