# pyWebGraph, a bridge between WebGraph an {J,P}ython 
# Copyright (C) 2009 Massimo Santini
# 
# This file is part of pyWebGraph.
# 
# pyWebGraph is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyWebGraph is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyWebGraph.  If not, see <http://www.gnu.org/licenses/>.

from cmd import Cmd
from functools import wraps
from random import choice
from re import search
from shlex import split
from types import FunctionType

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
	return f

def _add_help_from_doc( cls ):
	def mk_help_func( name ):
		def help_func( self ):
			print getattr( self, name ).__doc__
		help_func.__name__ = 'help_' + name[ 3 : ]
		help_func.__doc__ = 'Auto-generated'
		return help_func
	for name, obj in cls.__dict__.items():
		if type( obj ) is FunctionType:
			if name.startswith( 'do_' ) and obj.__doc__:
				help_func_name = 'help_' + name[ 3 : ]
				if not help_func_name in cls.__dict__:
					setattr( cls, help_func_name, mk_help_func( name ) )
	return cls

class Console( Cmd ):

	def __init__( self, graph, renderer = None ):
		Cmd.__init__( self )
		self.prompt = ">> "
		self.intro = """pyWebGraph console, Copyright (C) 2009 Massimo Santini
This program comes with ABSOLUTELY NO WARRANTY; for details type `help'.
This is free software, and you are welcome to redistribute it under 
certain conditions; see the COPYING file for details."""
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

	def do_help( self, arg ):
		if arg:	Cmd.do_help( self, arg )
		else:
			print "Available commands:",
			print ", ".join( [ name[ 3 : ] for name in dir( self )	if name.startswith( 'do_' ) and getattr( self, name ).__doc__ ] )
			print "Use 'help <command>' for details."


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
		"""graph basename
Loads the graph specified by the given basename; if basename + '-t' is present, it also load the transposed graph."""
		self.graph.load_graph( args )
		if self.renderer: self.renderer.clear()
		self._graph_loaded = True

	@_swallow_exceptions
	@_ensure_graph	
	def do_namemaps( self, args ):
		"""namemaps basename
Loads the name to node maps specified by the given basename (allowed extensions are, 'fcsl', 'iepm', and 'mwhc')."""
		self.graph.load_name_map( args )

	@_swallow_exceptions
	@_ensure_graph
	def do_cn( self, args ):
		"""cn [node_spec]
Sets the current working node to the one specified by the given node_spec."""
		self.graph.current_node = self.graph.resolve( args )

	@_swallow_exceptions
	@_ensure_graph
	def do_pwn( self, args ):
		"""pwn
Prints the current working node."""
		print self.graph.node_tos( self.graph.current_node )

	@_swallow_exceptions
	@_ensure_graph
	def do_ls( self, args ):
		"""ls [node_spec]
Prints a list of the outlinks of the given node_spec."""
		print self.graph.node_tos( self.graph.outlinks( self.graph.resolve( args ) ) )

	@_swallow_exceptions
	@_ensure_graph
	def do_sl( self, args ):
		"""sl [node_spec]
Prints a list of the inlinks of the given node_spec."""
		print self.graph.node_tos( self.graph.inlinks( self.graph.resolve( args ) ) ) 

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
	def do_bfs( self, args ):
		"""bsf [depth [node_spec]]
Performs a BFS of given depth (default 1) from the given node_spec adding discovered nodes (and edges) to the renderer."""
		m = search( r'(?:(\d+)){0,1}(?:\s+(.*)){0,1}', args )
		if not m: raise ValueError, "Must specify depth and an optional node_spec"
		depth = int( m.group( 1 ) ) if m.group( 1 ) else 1
		u = self.graph.resolve( m.group( 2 ) if m.group( 2 ) else '' )
		queue = [ u, -1 ]
		self.renderer.addnode( u )
		while queue and depth:
			u = queue.pop( 0 )
			if u < 0:
				depth = depth - 1
				queue.append( u )
				continue
			for v in self.graph.outlinks( u ):
				self.renderer.addedge( u, v )
				queue.append( v )

	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_isg( self, args ):
		"""isg
Makes the graph in the rendered the induced subgraph given by the shown nodes."""
		for u in list( self.renderer.nodes ):
			for v in self.graph.outlinks( u ):
				self.renderer.addedge( u, v, False )
			
	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_shown( self, args ):
		"""shown
List the nodes added to the renderer so far."""
		print self.graph.node_tos( self.renderer.nodes )

	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_hl( self, args ):
		"""hl [node_spec]
Highlights in the renderer the node specified by the given node_spec."""
		self.renderer.highlight( self.graph.resolve( args ) )
		
	@_swallow_exceptions
	@_ensure_graph
	@_ensure_renderer
	def do_label( self, args ):
		"""label [node_spec] [off]
Turns on/off the label in the renderer of the node specified by the given node_spec."""
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
		"""clear
Clears the renderer."""
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
