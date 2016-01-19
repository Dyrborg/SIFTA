import sys
import os
import random
from collections import *
from graphviz import Digraph
from class_definitions import *

from sets import Set #for filtering
from itertools import ifilter


class GraphFlow:
    def __init__(self, edges, pcs, mapping):
        self.edges = edges
        self.pcs = pcs
        self.mapping = mapping
 
    def __str__(self):
        nodeStr = ""
        appStr = ""
    
        for (index, (fromNode,toNode)) in enumerate(self.edges):
            nodeObject = self.mapping[toNode]

            if isinstance(nodeObject, Source):
                nodeStr += str(nodeObject).replace("\n", "").replace("Src ", "") + " --> "

            elif isinstance(nodeObject, Sink):
                nodeStr += str(nodeObject).replace("\n", "").replace("Sink ", "") + " "

            elif isinstance(nodeObject, Intent):
                #TODO add more properties
                type = "None"
                if len(nodeObject.intentDefinition.actions) > 0:
                    type = nodeObject.intentDefinition.actions[0]
                nodeStr += "Intent(" + type + ") --> "

            elif isinstance(nodeObject, IntentResult):
                #TODO add more properties
                nodeStr += "IntentResult --> "
        for pc in self.pcs:
            appStr += "|".join(pc) + ","

        return "Flow: " + nodeStr + "in apps (" + appStr[:-1] + ")"


graph = Graph()
graph.load()

#breakOffFlowCount= 1000000 # break after many flows found (probably too many then)
breakOffFlowCount= 3000000 # break after many flows found (probably too many then)

algorithm = "extended"
outputseverity = 0

pcapps = set()

edgeCount = dict()

for (hash, apps) in graph.edges.iteritems():
    for app in apps:
        if app not in edgeCount:
            edgeCount[app] = 0
        edgeCount[app] += 1


appsToIgnore = set()


for (app, count) in edgeCount.iteritems():
    if count > 1000000:
        appsToIgnore.add(app)

allFlows = set()
flowCount = 0

print "apps to ignore: %i" % len(appsToIgnore)

severityList = dict()
severityList["Sink:<android.util.Log: int e(java.lang.String,java.lang.String)>"] = 3
severityList["Sink:<android.util.Log: int v(java.lang.String,java.lang.String)>"] = 3
severityList["Sink:<android.os.Bundle: void putLongArray(java.lang.String,long[])>"] = 3
severityList["Sink:<android.telephony.SmsManager: void sendMultipartTextMessage(java.lang.String,java.lang.String,java.util.ArrayList,java.util.ArrayList,java.util.ArrayList)>"] = 3
severityList["Sink:<android.media.MediaRecorder: void setVideoSource(int)>"] = 3
severityList["Sink:<android.util.Log: int i(java.lang.String,java.lang.String)>"] = 3
severityList["Sink:<android.os.Handler: boolean sendMessage(android.os.Message)>"] = 3
severityList["Sink:<android.util.Log: int d(java.lang.String,java.lang.String)>"] = 3
severityList["Sink:<java.net.URL: void <init>(java.lang.String)>"] = 3
severityList["Sink:<org.apache.http.client.HttpClient: org.apache.http.HttpResponse execute(org.apache.http.client.methods.HttpUriRequest)>"] = 3
severityList["Sink:<android.content.ContentResolver: int update(android.net.Uri,android.content.ContentValues,java.lang.String,java.lang.String[])>"] = 3
severityList["Sink:<org.apache.http.message.BasicNameValuePair: void <init>(java.lang.String,java.lang.String)>"] = 3
severityList["Sink:<java.io.OutputStream: void write(byte[])>"] = 3
severityList["Sink:<android.content.ContentResolver: android.net.Uri insert(android.net.Uri,android.content.ContentValues)>"] = 3
severityList["Sink:<android.util.Log: int w(java.lang.String,java.lang.String)>"] = 3
severityList["Sink:<android.media.MediaRecorder: void setPreviewDisplay(android.view.Surface)>"] = 3
severityList["Sink:<org.apache.http.impl.client.AbstractHttpClient: org.apache.http.HttpResponse execute(org.apache.http.client.methods.HttpUriRequest)>"] = 3
severityList["Sink:<android.telephony.SmsManager: void sendTextMessage(java.lang.String,java.lang.String,java.lang.String,android.app.PendingIntent,android.app.PendingIntent)>"] = 3
severityList["Sink:<android.os.Bundle: void putParcelable(java.lang.String,android.os.Parcelable)>"] = 3
severityList["Sink:<android.content.ContentResolver: int delete(android.net.Uri,java.lang.String,java.lang.String[])>"] = 3
severityList["Sink:<java.io.FileOutputStream: void write(byte[])>"] = 3
severityList["Sink:<java.io.Writer: void write(java.lang.String)>"] = 3

