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
import graph_generation_lib


inputFolder=sys.argv[1]
print "loading graph generation input files from folder " + str(inputFolder)

fileList=[]
'''
Files are loaded if files with the same prefix and endings
.epicc ,
.fd.xml , and
.manifest.xml
exist.
'''
for fileName in os.listdir(inputFolder):
    if fileName.endswith(".epicc"):
        basename=fileName[:-len(".epicc")]
        manifestFileName=basename+".manifest.xml"
        fdFileName=basename+".fd.xml"
        if (os.path.isfile(fdFileName) and os.path.isfile(manifestFileName)):
            fileList.append(fileName)
            fileList.append(manifestFileName)
            fileList.append(fdFileName)
            
#flowSolver = FlowSolver(sys.argv)
flowSolver = graph_generation_lib.FlowSolver(fileList)
graphBuilder = graph_generation_lib.GraphBuilder([], flowSolver)
graph = graphBuilder.createGraph()

print "Number of failed apps: " + str(flowSolver.errorcount)

'''
Niklas: all Sources are private and contain sensitive information in some way.
The taintpropagation will be done after "graph.save()". However we will probably
structure this a little differently with all the graph construction code in one file
and the taint analysis / graph querying in another. Since we are now persisting the
graph, it is possible to load only that (and not redo graph construction) to get the
tainted flows.
'''
graph.save()
