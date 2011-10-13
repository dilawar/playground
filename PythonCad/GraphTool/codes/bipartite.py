from graph_tool.all import * 
import warnings as warn
try:
    __IPYTHON__
except NameError:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    # Now ipshell() will open IPython anywhere in the code
else:
    # Define a dummy ipshell() so the same code doesn't crash inside an
    # interactive IPython
    def ipshell(): pass

import unittest

g = Graph()

#usage: 
#   addSourceSink(graph, left vertices, right vertices)
def addSourceSink(g, nLeft, nRight):
    g.add_vertex(nLeft+nRight+2) # additional source and sink
    for v in g.vertices():
        if (int(v) >= 2) & (int(v) <= (nLeft + 1)):
            vLeft[v] = True
            #print vLeft[v]
        else:
            vLeft[v] = False
            #print vLeft[v]
    return g
def addEdges(g, edges):
    i = 0
    listEdges = list()
    for e in edges:
        listEdges.append(g.add_edge(g.vertex(int(e[0])), g.vertex(int(e[1]))))
        # and add capacity
        eCaps[listEdges[i]] = int(e[2])
        i += 1
    return g
def attachInfCapEdges(g):
    for v in g.vertices():
        if int(v) >= 2:
            if vLeft[v] == True :
                e = g.add_edge(g.vertex(0), v)
                eCaps[e] = inf
            else:
                e = g.add_edge(v, g.vertex(1))
                eCaps[e] = inf
    return g
def edmondKarp(graph, prop):
    src, tgt = graph.vertex(0), graph.vertex(1)
    res = edmonds_karp_max_flow(graph, src, tgt, prop)
    res.a = prop.a - res.a
    max_flow = sum(res[e] for e in tgt.in_edges())
    return max_flow, res.a
def pushRelabel(graph, prop):
    src, tgt = graph.vertex(0), graph.vertex(1)
    res = push_relabel_max_flow(graph, src, tgt, prop)
    res.a = prop.a - res.a
    max_flow = sum(res[e] for e in tgt.in_edges())
    return max_flow, res.a
def kolmogorov(graph, prop):
    src, tgt = graph.vertex(0), graph.vertex(1)
    res = boykov_kolmogorov_max_flow(graph, src, tgt, prop)
    # here we have a bug. res returned by above method does not have the same length
    # as others.
    if res.a.size == prop.a.size:
         res.a = prop.a - res.a
    else:
        warn.warn("Loop found here. This method can't handle it")
        return -1, res.a
    max_flow = sum(res[e] for e in src.out_edges())
    return max_flow, res.a
class GraphTestClass(unittest.TestCase):  
    # this is responsible in setting up the test-bench.
    def setUp(self): pass

    def createData(self, g, prop):
        self.flow1, self.res1 = edmondKarp(g, prop)
        self.flow2, self.res2 = pushRelabel(g, prop)
        self.flow3, self.res3 = kolmogorov(g, prop)
 
    # for graph g
    def diffAlgoSameResult(self):
        self.createData(g, eCaps)
        if self.flow1 > 0 and self.flow2 > 0 and self.flow3 > 0 : 
            self.assertEqual(self.flow1, self.flow2
                , 'Uneuqal result from diff algorithms')
            self.assertEqual(self.flow2, self.flow3
                , 'Uneuqal result from diff algorithms')
            #self.assertEqual(self.res1.all(), self.res2.all())
            #self.assertEqual(self.res2.all(), self.res3.all())
        else:
            warn.warn("Negative Flow. One of more method is unsuitable.")

    # check if graph is bipartite.
    def isBipartite(self):
        for e in g.edges():
            self.assertFalse(vLeft[g.vertex(int(e.source()))] &
                vLeft[g.vertex(int(e.target()))], 'Not a bipartite graph')


inf = 1000000 # infinite capacity.
vName = g.new_vertex_property("string") # name of the vertes (optional)
vLeft = g.new_vertex_property("bool") # if left or right node (left = True)
eName = g.new_edge_property("string") # name of an edge (optional)
eCaps = g.new_edge_property("int32_t") # capacity of edge
eFlow = g.new_edge_property("int32_t") # flow in edge 
# position of nodes
v_pos = g.new_vertex_property("vector<double>")


# Our graph contains 9 vertices. 5 on left, 4 on right.
g = addSourceSink(g, 5, 4)

edges = [(2,7,2), (2,9,11), (3,7,9), (3,8,9), (4,8,9)
        , (10,4,4), (5,10,5), (5,9,2), (6,10,8), (9,6,5)]
g = addEdges(g, edges)

g = attachInfCapEdges(g)



flow1, res1 = edmondKarp(g, eCaps)
print flow1, res1
flow2, res2 = pushRelabel(g, eCaps)
print flow2, res2
flow3, res3 = kolmogorov(g, eCaps)
print flow3, res3
# covert properties to global properties.
g.edge_properties["caps"] = eCaps # capacity
g.vertex_properties["lr"] = vLeft # left or right
g.save("graphs/bipartite.xml.gz")
# and print also.
graph_draw(g #, pos=v_pos
    , vprops={"label":g.vertex_index}
    , eprops = {"label":eCaps}
    , sep = 1.0, output="figs/bip__flow.pdf")

def suite():
    tests = ['diffAlgoSameResult', 'isBipartite']
    return unittest.TestSuite(map(GraphTestClass, tests))

# comment out following line if you don't want to run these tests.
bipSuite = suite()
unittest.TextTestRunner(verbosity=3).run(bipSuite)

#ipshell() # if we want to drop into ipython
