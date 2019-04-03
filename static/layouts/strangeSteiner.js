/* globals d3 */

async function strangeSteiner (setOfSets) {
  const newPositions = await (await window.fetch('/strangeSteiner', {
    method: 'POST',
    body: setOfSets.toJSON()
  })).json();
  const rawToScreen = d3.scaleLinear()
    .domain([-1, 1])
    .range([0, 1024]);
  console.log(newPositions);
  for (const [vertexName, position] of Object.entries(newPositions)) {
    position.x = rawToScreen(position.x);
    position.y = rawToScreen(position.y);
    setOfSets.vertices[vertexName].position = position;
  }
  return setOfSets;
}
// This label will show up in the interface
strangeSteiner.interfaceLabel = 'Strange Steiner';

export default strangeSteiner;
