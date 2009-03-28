from xmlrpclib import ServerProxy
	
class Graph( object ):

	ADDRESS = "http://127.0.0.1:8000/"
	
	def __init__( self, address = None ):
		if not address: address = Graph.ADDRESS
		self.__proxy = ServerProxy( address )

	def get_num_nodes( self ):
		return self.__proxy.get_num_nodes()
	
	num_nodes = property( get_num_nodes )

	def get_current_node( self ):
		return self.__proxy.get_current_node()
		
	def set_current_node( self, node ):
		return self.__proxy.set_current_node( node )

	current_node = property( get_current_node, set_current_node )

	def __getattr__( self, name ):
		if name == 'current_node' or name == 'num_nodes' :
			return getattr( self, name )
		else:
			return getattr( self.__proxy, name )
