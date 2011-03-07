#!/usr/bin/python
#
# Joe Conlin <joe@joeconlin.org>
# http://joeconlin.org
#
# Asynchronous DNS RBL Recon Tool v0.2 
# Proof of Concept

from async_dns import AsyncResolver
import os, sys
from netaddr import *

# put your CIDR blocks here
MY_BLOCKS = ['66.203.68.0/24', '68.171.128.0/20',]

#add or subtract your dnsrbls here
MY_RBLS = ['cbl.abuseat.org', 'b.barracudacentral.org','zen.spamhaus.org','xbl.spamhaus.org', 'sbl.spamhaus.org', 'dnsbl.sorbs.net', 'web.dnsbl.sorbs.net', 'all.spamrats.com', 'spam.dnsbl.sorbs.net', 'psbl.surriel.com', 'dun.dnsrbl.net', 'dnsbl.njabl.org', 'bl.spamcop.net', 'dnsbl-1.uceprotect.net', 'dnsbl-2.uceprotect.net', 'dnsbl-3.uceprotect.net']

hosts = []

def classDnets(ipnetwork):
        subnets = list(ipnetwork.subnet(32))
        return subnets

def rblName(classC, rbl):
    octa = classC.ip.words[0]
    octb = classC.ip.words[1]
    octc = classC.ip.words[2]
    octd = classC.ip.words[3]
    rblq = "%s.%s.%s.%s.%s" % (octd,octc,octb,octa,rbl)
    return rblq
print "Using %s RBLs" % (len(MY_RBLS))

for rbl in MY_RBLS:
    print "generating queries for %s" % (rbl)
    for ipnet in MY_BLOCKS:
        ipnet = IPNetwork(ipnet)
        for classC in classDnets(ipnet):
          hosts.append(rblName(classC, rbl))

#hosts = open("domains.txt", "r").read().splitlines()
number_of_hosts = len(hosts)

print "We have %s queries to make..." % (number_of_hosts)
s = raw_input('Hit any key to begin or Ctrl-C to escape ')

ar = AsyncResolver(hosts)
resolved = ar.resolve()

bad_hosts = []

for host, ip in resolved.items():
  if ip is None:
#    print "%s could not be resolved." % host
    pass
  else:
#    print "%s resolved to %s" % (host, ip)
    host = host.split(".")
    # get the blacklist name
    blacklist = host[4:]
    #get the hostname (must reverse it)
    host = host[:4]
    host.reverse()
    #join them together
    h = ".".join(host)
    b = ".".join(blacklist)
    bad_hosts.append((h,b,ip))

num_bad_hosts = len(bad_hosts)
bad_hosts.sort()

f = open('output.csv','w')
f.write("host,blacklist,code\n")
print "Number of listings: %s" % (num_bad_hosts)

for host,blacklist,ip in bad_hosts:
    line = "%s,%s,%s\n" % (host,blacklist,ip)
    f.write(line)
    print "%s\t%s\t%s" % (host,blacklist,ip)
f.close()

