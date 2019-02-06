/* globals d3 */
import { Model } from './node_modules/uki/dist/uki.esm.js';
import GraphicsView from './views/GraphicsView.js';
import SettingsView from './views/SettingsView.js';
import SetOfSets from './models/SetOfSets.js';
import layoutFunctions from './layouts/allLayouts.js';

class Controller extends Model {
  constructor () {
    super();

    this.currentLayout = 'none';

    this.views = [
      new GraphicsView(d3.select('#GraphicsView')),
      new SettingsView(d3.select('#SettingsView'))
    ];

    this.loadExampleData('slc.csv');
  }
  renderAllViews () {
    for (const view of this.views) {
      view.render();
    }
  }
  async loadExampleData (filename) {
    window.data = this.data = null;
    this.currentLayout = 'none';
    this.renderAllViews();
    const rawString = await d3.text(`exampleData/${filename}`);
    window.data = this.data = SetOfSets.fromCsv(filename, rawString);
    this.renderAllViews();
  }
  async loadFileObject (fileObj) {
    window.data = this.data = null;
    this.currentLayout = 'none';
    this.renderAllViews();
    return new Promise((resolve, reject) => {
      const reader = new window.FileReader();
      reader.onload = event => {
        window.data = this.data = SetOfSets.fromCsv(fileObj.name, event.target.result);
        this.renderAllViews();
        resolve();
      };
      reader.readAsText(fileObj);
    });
  }
  async applyLayout (layoutName) {
    this.currentLayout = layoutName;
    let temp = window.data;
    delete window.data;
    this.renderAllViews();
    temp = await layoutFunctions[this.currentLayout](temp);
    window.data = temp;
    this.renderAllViews();
  }
}

window.controller = new Controller();
