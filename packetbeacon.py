#!/usr/bin/env python
#
# packetbeacon.py - Monitor network interface for potentially insecure packets
#
#
# Author: Patrick F. Wilbur (pdub.net)
#
# Copyright 2019 Patrick F. Wilbur. All Rights Reserved.
#


import dpkt
import pcap
from socket import *
import sys

##### CONFIG #####
broadcast = None
#broadcast = ("192.168.255.255",13337) # Allows you to remotely monitor status (see /monitors)
### END CONFIG ###


ip_count = 0
tcp_count = 0
udp_count = 0
ip_stats = {}
ip_stats["tcp"] = {}
ip_stats["udp"] = {}
ip_stats["http"] = {}
s = None

def handler(ts,pkt,*d):
    global ip_count,tcp_count,udp_count,ip_stats,s
    try:
        eth = dpkt.ethernet.Ethernet(pkt)
        if isinstance(eth.data, dpkt.ip.IP):
            ip = eth.data
            if isinstance(ip.data, dpkt.tcp.TCP):
                tcp_count+=1
                tcp = ip.data
                sport = tcp.sport
                dport = tcp.dport
                proto = "tcp"
            elif isinstance(ip.data, dpkt.udp.UDP):
                udp_count+=1
                udp = ip.data
                sport = udp.sport
                dport = udp.dport
                proto = "udp"
            else:
                #print("other IP")
                return                
            port = min(sport,dport)
            if port == 80:
                if broadcast != None:
                    s.sendto(proto + "\t" + str(sport) + "\t" + str(dport) + "\n", broadcast)
                print("* Potentially unsafe activity detected on Port 80! *")
            if port < 10000:
                if port not in ip_stats[proto]:
                    ip_stats[proto][port] = 1
                else:
                    ip_stats[proto][port] += 1
                ip_count+=1
        else:
            #print("other ethernet")
            pass
    except:
        #print("strange packet exception occurred")
        pass

def main():
    global s
    if broadcast != None:
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    pc = pcap.pcap(name=sys.argv[1])
    pc.setfilter('')
    print('Now listening')
    try:
        pc.loop(0,handler)
    except KeyboardInterrupt:
        pass
    print('')
    print('Totals:')
    for j in ip_stats:
        for k in ip_stats[j]:
            print(str(j)+"\t"+str(k)+"\t"+str(ip_stats[j][k])+"\t" + str(float((ip_stats[j][k])/float(ip_count))*float(100)))
    print(ip_count)


if __name__ == "__main__":
    main()
