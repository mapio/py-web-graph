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

if __name__ == '__main__':

	from sys import argv, maxint
	
	from pywebgraph.webgraph.local import Graph
	
	graph = Graph()
	graph.load_graph( argv[ 1 ] )
	
	queue = []
	dist = [ maxint for i in range( graph.num_nodes ) ]
	ecc = 0
	
	lo = 0
	hi = graph.num_nodes
	
	for i in range( lo, hi ):
	
		if dist[ i ] == maxint:
	
			queue.append( i )
			dist[ i ] = 0
		
			while queue:
	
				curr = queue.pop( 0 )
				for succ in graph.outlinks( curr ):
					if dist[ succ ] == maxint:
						dist[ succ ] = dist[ curr ] + 1
						ecc = max( ecc, dist[ succ ] )
						queue.append( succ )
			
	print "The maximum depth of a tree in the breadth-first spanning forest is", ecc
	
