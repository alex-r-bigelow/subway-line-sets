export default {
  'vertices': {
    'vertexID': {
      'position': { 'x': 0, 'y': 0 },
      'fixed': false,
      'name': 'Some label',
      'size': '2em'
    }
  },
  'hyperedges': {
    'hyperedgeID': {
      'name': 'Some label',
      'color': '#bada55',
      'order': ['vertexID', 'vertexID'],
      'fixedOrder': false
    }
  },
  'settings': {
    'angleConstraint': '90'
    // ... TODO: edge crossing settings? others?
  }
};