severityList["Src: <android.net.wifi.WifiInfo: java.lang.String getSSID()>"] = 3
severityList["Src: <org.apache.http.HttpResponse: org.apache.http.HttpEntity getEntity()>"] = 3
severityList["Src: <android.location.LocationManager: android.location.Location getLastKnownLocation(java.lang.String)>"] = 3
severityList["Src: <java.util.Calendar: java.util.TimeZone getTimeZone()>"] = 3
severityList["Src: <android.location.Location: double getLatitude()>"] = 3
severityList["Src: <android.bluetooth.BluetoothAdapter: java.lang.String getAddress()>"] = 3
severityList["Src: <android.database.Cursor: java.lang.String getString(int)>"] = 3
severityList["Src: <java.net.URLConnection: java.io.InputStream getInputStream()>"] = 3
severityList["Src: <android.accounts.AccountManager: android.accounts.Account[] getAccounts()>"] = 3
severityList["Src: <android.location.Location: double getLongitude()>"] = 3
severityList["Src: <android.content.ContentResolver: android.database.Cursor query(android.net.Uri,java.lang.String[],java.lang.String,java.lang.String[],java.lang.String)>"] = 3
severityList["Src: <android.content.pm.PackageManager: java.util.List getInstalledApplications(int)>"] = 3
severityList["Src: <android.telephony.TelephonyManager: java.lang.String getSimSerialNumber()>"] = 3
severityList["Src: <android.telephony.TelephonyManager: java.lang.String getDeviceId()>"] = 3
severityList["Src: <android.media.AudioRecord: int read(short[],int,int)>"] = 3
severityList["Src: <android.content.pm.PackageManager: java.util.List queryContentProviders(java.lang.String,int,int)>"] = 3
severityList["Src: <android.telephony.gsm.GsmCellLocation: int getCid()>"] = 3
severityList["Src: <android.telephony.TelephonyManager: java.lang.String getSubscriberId()>"] = 3
severityList["Src: <android.content.pm.PackageManager: java.util.List getInstalledPackages(int)>"] = 3
severityList["Src: <android.os.Handler: android.os.Message obtainMessage(int,java.lang.Object)>"] = 3
severityList["Src: <android.telephony.TelephonyManager: java.lang.String getLine1Number()>"] = 3
severityList["Src: <java.util.Locale: java.lang.String getCountry()>"] = 3
severityList["Src: <android.telephony.gsm.GsmCellLocation: int getLac()>"] = 3


sinks = set()
visitedEdges = set()

def traverse(nodeHash, flow):
    global flowCount
    children = graph.nodes[nodeHash]

   # if len(children) > 50:
   #     print len(children)
   #     children = set(list(children)[0:50])


    for child in children:
        # We have problems with IntentResults, so lets ignore them
        if isinstance(graph.hashToObjectMapping[child], IntentResult):
            continue

        #We want to ignore flows, where an app have more than a 100 flows (we have the list of apps in appsToIgnore)
        appsOnEdge = graph.edges[nodeHash,child]

        pcTRUE = False

        # Presence condition
        if len(pcapps) != 0:
            for app in appsOnEdge:
                if app in pcapps:
                    pcTRUE = True
                    break
        else:
            pcTRUE = True

        if algorithm == "extended":
            if (nodeHash,child) in flow.edges or not pcTRUE:
                continue

        else:
            if (nodeHash,child) in visitedEdges or not pcTRUE:
                continue
            visitedEdges.add((nodeHash,child))

        newFlow = GraphFlow(flow.edges[:], flow.pcs[:], graph.hashToObjectMapping)
        newFlow.edges.append((nodeHash, child))
        newFlow.pcs.append(appsOnEdge)

        datObject = graph.hashToObjectMapping[child]
        if isinstance(datObject, Sink):# or (graph.hashToObjectMapping[newFlow.edges[0][1]].method in severityList and isinstance(graph.hashToObjectMapping[newFlow.edges[1][1]], Intent)):

            # We dont want to look at Src --> Snk flows
          #  if len(newFlow.edges) == 2 and isinstance(graph.hashToObjectMapping[newFlow.edges[1][1]], Sink):
          #      continue


