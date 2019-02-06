import { Model } from '../../node_modules/uki/dist/uki.esm.js';

const DEFAULT_SIZE = {
  width: 512,
  height: 512
};

class SetOfSets extends Model {
  constructor (name, sets, elements) {
    super();
    this.name = name;
    this.sets = sets;
    this.elements = elements;
  }
}
SetOfSets.fromCsv = (name, rawString) => {
  const elements = {};
  const sets = {};

  const rows = rawString.split('\n');

  // Get the headers
  const headers = rows[0].split(',');
  for (const header of headers.slice(1)) {
    sets[header] = {
      name: header,
      ordered: false,
      members: []
    };
  }

  // Parse each row
  for (const row of rows.slice(1)) {
    const cols = row.split(',');
    const element = {
      name: cols[0],
      memberships: {},
      position: {
        x: Math.random() * DEFAULT_SIZE.width,
        y: Math.random() * DEFAULT_SIZE.height,
        fixed: false
      }
    };
    elements[cols[0]] = element;
    let colIndex = 1;
    for (let memberIndex of cols.slice(1)) {
      memberIndex = parseInt(memberIndex);
      if (memberIndex >= 1) {
        const setName = headers[colIndex];
        sets[setName].members.push({
          element: element.name,
          memberIndex
        });
        element.memberships[setName] = true;
        if (memberIndex > 1) {
          sets[setName].ordered = true;
        }
      }
      colIndex++;
    }
  }

  // At this point, we know whether sets are ordered,
  // so we can sort + flatten their members lists
  for (const setObj of Object.values(sets)) {
    setObj.members = setObj.members
      .sort((a, b) => {
        return a.memberIndex - b.memberIndex;
      }).map(elementObj => {
        return elementObj.element;
      });
  }

  return new SetOfSets(name, sets, elements);
};
export default SetOfSets;
