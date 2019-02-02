import { Model } from '../../node_modules/uki/dist/uki.esm.js';

class SetOfSets extends Model {
  constructor (sets, elements) {
    super();
    this.sets = sets;
    this.elements = elements;
  }
}
SetOfSets.fromCsv = rawString => {
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
      memberships: {}
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

  return new SetOfSets(sets, elements);
};
export default SetOfSets;
