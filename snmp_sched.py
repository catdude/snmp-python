#!/usr/bin/python

# SNMP poll scheduler, using usnmp and a single process
#

import pprint
import ujson
import time
from easysnmp import snmp_get, snmp_walk, Session
import easysnmp

deviceStr = '\n'.join(open('devices.json', 'r').readlines())
oidStr = '\n'.join(open('oids.json', 'r').readlines())

devices = ujson.loads(deviceStr)
oids = ujson.loads(oidStr)

snmpTimeout = 2

start = time.time()

queryDict = {}

for o in oids['OIDs']:
	devClass = o['class']
	oList = o['OIDlist']
	queryDict[devClass] = []
	for oid in oList:
		oidName = oid['name']
		oidNum = oid['oid']
		queryDict[devClass].append(oidNum)

for device in devices['devices']:
	ipAddr = device['ip']
	name = device['name']
	devClass = device['type']
	community = device['rocomm']
	try:
		session = Session(hostname=ipAddr, community=community, version=2, timeout=snmpTimeout, retries=0)
		#print "Device %s (%s) will poll oids %s" % (name, ipAddr, queryDict[devClass])
		for o in queryDict[devClass]:
			x= session.walk(o)
			for val in x:
				#print "%s: %s" % (val.oid_index, val.value)
				pass
	except easysnmp.EasySNMPTimeoutError, e:
		print "Device %s (%s) timed out when requesting oid %s" % (name, ipAddr, o)
	except easysnmp.EasySNMPError, e:
		print "Non-timeout error from %s (%s) for oid %s" % (name, ipAddr, o)

#print "OIDs:"
#pprint.pprint(queryDict)

end = time.time()

print "Elapsed time was %d seconds" % (end - start)

#[root@watcher snmp-python]# python snmp_sched.py 
#Device cs05-a.us (192.168.100.15) timed out when requesting oid .1.3.6.1.2.1.31.1.1.1.6
#Device cs05-b.us (192.168.100.25) timed out when requesting oid .1.3.6.1.2.1.31.1.1.1.6
#Elapsed time was 7 seconds
#[root@watcher snmp-python]# 
