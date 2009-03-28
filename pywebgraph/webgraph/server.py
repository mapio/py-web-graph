from SimpleXMLRPCServer import SimpleXMLRPCServer

from pywebgraph.webgraph.local import Graph as LocalGraph

class Graph( object ):
	
	PORT = 8000
	"""The default pyWebGraph XML-RPC server port: `8000`"""
	
	def __init__( self, port = None ):
		if not port: port = Graph.PORT
		server = SimpleXMLRPCServer( ( "127.0.0.1", port ), allow_none = True )
		server.register_introspection_functions()
		server.register_multicall_functions()
		server.register_instance( LocalGraph() )
		print "Listening on port %d" % port
		server.serve_forever()
		
if __name__ == '__main__':

	from sys import argv

	if len( argv ) == 2:
		Graph( int( argv[ 1 ] ) )
	else:
		Graph()