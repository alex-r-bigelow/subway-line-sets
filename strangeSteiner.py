from dataclasses import dataclass, field
from typing import Any
import json
import numpy as np
import networkx as nx
from math import sqrt
from math import acos
from math import pi

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
        self.ordering = np.zeros(hypSize) #ordering of the hyperedges passing this edge


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

# returns the correct order for a given hyperedge
def returnHyperedgeOrder(hyperedge, edges):
    order = []
    listOfEdges = []
    for e in edges:
        if(e.hyperEdge[hyperedge] > 1):
            listOfEdges.append(e)
    firstEdge = listOfEdges[0]
    listOfEdges.remove(firstEdge)
    v = firstEdge.firstVertex
    order.append(v)
    w = firstEdge.secondVertex
    order.append(w)
    while(len(listOfEdges) > 0):
        print(len(listOfEdges))
        for e in listOfEdges:
            if e.firstVertex == v:
                v = e.secondVertex
                order.insert(0,v)
                listOfEdges.remove(e)
                break
            if e.secondVertex == v:
                v = e.firstVertex
                order.insert(0,v)
                listOfEdges.remove(e)
                break
            if e.firstVertex == w:
                w = e.secondVertex
                order.append(w)
                listOfEdges.remove(e)
                break
            if e.secondVertex == w:
                w = e.firstVertex
                order.append(w)
                listOfEdges.remove(e)
                break

    return order                
                
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



#calculates the crossingproblematic parts of the graph
def calculateGraph(edges, hyperedges, layout):
    ilp = []
    for i in range(len(hyperedges)):
        for j in range(i+1, len(hyperedges)):
            a = combinedGraph(edges, i, j, layout)
            if(a == []):
                continue
            obj = (i,j)
            ilp.append((obj,a))
    return ilp

#helpfunction
def subtract(p1, p2, layout):
    point1 = layout[p1.number]
    point2 = layout[p2.number]
    ar = [0] * len(point1)
    for i in range(len(point1)):
        ar[i] = (point1)[i] - point2[i]
    return ar

#helpfunction
def length(v):
    return sqrt(v[0]**2+v[1]**2)

#helpfunction
def dot_product(v,w):
   return v[0]*w[0]+v[1]*w[1]

#helpfunction
def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]

#helpfunction
def inner_angle(v,w):
   cosx=dot_product(v,w)/(length(v)*length(w))
   rad=acos(cosx) # in radians
   return rad*180/pi # returns degrees

#helpfunction
def angle_clockwise(A, B):
    inner=inner_angle(A,B)
    det = determinant(A,B)
    if det<0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else: # if the det > 0 then A is immediately clockwise of B
        return 360-inner

# returns 0 if h1 is further clockwise
# returns -1 if h1 does not exist
#returns -2 if h2 does not exist
def order(oldvertex, currentVertex, h1, h2, edges, layout):
    h1Vertex = None
    h2Vertex = None
    for e in edges:
        if (e.hyperEdge[h1] > 1 and e.hyperEdge[h2] < 2):
            if currentVertex == e.firstVertex:
                h1Vertex = e.secondVertex
            if currentVertex == e.secondVertex:
                h1Vertex = e.firstVertex
        if (e.hyperEdge[h2] > 1 and e.hyperEdge[h1] < 2):
            if currentVertex == e.firstVertex:
                h2Vertex = e.secondVertex
            if currentVertex == e.secondVertex:
                h2Vertex = e.firstVertex
    if(h1Vertex == None):
        return -1
    if (h2Vertex == None):
        return -1
    eOld = np.array(subtract(oldvertex, currentVertex, layout))
    e1 = np.array(subtract(h1Vertex, currentVertex, layout))
    e2 = np.array(subtract(h2Vertex, currentVertex, layout))

    angle1 = angle_clockwise(eOld, e1)
    angle2 = angle_clockwise(eOld, e2)
    if(angle1 > angle2):
        return 0
    else:
        return 1

#helpfunction
def set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset

    return cover

#takes a set of conditions and returns a valid solution for the given setcover problem
def setCoverRunner(ilpInstance, numVertices):
    ilpReal = []
    subset = [set() for x in range(numVertices +1)]
    for obj in ilpInstance:
        for cov in obj[1]:
            ilpReal.append(cov)
    universe = set(range(len(ilpReal)))
    for obj in range(len(ilpReal)):
        for vertex in ilpReal[obj]:
            subset[vertex.number].add(obj)
    cover = set_cover(universe, subset)
    vertexCrossings = []
    for v in range(len(subset)):
        if(subset[v] in cover):
            vertexCrossings.append(v)
            cover.remove(subset[v])
    return vertexCrossings

#computes the ordering at each hyperedge
#cros list of vertices on which crossings occur (setcoverrunner)
def edgeOrdering(edges, hyperedges, layout, cros):
    for h1 in range(len(hyperedges)):
        for h2 in range(h1+1, len(hyperedges)):
            totalGraph(edges, h1, h2, layout, cros)
    for edge in edges:
        for h in range(len(edge.hyperEdge)):
            if(edge.hyperEdge[h] == 2):
                edge.ordering[h] = edge.ordering[h] + 1

