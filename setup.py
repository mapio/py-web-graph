#!/usr/bin/env python

from distutils.core import setup

setup(
	name = 'pyWebGraph',
	version = '0.1a',
	description = 'A bridge between WebGraph and Python/Jython',
	long_description ="""This package is intended as a simple bridge easing the usage of the
`WebGraph <http://webgraph.dsi.unimi.it/>`_ library in Python.

This software is hosted at `<https://github.com/mapio/py-web-graph>`_.

Given that the library is written in Java, some modules of this package must
be run with `Jython <http://www.jython.org/>`_, or a si milar Python
interpreter able to execute Java code. To reduce the impact of such
dependency, a basic XML-RPC server is provided to a llow any other Python
interpreter to access WebGraph data.

Finally, the package contains a simple wrapper for `Ubigraph
<http://ubietylab.net/ubigraph/>`_ (a free tool for visualizing dynamic
graphs) is provided, allowing some visual exploration of WebGraph data. """,
	author = 'Massimo Santini',
	author_email = 'santini@di.unimi.it',
	url = 'https://github.com/mapio/py-web-graph',
	packages = [ 'pywebgraph', 'pywebgraph.examples', 'pywebgraph.webgraph' ],
	platforms = [ 'MacOS X', 'POSIX' ],
	license = 'GNU General Public License (GPL)',
	data_files = [ ( 'docs', [ 'COPYING', 'README.md' ] ) ]
)
