from functools import wraps

try:
	from java.lang import Exception as JException
	from it.unimi.dsi.webgraph import ImmutableGraph
	from it.unimi.dsi.fastutil.io import BinIO 
except:
	pass # kludge to allow for Sphinx automodule

def _convert_to_runtime( f ):
	@wraps( f )
	def wrapper( self, *args, **kwargs ):
		try:
			result = f( self, *args, **kwargs )
		except ( Exception, JException ), msg:
			raise RuntimeError, msg
		else:
			return result
	return wrapper
	
class Graph( object ):

	def __init__( self ):
		self.graph = None
		self._url_to_node_map = None
		self._node_to_url_map = None
		self._current_node = 0
	
	def get_current_node( self ):
		assert self.graph
		return self._current_node
		
	def set_current_node( self, node ):
		assert self.graph and node >= 0 and node < self.num_nodes
		self._current_node = node
	
	current_node = property( get_current_node, set_current_node )
	
	def get_num_nodes( self ):
		return self._num_nodes
		
	num_nodes = property( get_num_nodes )
	
	@_convert_to_runtime
	def load_graph( self, path ):
		self.graph = ImmutableGraph.load( path )
		self._num_nodes = self.graph.numNodes()
		self._url_to_node_map = None
		self._node_to_url_map = None
		self.current_node = 0

	@_convert_to_runtime
	def load_url_map( self, path ):
		assert self.graph
		self._url_to_node_map = BinIO.loadObject( path )
		self._node_to_url_map = self._url_to_node_map.list()
	
	def url_to_node( self, url ):
		assert self.graph
		if self._url_to_node_map:
			return self._url_to_node_map.getLong( url )
		else:
			return -1

	def node_to_url( self, node ):
		assert self.graph and node >= 0 and node < self.num_nodes
		if self._node_to_url_map:
			return self._node_to_url_map.get( node ).toString()
		else:
			return ''

	def outlinks( self, node ):
		assert self.graph and node >= 0 and node < self.num_nodes
		outdegree = self.graph.outdegree( node )
		return self.graph.successorArray( node ).tolist()[ 0 : outdegree ]

	def resolve( self, node_spec ):
		assert self.graph
		if not node_spec:
			node = self.current_node
		elif node_spec.startswith( '#' ):
			node = int( node_spec[ 1: ] )
		elif node_spec.startswith( 'http://' ):
			node = self.url_to_node( node_spec )
			if node == -1:
				raise ValueError, 'URL not in map (maybe the map was not loaded)'
		else:
			nodes = node_spec.rstrip( '/' ).split( '/' )
			pos = 0
			curr = nodes.pop( 0 )
			if curr:
				outlinks = self.outlinks( self.current_node )
				x = int( curr )
				if x < 0 or x >= len( outlinks ):
					raise ValueError, 'URL not in path at pos ' + str( pos )
				node = outlinks[ x ]
			else:
				node = 0
			while nodes:
				pos = pos + 1
				outlinks = self.outlinks( node )
				x = int( nodes.pop( 0 ) )
				if x < 0 or x >= len( outlinks ):
					raise ValueError, 'URL not in path at pos ' + str( pos )
				node = outlinks[ x ]
		if node < 0 or node >= self.num_nodes:
			raise ValueError, 'Node out of range'
		return node

	def node_tos( self, node ):
		assert self.graph 
		def tos( node ):
			assert node >= 0 and node < self.num_nodes
			return '#' + str( node ) + ' ' + self.node_to_url( node )
		if isinstance( node, int ):
			return tos( node )
		else:
			return '\n'.join( [ str( i ) + ': ' + tos( x ) for i, x in enumerate( node ) ] )

