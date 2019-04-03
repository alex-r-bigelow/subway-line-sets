import { Model } from '../node_modules/uki/dist/uki.esm.js';

const DEFAULT_SIZE = {
  width: 512,
  height: 512
};

class SetOfSets extends Model {
  constructor (name, hyperedges, vertices) {
    super();
    this.name = name;
    this.hyperedges = hyperedges;
    this.vertices = vertices;
  }
  toJSON () {
    return JSON.stringify({
      name: this.name,
      hyperedges: this.hyperedges,
      vertices: this.vertices
    });
  }
}
SetOfSets.fromCsv = (name, rawString) => {
  const vertices = {};
  const hyperedges = {};

  const rows = rawString.split('\n');

  // Get the headers
  const headers = rows[0].split(',');
  for (const header of headers.slice(1)) {
    hyperedges[header] = {
      name: header,
      fixedOrder: false,
      order: []
    };
  }

  // Parse each row
  for (const row of rows.slice(1)) {
    const cols = row.split(',');
    const vertex = {
      name: cols[0],
      memberships: {},
      position: {
        x: Math.random() * DEFAULT_SIZE.width,
        y: Math.random() * DEFAULT_SIZE.height
      },
      fixed: false
    };
    vertices[cols[0]] = vertex;
    let colIndex = 1;
    for (let memberIndex of cols.slice(1)) {
      memberIndex = parseInt(memberIndex);
      if (memberIndex >= 1) {
        const hyperedgeName = headers[colIndex];
        hyperedges[hyperedgeName].order.push({
          name: vertex.name,
          memberIndex
        });
        vertex.memberships[hyperedgeName] = true;
        if (memberIndex > 1) {
          hyperedges[hyperedgeName].fixedOrder = true;
        }
      }
      colIndex++;
    }
  }

  // At this point, we know whether sets are ordered,
  // so we can sort + flatten their members lists
  for (const hyperedge of Object.values(hyperedges)) {
    hyperedge.order = hyperedge.order
      .sort((a, b) => {
        return a.memberIndex - b.memberIndex;
      }).map(nameWrapper => {
        return nameWrapper.name;
      });
  }

  return new SetOfSets(name, hyperedges, vertices);
};
export default SetOfSets;
