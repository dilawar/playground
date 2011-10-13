from graph_tool.all import *
from itertools import izip
from numpy.random import randint

# here is a undirected graph
g = Graph()
g.add_vertex(100)

# create graph
for s,t in izip(randint(0, 100, 150), randint(0, 100, 150)):
    g.add_edge(g.vertex(s), g.vertex(t))


vprop_double = g.new_vertex_property("double")
vprop_double[g.vertex(10)] = 3.1416

vprop_vint = g.new_vertex_property("vector<int>")
vprop_vint[g.vertex(40)] = [1, 3, 42, 54]

# Draw
graph_draw(g, vprops={"label":g.vertex_index}, output="two-nodes.pdf")
