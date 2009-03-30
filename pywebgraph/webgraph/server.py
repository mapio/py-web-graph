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