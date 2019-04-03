import matplotlib.pyplot as mpl
import networkx as nx
import numpy as np
from dataclasses import dataclass, field
from typing import Any
from networkx.drawing.nx_pydot import write_dot

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class Vertex:
    def __init__(self, arrayOfEdges, number):
        self.arrayOfEdges = arrayOfEdges # one-hot encoded numpy vector, with indices corresponding to Hyperedge IDs (integer "value"s)
        self.number = number # number == integer ID
        self.arrayOfContaining = np.full((len(arrayOfEdges)), number) # what does this do?

class Edge:
    def __init__(self, firstVertex, secondVertex, distance, hypSize):
        self.firstVertex = firstVertex # Vertex object
        self.secondVertex = secondVertex # Vertex object
        self.distance = distance # some kind of float / weighting that indicates how far apart vertices should be, but NOT used to compute the layout (only used to order edges)
        self.hyperEdge = np.zeros(hypSize) # one-hot encoded numpy vector, indices corresponding to hyperedge IDs (integer "value"s)
        # TODO: self.hyperEdgeOrder = [ ... numeric hyperedge IDs ... ]

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

class Hypervertex:
    def __init__(self, setOfEdges, number):
        self.setOfEdges = setOfEdges # set containing Hyperedge IDs (integer "value"s)
        self.number = number # number == integer ID

class Hyperedge:
    def __init__(self, value):
        self.value = value # value == integer ID

class Hypergraph:
    def __init__(self, vertices, edges):
        self.vertices = vertices # set of Hypervertices
        self.edges = edges # set of Hyperedges

def distance2(vertex, vertex2, edgeNumber):
    summation = 0
    for i in range(edgeNumber):
        if (vertex.arrayOfEdges[i] > 0 and vertex2.arrayOfEdges[i] > 0):
            if(vertex.arrayOfContaining[i] != vertex2.arrayOfContaining[i]):
                summation = summation - 1
    return summation


def distance(vertex, vertex2, edgeNumber):
    summation = 0
    for i in range(edgeNumber):
        if (vertex.arrayOfEdges[i] > 0 and vertex2.arrayOfEdges[i] > 0):
            if(vertex.arrayOfContaining[i] != vertex2.arrayOfContaining[i]):
                summation = summation - 1
        if (vertex.arrayOfEdges[i] > 0 and vertex2.arrayOfEdges[i] == 0):
            summation = summation + 0.01
        if (vertex.arrayOfEdges[i] == 0 and vertex2.arrayOfEdges[i] != 0):
            summation = summation + 0.01
    return summation

def edgeChanger(vertex, vertex2, edge, edgeNumber):
    edge.hyperEdge = np.zeros(edgeNumber)
    for i in range(edgeNumber):
        if(vertex.arrayOfEdges[i] == 1 and vertex2.arrayOfEdges[i] == 1):
            edge.hyperEdge[i] = 1
def updateVertex(ver, ind):
    if ver.arrayOfEdges[ind] == 2:
        ver.arrayOfEdges[ind] = -1
    elif ver.arrayOfEdges[ind] == 1:
        ver.arrayOfEdges[ind] = 2

def graphToNetworkX(edges, vertexNumber):
    G = nx.Graph()
    for i in range(vertexNumber):
        G.add_node(i+1)
    for e in edges:
        G.add_edge(e.firstVertex.number, e.secondVertex.number)
    return G

def graphToMultiNetworkX(edges, vertexNumber):
    G = nx.MultiGraph()
    for i in range(vertexNumber):
        G.add_node(i+1)
    for e in edges:
        for i in range (len(e.hyperEdge)):
            if e.hyperEdge[i] > 1:
                color = lineToColor(i)
                G.add_edge(e.firstVertex.number, e.secondVertex.number, color)
    write_dot(G, 'multi6.dot')
    return G

def lineToColor(number2):
    number = number2 + 1
    if number == 1:
        return 'red'
    elif number == 2:
        return 'green'
    elif number == 3:
        return "yellow"
    elif number == 4:
        return "orange"
    elif number == 5:
        return "purple"
    elif number == 6:
        return "brown"
    elif number == 7:
        return "blue"
    elif number == 8:
        return "black"
    elif number == 9:
        return "azure3"
    elif number == 10:
        return "antiquewhite"
    else:
        return "beige"

def forceDirectedStuff(G):
    return nx.spring_layout(G)

def update(edge, vertices):
    v1 = edge.firstVertex
    v2 = edge.secondVertex
    for i in range(len(edge.hyperEdge)):
        if(v1.arrayOfEdges[i] > 0 and v2.arrayOfEdges[i]> 0):
            if(v1.arrayOfContaining[i] != v2.arrayOfContaining[i]):
                edge.hyperEdge[i] = 2
                updateVertex(v1, i)
                updateVertex(v2, i)
                updateComp(vertices, v1.arrayOfContaining[i], v2.arrayOfContaining[i], i)

