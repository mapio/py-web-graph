#!/usr/bin/env python

from distutils.core import setup
from os import walk
from os.path import join

docs_src = 'docs/_build/html/'
docs_dst = 'docs/html'
doc_files = []
for dirpath, dirnames, filenames in walk( docs_src ):
	if '.svn' in dirnames: dirnames.remove( '.svn' )
	fs = []
	for f in filenames:
		if not f.startswith( '.' ): fs.append( join( dirpath, f ) )
	doc_files.append( ( join( docs_dst, dirpath[ len( docs_src ) : ] ), fs ) )

setup(
	name = 'pyWebGraph',
	version = '0.1a',
	description = 'A bridge between WebGraph and Python/Jython',
	author = 'Massimo Santini',
	author_email = 'santini@dsi.unimi.it',
	url = 'http://py-web-graph.googlecode.com/',
	packages = [ 'pywebgraph', 'pywebgraph.examples', 'pywebgraph.webgraph' ],
	data_files = [ ( 'docs', [ 'COPYING', 'README.txt' ] ) ] + doc_files,
)
