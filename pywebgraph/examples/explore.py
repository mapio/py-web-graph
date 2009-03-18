if __name__ == '__main__':

	from sys import argv
	
	from pywebgraph.ubigraph import Renderer
	from pywebgraph.webgraph.local import Graph
	
	graph = Graph()
	graph.load_graph( argv[ 1 ] )
	renderer = Renderer()
	
	def callback( u ):
		try:
			for v in graph.outlinks( u ):
				if ( u == v ): continue
				renderer.addedge( u, v )
		except:
			return -1
		return 0

	import random
	from SimpleXMLRPCServer import SimpleXMLRPCServer
	
	port = random.randint( 20739, 20999 )
	callback_server = SimpleXMLRPCServer( ( "127.0.0.1", port ) )
	callback_server.register_introspection_functions()
	callback_server.register_function( callback )

	renderer.addcallback( "http://127.0.0.1:" + str( port ) + "/callback" )
	renderer.addnode( int( argv[ 2 ] ) )

	print "Callback server at port %d" % port
	callback_server.serve_forever()
	
	
