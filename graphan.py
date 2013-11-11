import networkx as nx
import pdb

def make_graph():
	f = open('graph.txt')
	lines = f.readlines()
	info = [line.strip().split() for line in lines]
	edges =[(line[0],line[1]) for line in info]
	G = nx.Graph()
	color_dict = {}
	for line in info:
		color_dict[line[0]] = line[2]
	for node in color_dict.keys():
		G.add_node(node, color = color_dict[node])
	G.add_edges_from(edges)
	return G