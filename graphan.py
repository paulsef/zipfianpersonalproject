import networkx as nx
def make_graph():
	f = open('graph.txt')
	mapping = f.readlines()
	edges = [line.strip().split() for line in mapping]
	G = nx.Graph()
	#nodes = set([edge[0] for edge in edges] + [edge[1] for edge in edges])
	#G.add_nodes_from(nodes)
	G.add_edges_from(edges)
	return G