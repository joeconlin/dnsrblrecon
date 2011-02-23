#!/usr/bin/python
#
# Joe Conlin <joe@joeconlin.org>
# http://joeconlin.org
#
# Asynchronous DNS RBL Recon Tool v0.1 
# Proof of Concept

from async_dns import AsyncResolver
import os, sys
from netaddr import *

MY_BLOCKS = ['66.203.64.0/19','68.171.128.0/20','69.26.96.0/19','69.147.160.0/19']
MY_RBLS = ['cbl.abuseat.org', 'b.barracudacentral.org']

hosts = []

def classDnets(ipnetwork):
        subnets = list(ipnetwork.subnet(32))
        return subnets

def rblName(classC, MY_RBLS):
    octa = classC.ip.words[0]
    octb = classC.ip.words[1]
    octc = classC.ip.words[2]
    octd = classC.ip.words[3]
    rblq = "%s.%s.%s.%s.%s\n" % (octd,octc,octb,octa,rbl)
    return rblq

for rbl in MY_RBLS:
    for ipnet in MY_BLOCKS:
	ipnet = IPNetwork(ipnet)
	for classC in classDnets(ipnet):
	  hosts.append(rblName(classC, rbl))
		
number_of_hosts = len(hosts)

print "We have %s queries to make..." % (number_of_hosts)
s = raw_input('You ready 4 dis? --> ')

ar = AsyncResolver(hosts)
resolved = ar.resolve()

for host, ip in resolved.items():
  if ip is None:
    pass
  else:
    print "%s resolved to %s" % (host, ip)

