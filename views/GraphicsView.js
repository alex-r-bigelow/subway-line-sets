/* globals d3 */
import { View } from '../node_modules/uki/dist/uki.esm.js';

const DEFAULT_NODE_RADIUS = 5;

class GraphicsView extends View {
  constructor () {
    super(...arguments);
    window.addEventListener('resize', () => {
      this.render();
    });
  }
  setup () {
    this.doc = this.d3el.select('#doc');
    this.currentZoom = d3.zoomTransform(this.doc.node());
    const zoom = d3.zoom()
      .scaleExtent([1 / 4, 4])
      .on('zoom', () => {
        this.currentZoom = d3.event.transform;
        this.doc.selectAll(':scope > g')
          .attr('transform', this.currentZoom);
      });
    this.doc.call(zoom);
    this.spinner = this.d3el.select('#spinner');
  }
  draw () {
    const bounds = this.d3el.node()
      .getBoundingClientRect();
    this.doc.attr('width', bounds.width)
      .attr('height', bounds.height);

    if (!window.data) {
      this.spinner.style('display', null);
      this.doc.style('opacity', 0.5);
    } else {
      this.doc.style('opacity', null);
      this.spinner.style('display', 'none');

      this.drawLinkLayer();
      this.drawNodeLayer();
      this.drawOverlay();
    }
  }
  drawLinkLayer () {
    let linkLayer = this.doc.select('#linkLayer');

    let links = linkLayer.selectAll('.link')
      .data(d3.entries(window.data.sets), d => d.key);
    links.exit().remove();
    const linksEnter = links.enter().append('g')
      .classed('link', true);
    links = links.merge(linksEnter);

    linksEnter.append('path');
    links.select('path')
      .attr('fill', 'none')
      .attr('stroke', 'black')
      .attr('stroke-width', '3px')
      .attr('d', d => {
        return this.computePath(d.value);
      });
  }
  drawNodeLayer () {
    let nodeLayer = this.doc.select('#nodeLayer');

    let nodes = nodeLayer.selectAll('.node')
      .data(d3.entries(window.data.elements), d => d.key);
    nodes.exit().remove();
    const nodesEnter = nodes.enter().append('g')
      .classed('node', true);
    nodes = nodes.merge(nodesEnter);

    nodesEnter.append('circle');
    nodesEnter.append('text');

    nodes.attr('transform', d => {
      return `translate(${d.value.position.x},${d.value.position.y})`;
    });
    nodes.select('circle')
      .attr('r', DEFAULT_NODE_RADIUS)
      .attr('fill', 'white')
      .attr('stroke', 'black')
      .attr('stroke-width', '1px');
    nodes.select('text')
      .text(d => d.key)
      .attr('x', 2 * DEFAULT_NODE_RADIUS);
  }
  drawOverlay () {

  }
  computePath (setObj) {
    let result = 'M';
    for (const elementName of setObj.members) {
      if (result.length > 1) {
        result += 'L';
      }
      const elementObj = window.data.elements[elementName];
      result += `${elementObj.position.x},${elementObj.position.y}`;
    }
    return result;
  }
}

export default GraphicsView;
