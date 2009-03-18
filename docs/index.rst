Welcome to pyWebGraph's documentation!
======================================

This package is intended as a simple bridge easing the usage of the `WebGraph <http://webgraph.dsi.unimi.it/>`_ library in Python.

Given that the library is written in Java, some modules of this package must be run with `Jython <http://www.jython.org/>`_, or a similar Python interpreter able to execute Java code. To reduce the impact of such dependency, a basic XML-RPC server is provided to allow any other Python interpreter to access WebGraph data.

Finally, the package contains a simple wrapper for `Ubigraph <http://ubietylab.net/ubigraph/>`_ (a free tool for visualizing dynamic graphs) is provided, allowing some visual exploration of WebGraph data.


This documentation includes:

.. toctree::
   :maxdepth: 2

   quickstart/index
   modules/index  
  
  
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

