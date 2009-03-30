from cmd import Cmd
from random import choice
from shlex import split
from functools import wraps

from pywebgraph.ubigraph import Renderer

def _swallow_exceptions( f ):
	@wraps( f )
	def wrapper( *args, **kwargs ):
		try:
			result = f( *args, **kwargs )
		except Exception, msg:
			print 'Error:', msg
			return None
		else:
			return result
	return wrapper
		
class Console( Cmd ):

	def __init__( self, graph, renderer = None ):
		Cmd.__init__( self )
		self.prompt = ">> "
		self.intro = "Welcome to pyWebGraph console!"
		self.graph = graph
		self.renderer = renderer
		self._graph_loaded = False
		self._globals = {}
		self._locals = {}
	
	def emptyline( self ):	
		pass

	def default( self, line ):	   
		try:
			exec( line ) in self._globals, self._locals
		except Exception, e:
			print e.__class__, ":", e

	def do_EOF( self, args ):
		return -1 


	def _ensure_graph( f ):
		@wraps( f )
		def wrapper( self, *args, **kwargs ):
			if not self._graph_loaded:
				raise RuntimeError, "No graph loaded: ignoring command"
			else:
				return f( self, *args, **kwargs )
		return wrapper

	def _ensure_renderer( f ):
		@wraps( f )
		def wrapper( self, *args, **kwargs ):
			if not self.renderer:
				raise RuntimeError, "No renderer available: ignoring command"
			else:
				return f( self, *args, **kwargs )
		return wrapper


	@_swallow_exceptions
	def do_graph( self, args ):
		self.graph.load_graph( args )
		self._graph_loaded = True

	@_swallow_exceptions
	@_ensure_graph	
	def do_namemaps( self, args ):
		self.graph.load_name_map( args )

	@_swallow_exceptions
	@_ensure_graph
	def do_cn( self, args ):
		self.graph.current_node = self.graph.resolve( args )

	@_swallow_exceptions
	@_ensure_graph
	def do_pwn( self, args ):
		print self.graph.node_tos( self.graph.current_node )

	@_swallow_exceptions
	@_ensure_graph
	def do_ls( self, args ):
		print self.graph.node_tos( self.graph.outlinks( self.graph.resolve( args ) ) ) 

	@_swallow_exceptions
	@_ensure_graph
	def do_rwa( self, args ):
		num = int( args )
		curr = self.graph.current_node
		while num > 0:
			num = num - 1
			self.do_add( '#' + str( curr ) )
			print self.graph.node_tos( curr ) 
			outlinks = self.graph.outlinks( curr )
			if not outlinks: break
			curr = choice( outlinks )
		self.do_add( '#' + str( curr ) )	
		print self.graph.node_tos( curr )
		self.graph.current_node = curr

	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_add( self, args ):
		u = self.graph.resolve( args )
		for v in self.graph.outlinks( u ):
			if ( u == v ): continue
			self.renderer.addedge( u, v )

	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_shown( self, args ):
		print self.graph.node_tos( self.renderer.nodes )

	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_highlight( self, args ):
		self.renderer.id( self.graph.resolve( args ) )
		
	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_label( self, args ):
		sargs =	split( args )
		if len( sargs ) == 2:
			nodes = [ self.graph.resolve( sargs.pop( 0 ) ) ]
		else:
			nodes = self.renderer.nodes
		if sargs[ 0 ] == 'off':			
			for node in nodes:
				self.renderer.unlabel( node )		
		else:
			for node in nodes:
				self.renderer.label( node, self.graph.node_tos( node ) )		

	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_clear( self, args ):
		self.renderer.clear()


if __name__ == '__main__':

	from optparse import OptionParser

	import pywebgraph.webgraph

	parser = OptionParser()
	parser.add_option( "-r", "--renderer", help = "the address of the Ubigraph server (if equals to -, it will be expanded to the default value).", type = str )
	parser.add_option( "-g", "--graph-server", 	help = "the address of the XML-RPC pyWebGraph graph server (if equals to -, it will be expanded to the default value).", type = str )
	(options, args) = parser.parse_args()
	
	renderer = None
	if options.renderer:
		if options.renderer == '-': options.renderer = None
		try:
			renderer = Renderer( options.renderer )
		except RuntimeError, msg:
			print 'Error: connecting to ubigraph:', msg
	
	try:
		if options.graph_server:
			if options.graph_server == '-': options.graph_server = None
			graph = pywebgraph.webgraph.new_remote_graph( options.graph_server )
		else:
			graph = pywebgraph.webgraph.new_local_graph()
	except RuntimeError, msg:
		print 'Error: instantiating graph:', msg
	else:
		Console( graph, renderer ).cmdloop() 
