ADDRESS = 'http://127.0.0.1:20738/RPC2'
	
class Renderer( object ):

	def __init__( self, address = ADDRESS ):
		import xmlrpclib
		import socket
		try:
			self.server = xmlrpclib.Server( address ).ubigraph
		except socket.error, msg:
			raise RuntimeError, 'connecting to ubigraph: ' + msg
		self.clear()
	
	def clear( self ):
		self.server.clear()
		self.server.set_vertex_style_attribute( 0, "color", "#ff00ff" )
		self.server.set_vertex_style_attribute( 0, "shape", "sphere" )
		self.server.set_edge_style_attribute( 0, "oriented", "true" )
		self.highlightStyle = self.server.new_vertex_style( 0 )
		self.server.set_vertex_style_attribute( self.highlightStyle, "color", "#ff80ff" )
		self.server.set_vertex_style_attribute( self.highlightStyle, "size", "2.0" )
		self.nodes = []
		self.edges = []

	def label( self, node, label ):
		if node not in self.nodes:
			self.nodes.append( node )
			self.server.new_vertex_w_id( node )
		self.server.set_vertex_attribute( node, 'label', label )

	def unlabel( self, node ):
		if node not in self.nodes: return
		self.server.change_vertex_style( node, 0 )

	def addnode( self, node ):
		if node not in self.nodes:
			self.nodes.append( node )
			self.server.new_vertex_w_id( node )
		
	def addedge( self, from_node, to_node ):
		if ( from_node, to_node ) not in self.edges:
			self.edges.append( ( from_node, to_node ) )
			self.addnode( from_node )
			self.addnode( to_node )
			self.server.new_edge( from_node, to_node )

	def highlight( self, node ):
		from threading import Timer
		def unHighlight():
			self.server.change_vertex_style( node, 0 )
		if node in self.nodes:
			self.server.change_vertex_style( node, self.highlightStyle )
			Timer( 1, unHighlight ).start()
			
	def addcallback( self, callback_url ):
		self.server.set_vertex_style_attribute( 0, "callback_left_doubleclick", callback_url )
