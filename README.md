A simple package allowing to use [WebGraph](http://webgraph.di.unimi.it/) data in Python (using the Jython interpreter).

The code in this project is based on

  * WebGraph 3.6.5
  * Python 2.7.16
  * Jython 2.7.2
  * Ubigraph 0.2.4alpha **no more available**

and has been tested on Mac OS X 10.13.6.

For details, please refer to the [documentation](http://mapio.github.io/py-web-graph/).

## Installation hint

To install the required jars run `./install_jars.sh` (it basically downloads the
*binary tarball* and *dependencies tarball* tarballs from the
[WebGraph](http://webgraph.di.unimi.it/) site and unpacks all the jars in the
`jars` directory); observe that the script refers to version `3.6.5` of WebGraph, in case of version changes just update the relevant line of the script.

Then create an `example.graph-txt` file containing a test graph (as per [ASCIIGraph](http://webgraph.di.unimi.it/docs/it/unimi/dsi/webgraph/ASCIIGraph.html) format), for instance

    3
    0 1 2
    2
    0

Now, running Jython as `jython -J-cp 'jars/*'` should work as follows

    Jython 2.7.2 (v2.7.2:925a3cc3b49d, Mar 21 2020, 10:03:58)
    [Java HotSpot(TM) 64-Bit Server VM (Oracle Corporation)] on java11.0.5
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from it.unimi.dsi.webgraph import ASCIIGraph
    >>> ASCIIGraph.load('example')
    Nodes: 3
    Arcs: 5
    Successors of 0 (degree 3): 0 1 2
    Successors of 1 (degree 1): 2
    Successors of 2 (degree 1): 0

Note the `-J-cp 'jars/*'` that sets the classpath to the directory where the jars have been unpacked.