#            sinks.add(datObject.method)

            #if datObject.method not in importantSinks :
            #    continue

            allFlows.add(newFlow)
            flowCount = flowCount + 1

            if flowCount % 10000 == 0:
                sys.stderr.write("\rFlow count: %i" % flowCount)
                sys.stderr.flush()
        else:
            if (flowCount > breakOffFlowCount):
                print ("more than %i flows. breaking off!" % breakOffFlowCount)
                return
            #print "down the rabithole we go! (flowlength: " + str(len(newFlow)) + ")"
            if (child in graph.nodes): #child has other children
                traverse(child, newFlow)


sys.stderr.write("Finding flows\n")
nodeCount = len(graph.sources)

def getColor(datString):
    if datString.startswith("Sink"):
        return "red"

    if datString.startswith("Src"):
        return "green"

    return ""

def drawGraph():
    seenBefore = set()
    seenEdges  = set()
    dot = Digraph(comment="Graph")
    print "FLOWS FOUND: " + str(len(allFlows))
    
    largestPCsize=0
    edgeWithlargestPCsize=None

    for flow in allFlows:
        edges = flow.edges

        for (fromHash, toHash) in edges:
            simp = str(graph.hashToObjectMapping[toHash])
            if simp not in seenBefore:
                color = getColor(simp)
                dot.node(simp, simp, color = color)
                seenBefore.add(simp)

            if fromHash == None:
                continue

            esimp = str(graph.hashToObjectMapping[fromHash])
            if esimp not in seenBefore:
                color = getColor(esimp)
                dot.node(esimp,esimp, color = color, constraint= False)
                seenBefore.add(esimp)
            try:
                if (fromHash, toHash) not in seenEdges:
                    numApps = len(graph.edges[fromHash,toHash])
                    if (numApps > largestPCsize):
                        largestPCsize=numApps
                        edgeWithlargestPCsize=(graph.hashToObjectMapping[fromHash],graph.hashToObjectMapping[toHash])
                    dot.edge(esimp,simp, label= "apps: " + str(numApps)) #+ ",\n".join([e.split(".")[-1] for e in list(graph.edges[fromHash,toHash])]))#
                    seenEdges.add((fromHash, toHash))
            except:
                pass
            before = hash
    print "Nodes in flows: %i" % len(seenBefore)
    print "Edges in flows: %i" % len(seenEdges)
    if (largestPCsize>0):
        print "Largest PC Size: %i" % largestPCsize
        print "on Edge: " + str(edgeWithlargestPCsize[0]) + str(edgeWithlargestPCsize[1])
    dot.render("sifta-graph.gv", view=False)
    print "ALL DONE"


def printFlowDetails(flows):
    flowlengths = dict()

    #Dangerous
    print "High severity flows:"
    for flow in flows:
        (fromEdge, toEdge) = flow.edges[0]
        source = graph.hashToObjectMapping[toEdge]

        severity = severityList.get(source.method, -1)

        if severity == 3:
            print flow

    if outputseverity != 2:
        #Medium
        print "Medium severity flows:"
        for flow in flows:
            (fromEdge, toEdge) = flow.edges[0]
            source = graph.hashToObjectMapping[toEdge]

            severity = severityList.get(source.method, -1)

            if severity == 2:
                print flow

    if outputseverity == 0:
        #Low
        print "Low severity flows:"
        for flow in flows:
            (fromEdge, toEdge) = flow.edges[0]
            source = graph.hashToObjectMapping[toEdge]

            severity = severityList.get(source.method, -1)

            if severity == 1:
                print flow

    #Unknown
    print "Unknown severity flows:"
    for flow in flows:
        (fromEdge, toEdge) = flow.edges[0]
        source = graph.hashToObjectMapping[toEdge]

        severity = severityList.get(source.method, -1)

        if severity < 1:
            print flow


    for flow in flows:
        datLength = len(flow.edges)
        if datLength not in flowlengths:
            flowlengths[datLength] = 0
        flowlengths[datLength] += 1


    for (key, value) in flowlengths.iteritems():
        print "flows of length %i exists %i times" % (key, value)

    flowLengths = [len(i.edges) for i in flows]
    flowcountlength = len(flowLengths)

    totallength = float(sum(flowLengths))

    if flowcountlength != 0:
        print "Average flow length: %f" % (float(totallength / flowcountlength))
    else:
        print "Average flow length: NONE"

