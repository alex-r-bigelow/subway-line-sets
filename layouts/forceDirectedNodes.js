/* globals d3 */

/*
  This is a naive layout approach, using d3's force-directed
  layout algorithm to position nodes independently, with edges
  between adjacent nodes in a path (this doesn't attempt to
  re-order paths)
*/

async function forceDirectedNodes (setOfSets) {
  // Convert the nodes to the format that D3 expects
  const nodes = Object.values(setOfSets.elements).map(element => {
    const d3Node = {
      name: element.name,
      x: element.position.x,
      y: element.position.y
    };
    if (d3Node.fixed) {
      d3Node.fx = d3Node.x;
      d3Node.fy = d3Node.y;
    }
    return d3Node;
  });

  // Create a lookup into the list of nodes
  const nodeLookup = {};
  nodes.forEach((node, index) => {
    nodeLookup[node.name] = index;
  });

  // D3 also expects links as an array
  const links = [];

  // Connect nodes to their adjacent neighbors in each ordered set
  for (const setObj of Object.values(setOfSets.sets)) {
    for (const elementName of setObj.members) {
      links.push({
        source: nodeLookup[elementName],
        target: nodeLookup[elementName]
      });
    }
  }

  // Initialize the simulation
  const simulation = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody().strength(-80))
    .force('link', d3.forceLink(links).distance(30).strength(1).iterations(10))
    .force('x', d3.forceX())
    .force('y', d3.forceY())
    .stop();

  // Running the simulation takes a while; we use a Promise + timeout to make
  // sure we don't lock up the interface while we're computing things
  return new Promise((resolve, reject) => {
    d3.timeout(() => {
      // See https://github.com/d3/d3-force/blob/master/README.md#simulation_tick
      for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
        simulation.tick();
      }

      // Copy the new positions back to the original elements
      for (const node of nodes) {
        setOfSets.elements[node.name].x = node.x;
        setOfSets.elements[node.name].y = node.y;
      }

      // Signal that we're done
      resolve(setOfSets);
    });
  });
}
// This label will show up in the interface
forceDirectedNodes.interfaceLabel = 'Naive force-directed layout';

export default forceDirectedNodes;
