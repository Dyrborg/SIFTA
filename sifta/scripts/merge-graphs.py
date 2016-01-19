#       IntentDefinition(String[] actions, String[] category, String mimeType, String data, String packageName)
#
#		Intent(IntentDefinition intentDef, String component, String app)
#	    IntentFilter(IntentDefinition intentDef, String component, Int priority, String app)
#		IntentResult(Intent intent, String app) evt from and to?
#		Source(String app, String method)
#		Sink(String app, String method)
#
#		Flow(Object sender, Object reciever)
#

from collections import *
from collections import OrderedDict
from epicc_parser import parse_epicc
from class_definitions import *
import copy
#from graph_generation_lib import FlowSolver, GraphBuilder
import graph_generation_lib

script_path = os.path.dirname(os.path.realpath(__file__))
android_pfx = "{http://schemas.android.com/apk/res/android}"

INTENT = 0
INTENT_RESULT = 1

FlowdroidElement = namedtuple("FlowdroidElement", ["componentType", "component", "intentId", "type"])

graph = Graph()

arguments=sys.argv[1:]

flowSolver = graph_generation_lib.FlowSolver(list())

for dirname in arguments :
	if not dirname.endswith("/") :dirname = dirname + "/"
	print "loading graph files from folder " + str(dirname)
	files = os.listdir(dirname)
	graph.loadFromDir(dirname)


graphBuilder = graph_generation_lib.GraphBuilder([], flowSolver)
graph = graphBuilder.createGraph()
graph.save()