def printFirstFlowWithLen(flows, length):
    for flow in allFlows:
        datLength = len(flow.edges)
        if (datLength == length):
            print "first flow with length %i :\n" % length
            print flow
            break

def appStatistics(flows):
    print "App Stats:"
    occurrencesPerApp=dict()
    intermediaryApps=set() # apps that receive and intent and send an intent (can be used for info forwarding)
    for flow in allFlows:
        #get intermediary
        if (len(flow.pcs) > 2):
            for pc in flow.pcs[1:-1]: # all pcs but the first and last one
                for appId in pc:
                    intermediaryApps.add(appId)
        #get occurrances
        appsInPath=set()
        for pc in flow.pcs:
            for appId in pc:
                appsInPath.add(appId)
        for app in appsInPath:
            if app not in occurrencesPerApp:
                occurrencesPerApp[app] = 0
            occurrencesPerApp[app] += 1
    sortedOccurrences=sorted(occurrencesPerApp, key=occurrencesPerApp.get, reverse=True)
    
    print "Rank\t App ID\t Occurrences in Flows"
    for x in range(0,10):
        print x, "\t", sortedOccurrences[x], "\t", occurrencesPerApp[sortedOccurrences[x]]
    print "Total number of apps in pcs: ", len(occurrencesPerApp)
    appStatsFile = open("appOccurrences.csv", "w+")
    appStatsFile.write("AppID\tOccurrencesInFlows\n")
    for app in sortedOccurrences:
        appStatsFile.write(app + "\t" + str(occurrencesPerApp[app]) + "\n")
    appStatsFile.close()
    
    print "Total number intermediary apps: ", len(intermediaryApps)
    intermAppStatsFile = open("intermediaryApps.csv", "w+")
    intermAppStatsFile.write("AppID\n")
    for app in intermediaryApps:
        intermAppStatsFile.write(app + "\n")
    intermAppStatsFile.close()
    

def printFlowLengthsDetailsReturnMax(flows):
    flowlengths = dict()
    maxLen = 0
    for flow in allFlows:
        datLength = len(flow.edges)
        if datLength not in flowlengths:
            flowlengths[datLength] = 0
        flowlengths[datLength] += 1
        if datLength > maxLen:
            maxLen=datLength

    for (key, value) in flowlengths.iteritems():
        print "flows of length %i exists %i times" % (key, value)

    return maxLen

def printFlows(flows):
    print "-------- INTERNAL FLOWS ---------"
    for flow in allFlows:
        if len(flow) != 2:
            continue
        print "------------------------------"
        for hash in flow:
            realObject = graph.hashToObjectMapping[hash]

            if isinstance(realObject, Sink):
                print "" + str(realObject).replace(" \n", ": ")
            else:
                print "" + str(realObject).replace(" \n", ": ") + "\n--> (" + ",".join(graph.edges[(hash, flow[1])]) + ")"

    print "-----------------------------------"

    print "------------ INTER APP FLOWS -------------"

    for flow in allFlows:
        if len(flow) == 2:
            continue
        print "------------------------------"
        i = 0
        for hash in flow:
            realObject = graph.hashToObjectMapping[hash]

            if isinstance(realObject, Sink):
                print str(realObject)
            else:
                print str(realObject) + "\n--> (" + ",".join(graph.edges[(hash, flow[i + 1])]) + ")"
            i += 1


def printSpecificEdgeStats():
    fromHash="fbc53f89072658fdc7da80d942bdfde9"
    toHash="da18b05c673b837a26e56acbbd4f7f5e"
    if (graph.edges[fromHash,toHash]) :
        print "edge %s to %s exists\n"%(fromHash,toHash)
        print "From %s\n"%graph.hashToObjectMapping[fromHash]
        print "To %s\n"%graph.hashToObjectMapping[toHash]
        print "Apps %s\n"%graph.edges[fromHash,toHash]
    
