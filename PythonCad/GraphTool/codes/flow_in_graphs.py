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

g = Graph()

g1 = Graph()

def edmondKarp(graph, prop):
    src, tgt = graph.vertex(0), graph.vertex(1)
    res = edmonds_karp_max_flow(graph, src, tgt, prop) # graph-tool method
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
 
class TestForEquality(GraphTestClass):
    # add tests here.
    # for graph g1
    def testEqualG1(self):
        self.createData(g, e_caps)
        if self.flow1 > 0 and self.flow2 > 0 and self.flow3 > 0 : 
            self.assertEqual(self.flow1, self.flow2)
            self.assertEqual(self.flow2, self.flow3)
            self.assertEqual(self.res1.all(), self.res2.all())
            self.assertEqual(self.res2.all(), self.res3.all())
        else:
            warn.warn("Negative Flow. One of more method is unsuitable.")


v_name = g.new_vertex_property("string") # name of vertex
e_name = g.new_edge_property("string") # name of edge 
e_caps = g.new_edge_property("int32_t") # capacity on edges (must)
e_flow = g.new_edge_property("int32_t") # flow (optional)


v_pos = g.new_vertex_property("vector<double>")

vName = g1.new_vertex_property("string")
eName = g1.new_edge_property("string")
eCaps = g1.new_edge_property("int32_t")
eFlow = g1.new_edge_property("int32_t")

g.add_vertex(4) # a flow path with 4 vertex.
i = 0.0
for v in g.vertices():
    v_pos[g.vertex(v)] = [i,0.0]
    i += 2.0 # gap of 2 units
# we need to fix 0 and 1 manually
v_pos[g.vertex(0)] = [0.0,0.0]
v_pos[g.vertex(1)] = [6.0,0.0]


e12 = g.add_edge(g.vertex(0), g.vertex(2))
e_caps[e12] = 10
e23 = g.add_edge(g.vertex(2), g.vertex(3))
e_caps[e23] = 5
e31 = g.add_edge(g.vertex(3), g.vertex(1))
e_caps[e31] = 6

# total 6 vertices. O and 1 are source and sink vertex.
g1.add_vertex(6)

# add edges and assigned capacity.
e02 = g1.add_edge(g1.vertex(0), g1.vertex(2))
eCaps[e02] = 16
e03 = g1.add_edge(g1.vertex(0), g1.vertex(3))
eCaps[e03] = 13

e24 = g1.add_edge(g1.vertex(2), g1.vertex(4))
eCaps[e24] = 12
e23 = g1.add_edge(g1.vertex(2), g1.vertex(3))
eCaps[e23] = 10

e32 = g1.add_edge(g1.vertex(3), g1.vertex(2))
eCaps[e32] = 4
e34 = g1.add_edge(g1.vertex(3), g1.vertex(4))
eCaps[e34] = 9
e35 = g1.add_edge(g1.vertex(3), g1.vertex(5))
eCaps[e35] = 14

e41 = g1.add_edge(g1.vertex(4), g1.vertex(1))
eCaps[e41] = 20

e51 = g1.add_edge(g1.vertex(5), g1.vertex(1))
eCaps[e51] = 4
e54 = g1.add_edge(g1.vertex(5), g1.vertex(4))
eCaps[e54] = 7


max_flow1, res1 = edmondKarp(g, e_caps)
max_flow2, res2 = pushRelabel(g, e_caps)
max_flow3, res3 = kolmogorov(g, e_caps)
print max_flow1, max_flow2, max_flow3

max_flow1, res1 = edmondKarp(g1, eCaps)
max_flow2, res2 = pushRelabel(g1, eCaps)
max_flow3, res3 = kolmogorov(g1, eCaps)
print max_flow1, max_flow2, max_flow3

g.edge_properties["cap"] = e_caps 

g1.edge_properties["cap"] = eCaps 

g.save("graphs/simple_flow_path.xml.gz")
# and print also.
graph_draw(g , pos=v_pos
    , vprops={"label":g.vertex_index}
    , eprops = {"label":e_caps}
    , output="figs/simple_flow.pdf")

g.edge_properties["cap"] = e_caps 

g1.edge_properties["cap"] = eCaps 

g.save("./graphs/simple_flow_network.xml.gz")
# and print also.
graph_draw(g1
    , vprops={"label":g1.vertex_index}
    , eprops = {"label":eCaps}
    , sep = 2.0, output="./figs/flow_network.pdf")

#ipshell()