def updateComp(vertices, old, new, pos):
    obj = list(filter(lambda x: old == x.arrayOfContaining[pos], vertices))
    for element in obj:
        element.arrayOfContaining[pos] = new

def updateDistance(edge):
    v1 = edge.item.firstVertex
    v2 = edge.item.secondVertex
    edge.item.distance = distance(v1, v2, len(v1.arrayOfEdges))
    edge.priority = distance(v1, v2, len(v1.arrayOfEdges))

def strangeSteinerProblem4(g):
    orderEdges = []
    edges = g.edges
    vertices = g.vertices

    while len(edges) > 0:
        edges.sort()
        #for e in edges:
         #  print(e.item.distance)

        #print("NEXTROUND")
        edge = edges[0]
        edges.remove(edge)
        if edge.item.distance >= 0:
            #print(str(edge.item.firstVertex.number) + ";" + str(edge.item.secondVertex.number))
            #print (distance3(edge.item.firstVertex, edge.item.secondVertex,4))
            return orderEdges

        orderEdges.append(edge.item)
        update(edge.item, vertices)

        for e in edges:
            updateDistance(e)
        #map(updateDistance, edges)
        #map(updateDistance, edges)

    return orderEdges


def hypergraphToGraph(hypergraph):
    vertexSet = set()
    hypervertices = hypergraph.vertices
    edgeNumber = len(hypergraph.edges)
    for hypervertex in hypervertices:
        v = Vertex(np.zeros(edgeNumber, dtype=int), hypervertex.number)
        for hyperedge in hypervertex.setOfEdges:
            v.arrayOfEdges[hyperedge-1] = 1
        vertexSet.add(v)
    edgeSet = []
    for vertex in vertexSet:
        for vertex2 in vertexSet:

            if vertex.number < vertex2.number:
                dist = distance(vertex, vertex2, edgeNumber)
                e = Edge(vertex, vertex2, dist, edgeNumber) # Every pairwise vertex combination INITIALLLY gets an Edge object
                edgeChanger(vertex, vertex2, e, edgeNumber)
                obj = PrioritizedItem(dist, e)
                edgeSet.append(obj)

    return Graph(vertexSet, edgeSet)



ver1 = Hypervertex(set([1, 2, 3]), 1)
ver2 = Hypervertex(set([2, 5]), 2)
ver3 = Hypervertex(set([1, 2, 3, 4]), 3)
ver4 = Hypervertex(set([1, 2, 3, 4]), 4)
ver5 = Hypervertex(set([3,6]), 5)
ver6 = Hypervertex(set([4]),6)
ver7 = Hypervertex(set([1, 2, 3, 4,5,6]), 7)
ver8 = Hypervertex(set([3,4,6]), 8)
ver9 = Hypervertex(set([1,4,5]),9)
ver10 = Hypervertex(set([1,2,7]),10)
ver11 = Hypervertex(set([1,4,7]),11)
ver12 = Hypervertex(set([5,7]),12)
ver13 = Hypervertex(set([2,6,7]),13)
ver14 = Hypervertex(set([2,3,7]),14)
ver15 = Hypervertex(set([1,3]),15)
ver16 = Hypervertex(set([3,7]),16)
ver17 = Hypervertex(set([3,6]),17)
ver18 = Hypervertex(set([2,5]),18)
ver19 = Hypervertex(set([3,7]),19)
ver20 = Hypervertex(set([2,3,6]),20)



ver = set([ver1, ver2, ver3, ver4, ver5, ver6, ver7, ver8, ver9, ver10, ver11, ver12, ver13, ver14, ver15, ver16, ver17, ver18, ver19])

#h = list(filter(lambda x: 4 in x.setOfEdges, ver))
#print(len(h))
hedge1 = Hyperedge(1)
hedge2 = Hyperedge(2)
hedge3 = Hyperedge(3)
hedge4 = Hyperedge(4)
hedge5 = Hyperedge(5)
hedge6 = Hyperedge(6)
hedge7 = Hyperedge(7)
hedge8 = Hyperedge(8)
hedge = set([hedge1, hedge2, hedge3, hedge4, hedge5, hedge6, hedge7])
h = Hypergraph(ver, hedge)
g = hypergraphToGraph(h)

#e1 = heapq.heappop(g.edges)
#print(e1.item.hyperEdge[2])

list = strangeSteinerProblem4(g) # list of Edge objects, filters to only the ones that will be rendered


r = graphToNetworkX(list, len(ver))
p = graphToMultiNetworkX(list, len(ver)) # writes dot file; p not used?
s = forceDirectedStuff(r)
#s = forceDirectedStuff(p)
#A = nx.nx_agraph.to_agraph(s)
nx.draw(r, s)
for a in list:
    print(str(a.firstVertex.number) + "," + str(a.secondVertex.number) + ";" + str(a.distance))
#mpl.show()
