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