def printSpecificAppStats():
	#searchApp="com.merunetworks.IdentityWifi" ##com.merunetworks.
	#searchApp="air.com.doitflash.ar.atelier"
	searchApp="com.nixpa.kik.sketchee"
	
	print "\n%s on graph edges: " % searchApp
	for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
		if searchApp in apps:
			fromObj = graph.hashToObjectMapping[hashFrom]
			toObj = graph.hashToObjectMapping[hashTo]
			print (searchApp, " in ", fromObj.__str__(),  "app:", fromObj.app, " to ", toObj.__str__(), "app:", toObj.app, "\n")
	print "\n%s on graph nodes: " % searchApp
	for node in graph.nodes:
		nodeObj = graph.hashToObjectMapping[node]
		#if isinstance(nodeObj, Source):
			#
		#elif isinstance(nodeObj, Sink):
			#
		if isinstance(nodeObj, Intent):
			if nodeObj.app == searchApp : #"com.rekonsult.MTFashionAlert" :
				print nodeObj
		elif isinstance(nodeObj, IntentResult):
			if nodeObj.app == searchApp :
				print nodeObj
	print "\n"
	
def printSpecificNodeStats():
	searchHash="0b49a5484aabba98d1bef07f8f30ba59"
	if searchHash in graph.nodes.keys(): print "HASH is in graph.nodes"
	else: print "HASH is NOT in graph.nodes"
	nodeObj = graph.hashToObjectMapping[searchHash]
	if (nodeObj) :
		print "Node %s:\n %s\n" %(searchHash, nodeObj.__str__())
		incoming=list()
		outgoing=list()
		for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
			if hashFrom==searchHash:
				outgoing.append(((hashFrom,hashTo), apps))
			if hashTo==searchHash:
				incoming.append(((hashFrom,hashTo), apps))
		print "Incoming Edges (%d)\n"%len(incoming)
		for ((hashFrom,hashTo), apps) in incoming:
			fromObj = graph.hashToObjectMapping[hashFrom]
			print ("From: %s, hash:%s  app: %s\n"%(fromObj.__str__(),hashFrom, apps))
		print "Outgoing Edges (%d)\n"%len(outgoing)
		for ((hashFrom,hashTo), apps) in outgoing:
			toObj = graph.hashToObjectMapping[hashTo]
			print ("To: %s, hash:%s  app: %s\n"%(toObj.__str__(),hashTo, apps))
		print "\n"
	else: print "Hash %s not found"%searchHash
	

def checkNoEmptyEdges():
	for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
		if not apps : #apps is empty
			fromObj = graph.hashToObjectMapping[hashFrom]
			toObj = graph.hashToObjectMapping[hashTo]
			print "Empty Edge from %s \nto%s"%(fromObj.__str__(),toObj.__str__())
	print "\n"
	
def checkNodeApps():
	for node in graph.nodes:
		nodeObj = graph.hashToObjectMapping[node]
		#if isinstance(nodeObj, Source):
			#
		#elif isinstance(nodeObj, Sink):
			#
		if isinstance(nodeObj, Intent): ## assumption: app should be on incoming
			incoming=set()
			outgoing=set()
			for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
				if hashTo == node : incoming = incoming.union(apps)
				if hashFrom == node : outgoing = outgoing.union(apps)
			if (not (nodeObj.app in incoming)):
				print "Intent node; app %s not on incoming HASH: %s \n" % (nodeObj.app , node)
				print " incoming apps: %s\n" % incoming
				print " outgoing apps: %s\n" % outgoing
		elif isinstance(nodeObj, IntentResult):
			incoming=set()
			outgoing=set()
			for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
				if hashTo == node : incoming = incoming.union(apps)
				if hashFrom == node : outgoing = outgoing.union(apps)
			if (not (nodeObj.app in incoming)):
				print "IntentResult node; app %s not on incoming HASH: %s \n" % (nodeObj.app , node)
				print " incoming apps: %s\n" % incoming
				print " outgoing apps: %s\n" % outgoing
		#elif isinstance(nodeObj, IntentFilter):
			#print "IntentFilter node with app %s\n" % nodeObj.app
			#for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
				#if hashTo == node :
					#print " incoming apps: %s\n" % apps 
				#if hashFrom == node :
					#print " outgoing apps: %s\n" % apps 
	print "\n"

