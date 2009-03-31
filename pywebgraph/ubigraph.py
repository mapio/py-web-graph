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

class Renderer( object ):

	ADDRESS = 'http://127.0.0.1:20738/RPC2'
	"""The default Ubigraph XML-RPC server address: `http://127.0.0.1:20738/RPC2`"""

	def __init__( self, address = None ):
		import xmlrpclib
		import socket
		if not address: address = Renderer.ADDRESS
		try:
			self.server = xmlrpclib.Server( address ).ubigraph
			self.clear()
		except socket.error, msg:
			raise RuntimeError, 'connecting to ubigraph: ' + str( msg )
	
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
		
	def addedge( self, from_node, to_node, imply = True ):
		if ( from_node, to_node ) not in self.edges:
			if imply or ( from_node in self.nodes and to_node in self.nodes ):
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
