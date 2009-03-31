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

from xmlrpclib import ServerProxy
	
class Graph( object ):

	ADDRESS = "http://127.0.0.1:8000/"
	"""The default pyWebGraph XML-RPC server address: `http://127.0.0.1:8000/`"""
	
	def __init__( self, address = None ):
		if not address: address = Graph.ADDRESS
		self.__proxy = ServerProxy( address )
		self.__wrapped = [ 'current_node', 'num_nodes', 'node_tos' ]

	def __getattr__( self, name ):
		if name in self.__wrapped:
			return getattr( self, name )
		else:
			return getattr( self.__proxy, name )
		
	def get_num_nodes( self ):
		return self.__proxy.get_num_nodes()
	
	num_nodes = property( get_num_nodes )

	def get_current_node( self ):
		return self.__proxy.get_current_node()
		
	def set_current_node( self, node ):
		return self.__proxy.set_current_node( node )

	current_node = property( get_current_node, set_current_node )

	def node_tos( self, node ):
		return self.__proxy.node_tos( node ).encode( 'utf8' )
