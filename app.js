/* globals d3 */
import { Model } from '../node_modules/uki/dist/uki.esm.js';
import GraphicsView from './views/GraphicsView.js';
import SettingsView from './views/SettingsView.js';
import SetOfSets from './models/SetOfSets.js';

class Controller extends Model {
  constructor () {
    super();
    this.loadExampleData('simpsons.csv');

    this.views = [
      new GraphicsView(d3.select('#GraphicsView')),
      new SettingsView(d3.select('#SettingsView'))
    ];
  }
  async loadExampleData (filename) {
    const rawString = await d3.text(`exampleData/${filename}`);
    window.data = this.data = SetOfSets.fromCsv(rawString);
  }
}

window.controller = new Controller();
