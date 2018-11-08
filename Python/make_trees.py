
import networkx as nx
import matplotlib.pyplot as plt

def construct_Tree(i):
	#i is tree num
	
	G=nx.Graph()
	G.add_node(1)
	G.add_node(2)
	G.add_node(3)
	G.add_node(4)
	G.add_node(5)
	G.add_node(6)
	G.add_node(7)
	G.add_node(8)

	G.add_edge(1,2,color='k',weight=3)
	G.add_edge(2,3,color='k',weight=3)
	G.add_edge(3,4,color='k',weight=3)
	G.add_edge(4,5,color='k',weight=3)
	G.add_edge(5,6,color='k',weight=3)
	G.add_edge(6,7,color='k',weight=3)
	G.add_edge(2,8,color='k',weight=3)

	pos = {1: (30, 50), 2: (35, 50), 3: (40, 50), 4: (45, 50), 5:(50,50),
                6:(55,50), 7:(60,50), 8:(35,55)} 
        

	edges = G.edges()
	colors = [G[u][v]['color'] for u,v in edges]
	weights = [G[u][v]['weight'] for u,v in edges]
	colors_n = ['teal','crimson', 'gold', 'mediumblue', 'darkgreen', 'darkviolet','orangered', 'pink']

        # First fix the axis lower limits.
	nx.draw_networkx(G, pos=pos, edges=edges
                , with_labels = False
                , node_color=colors_n
                , edge_color=colors
                , width=weights
                )

        ax = plt.gca()   # (g)get (c)urrent (a)xis.
        ## You can manually set the left and right limits
        plt.ylim( bottom = 30, top=60 )
        ax.set_aspect( 'equal' )

        # Uncomment to remove the axis
        plt.axis('off')


	plt.savefig('Tree_'+ str(i)+'.png')
	#  plt.show()
	print i


#main

construct_Tree(1)



