if __name__ == '__main__':

	from sys import argv, maxint
	
	from it.unimi.dsi.webgraph import ImmutableGraph
	from it.unimi.dsi.logging import ProgressLogger
	
	graph = ImmutableGraph.load( argv[ 1 ] )
	
	queue = []
	dist = [ maxint for i in range( graph.numNodes() ) ]
	ecc = 0
	
	lo = 0
	hi = graph.numNodes()
	
	pl = ProgressLogger()
	pl.start( "Starting visit..." )
	pl.expectedUpdates = hi - lo
	pl.itemsName = "nodes"
	
	for i in range( lo, hi ):
	
		if dist[ i ] == maxint:
	
			queue.append( i )
			dist[ i ] = 0
		
			while queue:
	
				curr = queue.pop( 0 )
				successors = graph.successors( curr )
				d = graph.outdegree( curr )
	
				while d != 0:
	
					d = d - 1
	
					succ = successors.nextInt()
					if dist[ succ ] == maxint:
						dist[ succ ] = dist[ curr ] + 1
						ecc = max( ecc, dist[ succ ] )
						queue.append( succ )
			
		pl.update()
			
	pl.done()
	
	print "The maximum depth of a tree in the breadth-first spanning forest is", ecc
	
