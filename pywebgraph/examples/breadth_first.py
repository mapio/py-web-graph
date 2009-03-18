if __name__ == '__main__':

	from sys import argv, maxint
	
	from pywebgraph.webgraph.local import Graph
	
	graph = Graph()
	graph.load_graph( argv[ 1 ] )
	
	queue = []
	dist = [ maxint for i in range( graph.num_nodes ) ]
	ecc = 0
	
	lo = 0
	hi = graph.num_nodes
	
	for i in range( lo, hi ):
	
		if dist[ i ] == maxint:
	
			queue.append( i )
			dist[ i ] = 0
		
			while queue:
	
				curr = queue.pop( 0 )
				for succ in graph.outlinks( curr ):
					if dist[ succ ] == maxint:
						dist[ succ ] = dist[ curr ] + 1
						ecc = max( ecc, dist[ succ ] )
						queue.append( succ )
			
	print "The maximum depth of a tree in the breadth-first spanning forest is", ecc
	
