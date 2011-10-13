#! /usr/bin/env python 

import sys, os
from pylab import *
from numpy.random import *
seed(2)

from graph_tool.all import *

# lets build a price network. Following algorithm is shameless copied from
# graph-tool quick-start guide.

g = Graph()

v_age = g.new_vertex_property("int")
e_age = g.new_edge_property("int")

# final size of network
N = 100000

v = g.add_vertex()
v_age[v] = 0

vlist = [v]

for i in xrange(1,N):
    # create our new vertex
    v = g.add_vertex()
    v_age[v] = i
    
    i = randint(0, len(vlist))
    target = vlist[i]

    e = g.add_edge(v, target)
    vlist.append(v)


in_hist = vertex_hist(g, "in")

figure(figsize=(4,3))
errorbar(in_hist[1][:-1], in_hist[0], fmt="o", yerr=sqrt(in_hist[0]),
        label="in")
gca().set_yscale("log")
gca().set_xscale("log")
gca().set_ylim(1e-1, 1e5)
gca().set_xlim(0.8, 1e3)
subplots_adjust(left=0.2, bottom=0.2)
xlabel("$k_{in}$")
ylabel("$NP(k_{in})$")
savefig("deg-hist.pdf")



graph_draw(g, vprops={"label":g.vertex_index}, output="two-nodes.pdf")