#helfunction
def totalGraph(edges, h1, h2, layout, cros):
    listOfEdges = []
    for e in edges:
        if(e.hyperEdge[h1] > 1 and e.hyperEdge[h2] > 1):
            listOfEdges.append(e)
    while(len(listOfEdges) > 0):
        e = listOfEdges[0]
        listOfEdges.remove(e)
        ar = []
        v = e.firstVertex
        w = e.secondVertex
        vLast = w
        wLast = v
        ar.insert(0,v)
        ar.append(w)
        change = 1
        while(change == 1):
            change = 0
            for edge in listOfEdges:
                if edge.firstVertex == v:
                    listOfEdges.remove(edge)
                    vLast = v
                    v = edge.secondVertex
                    ar.insert(0,v)
                    change = 1
                    break
                if edge.secondVertex == v:
                    listOfEdges.remove(edge)
                    vLast = v
                    v = edge.firstVertex
                    ar.insert(0,v)
                    change = 1
                    break
                if edge.firstVertex == w:
                    listOfEdges.remove(edge)
                    wLast = w
                    w = edge.secondVertex
                    ar.append(w)
                    change = 1
                    break
                if edge.secondVertex == w:
                    listOfEdges.remove(edge)
                    wLast = w
                    w = edge.firstVertex
                    ar.append(w)
                    change = 1
                    break
        value1 = order(vLast, v, h1, h2, edges, layout)
        value2 = order(wLast, w, h1, h2, edges, layout)
        if( value1== value2 and value1 > -1 ):
            positionUpdater(edges, h1, h2, ar, value1, 1, cros)
        elif (value1 < 0):
            if(value2 < 0):
                positionUpdater(edges, h1, h2, ar, 0, 0, cros)
            else:
                positionUpdater(edges, h1, h2, ar, 1 - value2, 0, cros)
        elif(value2 < 0):
            positionUpdater(edges, h1, h2, ar, value1, 0, cros)
        else:
            positionUpdater(edges, h1, h2, ar, value1, 0, cros)

#helpfunction
def edgeOrientation(v,w):
    if(v.number > w.number):
        return -1
    return 1

#helpfunction
def edgeFinder(edges, u,v):
    if(u.number > v.number):
        a = v
        v = u
        u = a
    for e in edges:
        if(e.firstVertex == u and e.secondVertex == v):
            return e

#helpfunction
#val = 0 if no crossing one otherwise
def positionUpdater(edges, h1, h2, subgraph, val1, crosHappens, cros):
    num = val1
    if(len(subgraph) == 1):
        return
    updater = None
    edge = edgeFinder(edges, subgraph[0], subgraph[1])
    if(subgraph[0].number > subgraph[1].number):
        num = 1 - num

    if(num == 0):
        updater = h2
    else:
        updater = h1
    if(crosHappens == 1):
        if subgraph[0].number in cros:
            if (updater == h2):
                updater = h1
            else:
                updater = h2
            crosHappens = 0
            val1 = 1 - val1
    edge.ordering[updater] = edge.ordering[updater] + 1
    positionUpdater(edges, h1, h2, subgraph[1:len(subgraph)], val1, crosHappens, cros)

#supportEdges are the edges of the support graph (strangeSteiner)
#computes the ordering of the metrolines for each edge
def computeEdgeOrder(supportEdges, hyperedges, numVertices, layout):
    ilpInstance  = calculateGraph(supportEdges,hyperedges, layout)
    cover = setCoverRunner(ilpInstance, numVertices)
    edgeOrdering(supportEdges, hyperedges, layout, cover)

# helpfunction
def combinedGraph(edges, h1, h2, layout):
    listOfEdges = []
    listOfConnectedSubpaths = []
    for e in edges:
        if(e.hyperEdge[h1] > 1 and e.hyperEdge[h2] > 1):
            listOfEdges.append(e)
    while(len(listOfEdges) > 0):
        e = listOfEdges[0]
        listOfEdges.remove(e)
        ar = []
        v = e.firstVertex
        w = e.secondVertex
        vLast = w
        wLast = v
        ar.insert(0,v)
        ar.append(w)
        change = 1
        while(change == 1):
            change = 0
            for edge in listOfEdges:
                if edge.firstVertex == v:
                    listOfEdges.remove(edge)
                    vLast = v
                    v = edge.secondVertex
                    ar.insert(0,v)
                    change = 1
                    break
                if edge.secondVertex == v:
                    listOfEdges.remove(edge)
                    vLast = v
                    v = edge.firstVertex
                    ar.insert(0,v)
                    change = 1
                    break
                if edge.firstVertex == w:
                    listOfEdges.remove(edge)
                    wLast = w
                    w = edge.secondVertex
                    ar.append(w)
                    change = 1
                    break
                if edge.secondVertex == w:
                    listOfEdges.remove(edge)
                    wLast = w
                    w = edge.firstVertex
                    ar.append(w)
                    change = 1
                    break
        value1 = order(vLast, v, h1, h2, edges, layout)
        value2 = order(wLast, w, h1, h2, edges, layout)
        if( value1== value2 and value1 > -1 ):
            listOfConnectedSubpaths.append(ar.copy())

    return listOfConnectedSubpaths







