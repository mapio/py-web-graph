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

def new_local_graph():
	try:
		from java.lang import Exception as JException
	except ImportError:
		raise RuntimeError, 'To acess WebGraph data you need to run this with jython.'
	else:
		from pywebgraph.webgraph.local import Graph
		return Graph()
	
def new_remote_graph( address = None ):
	from pywebgraph.webgraph.client import Graph
	import xmlrpclib
	import socket
	graph = Graph( address )
	try:
		graph.current_node
	except xmlrpclib.Fault:
		pass
	except socket.error:
		raise RuntimeError, "pyWebGraph XML-RPC server at %s not responding." % address
		graph = None
	except:
		raise
	return graph