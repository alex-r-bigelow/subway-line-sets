import { View } from '../node_modules/uki/dist/uki.esm.js';
import layoutFunctions from '../layouts/allLayouts.js';
import exampleList from '../exampleData/exampleList.js';

class SettingsView extends View {
  setup () {
    this.setupCollapseButton();
    this.setupExamplePicker();
    this.setupUploadButton();
    this.setupLayoutOptions();
    this.setupDownloadButton();
  }
  setupCollapseButton () {
    this.d3el.select('#collapseButton').on('click', () => {
      this.d3el.classed('expanded', !this.d3el.classed('expanded'));
      window.controller.renderAllViews();
    });
  }
  setupExamplePicker () {
    const examplePicker = this.d3el.select('#examplePicker');

    const exampleOptions = examplePicker.selectAll('option')
      .data(['none'].concat(exampleList), d => d);
    exampleOptions.enter().append('option')
      .attr('value', d => d)
      .property('disabled', d => d === 'none')
      .text(d => d === 'none' ? 'Select a dataset' : d);
    const self = this;
    examplePicker.on('change', function () {
      self.d3el.select('#uploadButton').node().value = null;
      window.controller.loadExampleData(this.value);
    });
  }
  setupUploadButton () {
    this.d3el.select('#uploadButton').on('change', function () {
      if (this.files.length > 0) {
        window.controller.loadFileObject(this.files[0]);
      }
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
  setupDownloadButton () {
    this.d3el.select('#downloadButton').on('click', () => {
      window.alert('sorry, not implemented yet');
    });
  }
  draw () {
    this.d3el.select('#examplePicker').node().value = window.data && exampleList.indexOf(window.data.name) !== -1 ? window.data.name : 'none';
    this.d3el.select('#layoutPicker').node().value = window.controller.currentLayout;
  }
}

export default SettingsView;