def countBarbells(): # count how many of these constructs are in the graph: 0-0 (two nodes, connected by one edge but without connections to the rest of the graph; looks like a barbell)
	count=0
	for node in graph.nodes:
		nodeObj = graph.hashToObjectMapping[node]
		incoming=0
		invalid = 0
		if not isinstance(nodeObj,Source):
			nextHasOutgoing=0
			for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
				if hashTo == node : incoming+=1
				if hashFrom == node :
						nextNodeObj = graph.hashToObjectMapping[node]
						if not isinstance(nodeObj,Sink):
							for ((hashFrom2,hashTo2), apps) in graph.edges.iteritems():
								if (hashFrom2 == hashTo):
									nextHasOutgoing+=1
						else: invalid=1
		else: invalid=1
		if invalid==0 and incoming==0 and nextHasOutgoing==0:
			count+=1
	print "Barbells: %d" % count
		#elif isinstance(nodeObj, IntentResult):
			#print "IntentResult node with app %s\n" % nodeObj.app
			#for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
				#if hashTo == node :
					#print " incoming apps: %s\n" % apps 
				#if hashFrom == node :
					#print " outgoing apps: %s\n" % apps 
		#elif isinstance(nodeObj, IntentFilter):
			#print "IntentFilter node with app %s\n" % nodeObj.app
			#for ((hashFrom,hashTo), apps) in graph.edges.iteritems():
				#if hashTo == node :
					#print " incoming apps: %s\n" % apps 
				#if hashFrom == node :
					#print " outgoing apps: %s\n" % apps 
	print "\n"

def main(args):
    global pcapps
    global outputseverity
    global algorithm

    prevarg = ""
    for arg in args:

        if prevarg == "-top":
            cap = int(arg)
            pcapps = list(graph.processedApps)[0:cap]
        if prevarg == "-applist":
            pcapps = set(arg.split(","))

        if prevarg == "-severity":
            outputseverity = int(arg)

        if prevarg == "-pathalgorithm":
            algorithm = arg
        prevarg = arg

    printAllFlows=False
    printStatistics=False
    printSampleFlows=False
    printAppStatistics=False
    arguments=sys.argv
    if (len(arguments[1:]) > 0):
        if "-printAllFlows" in arguments:
            print("Printing all flows.")
            printAllFlows=True
        if "-printSampleFlows" in arguments:
            print("Printing a sample of the flows (100 flows with length > 2).")
            printSampleFlows=True
        if "-printStatistics" in arguments:
            print("Printing statistics.")
            printStatistics=True
        if "-printAppStats" in arguments:
            print("Printing app statistics.")
            printAppStatistics=True
    if not printAllFlows:
        print("Printing only one flow of max. found length. Use -printAllFlows to print all.")
    if not printStatistics:
        print("Omitting graph statistics. Use -printStatistics to print them.")
        
    print "Running querier with algorithm: %s" % algorithm

    #printSpecificEdgeStats()
    #printSpecificAppStats()
    #printSpecificNodeStats()
    #checkNodeApps()
    #countBarbells()
    #checkNoEmptyEdges()
    
    #return
    
    print ("Graph: %s nodes, %s edges"%(len(graph.nodes), len(graph.edges)))
    '''
    nodesFile = open("nodes.txt", 'w')
    for node in sorted(graph.nodes):
        nodesFile.write("Node %s: %s\n"%(node,graph.hashToObjectMapping[node]))
    nodesFile.close()
    edgesFile = open("edges.txt", 'w')
    for (fromhash,tohash) in sorted(graph.edges) :
        edgesFile.write("Edge %s to %s\n"%(fromhash,tohash))
    edgesFile.close()
    '''

    for node in graph.sources:
        global visitedEdges
        visitedEdges = set()
        if (not node in graph.nodes): #source has children
            print ("source is not key in graph.nodes list?!: " + node)
        else:
            traverse(node, GraphFlow([(None,node)], [], graph.hashToObjectMapping))
        if (flowCount > breakOffFlowCount):
            print ("more than %i flows. breaking off!" % breakOffFlowCount)
            break
        

    
    if len(allFlows)==0:
        print("0 flows found!")
    else:
        if printSampleFlows:
            print("computing sample")
            sample = random.sample(Set(ifilter(lambda flow: len(flow.edges) > 2 , allFlows)), 10) # 100 flows with more than 2 nodes
            print("printing sample")
            printFlowDetails(sample)
        if printAllFlows:
            printFlowDetails(allFlows)
        maxLen=printFlowLengthsDetailsReturnMax(allFlows)
        printFirstFlowWithLen(allFlows, maxLen)
        if printAppStatistics:
            appStatistics(allFlows)
        if printStatistics:
            graph.printAllStatistics()
        #graph.drawGraph()
        drawGraph()

main(sys.argv)
