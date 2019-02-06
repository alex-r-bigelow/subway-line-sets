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
    this.d3el.select('#examplePicker').on('change', function () {
      window.controller.loadExampleData(this.value);
    });
  }
  setupLayoutOptions () {
    const layoutPicker = this.d3el.select('#layoutPicker');

    const layoutList = ['none'].concat(Object.keys(layoutFunctions));
    const layoutOptions = layoutPicker.selectAll('option')
      .data(layoutList, d => d);
    layoutOptions.enter().append('option')
      .attr('value', d => d)
      .property('disabled', d => d === 'none')
      .text(d => d === 'none' ? 'Select a layout' : layoutFunctions[d].interfaceLabel);
    layoutPicker.on('change', async function () {
      window.controller.applyLayout(this.value);
    });
  }
  draw () {
    this.d3el.select('#layoutPicker').node().value = window.controller.currentLayout;
  }
}

export default SettingsView;
