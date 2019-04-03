from dataclasses import dataclass, field
from typing import Any
import json
import numpy as np
import networkx as nx

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

def distance(vertex, vertex2, edgeNumber):
    summation = 0
    for i in range(edgeNumber):
        if vertex.arrayOfEdges[i] > 0 and vertex2.arrayOfEdges[i] > 0:
            if vertex.arrayOfContaining[i] != vertex2.arrayOfContaining[i]:
                summation = summation - 1
        if vertex.arrayOfEdges[i] > 0 and vertex2.arrayOfEdges[i] == 0:
            summation = summation + 0.01
        if vertex.arrayOfEdges[i] == 0 and vertex2.arrayOfEdges[i] != 0:
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

def updateComp(vertices, old, new, pos):
    obj = list(filter(lambda x: old == x.arrayOfContaining[pos], vertices))
    for element in obj:
        element.arrayOfContaining[pos] = new

def updateDistance(edge):
    v1 = edge.item.firstVertex
    v2 = edge.item.secondVertex
    edge.item.distance = distance(v1, v2, len(v1.arrayOfEdges))
    edge.priority = distance(v1, v2, len(v1.arrayOfEdges))

def update(edge, vertices):
    v1 = edge.firstVertex
    v2 = edge.secondVertex
    for i in range(len(edge.hyperEdge)):
        if v1.arrayOfEdges[i] > 0 and v2.arrayOfEdges[i] > 0:
            if v1.arrayOfContaining[i] != v2.arrayOfContaining[i]:
                edge.hyperEdge[i] = 2
                updateVertex(v1, i)
                updateVertex(v2, i)
                updateComp(vertices, v1.arrayOfContaining[i], v2.arrayOfContaining[i], i)

def strangeSteinerProblem4(g):
    orderEdges = []
    edges = g.edges
    vertices = g.vertices

    while edges:
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

def graphToNetworkX(edges, vertexNumber):
    G = nx.Graph()
    for i in range(vertexNumber):
        G.add_node(i+1)
    for e in edges:
        G.add_edge(e.firstVertex.number, e.secondVertex.number)
    return G

def forceDirectedStuff(G):
    return nx.spring_layout(G)

def strangeSteiner(jsonData):
    vertexSet = set()
    hypervertices = jsonData['vertices'].values()
    hyperedges = jsonData['hyperedges'].values()
    edgeNumber = len(hyperedges)
    for vertexIndex, hypervertex in enumerate(hypervertices):
        v = Vertex(np.zeros(edgeNumber, dtype=int), vertexIndex)
        for hyperedgeName in hypervertex['memberships'].keys():
            hyperedgeIndex = next(i for i, e in enumerate(hyperedges) if e['name'] == hyperedgeName)
            v.arrayOfEdges[hyperedgeIndex] = 1
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
    g = Graph(vertexSet, edgeSet)
    filteredEdgeList = strangeSteinerProblem4(g)
    nxGraph = graphToNetworkX(filteredEdgeList, len(hypervertices))
    indexedPositions = forceDirectedStuff(nxGraph)
    newPositions = {}
    for index, vertex in enumerate(hypervertices):
        newPositions[vertex['name']] = {
            'x': indexedPositions[index][0],
            'y': indexedPositions[index][1]
        }

    return json.dumps(newPositions)
