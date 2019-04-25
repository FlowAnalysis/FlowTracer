# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:33:39 2018

@author: Heyang
"""

from scapy.all import *
import time
import os
import json


def find_file(dir,tmp):
    '''search latest file'''
    file_lists = os.listdir(dir)
    if len(file_lists) == 0:
        return 'no files'
    file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn)
                    if not os.path.isdir(dir + "\\" + fn) else 0)
    
    for i in file_lists:
        fp= os.path.join(dir, i)
        if fp == tmp:
            os.remove(fp)           
        elif i.split('.')[-1] == 'pcap':
            return fp
    return 'no logs'            

def pickhead(pkt):

    #print(pkt[IP].tos)
    if pkt[IP].tos == 4:        
        head = pkt[Dot1Q].vlan
        tail = 'h2'
        dst = pkt[IP].ttl
    else:
        head = pkt[Dot1Q][1].vlan
        tail = pkt[Dot1Q][0].vlan
        dst = pkt[IP].ttl
    tuple = [head,tail,dst]
    return tuple

def tolist(d,f,pd,dst):
    l = []
    for i in d:
        r = {}
        r['src_ip'] = i
        r['dst_ip'] = dst
        r['bytes'] = f[i]
        link_id = []
        for j in sorted(d[i].keys(),reverse=1):
            #print(d[i][j])
            #print(pd[d[i][j]])
            link_id.append(str(pd[d[i][j]]))
            
        r['link_id'] = link_id
        path_id = ''
        for k in link_id:
            if k == 'end':
                path_id = path_id + k
            else:
                path_id = path_id + k + '-'
        r['path_id'] = path_id
        l.append(r)
    return l 
    
    
if __name__=="__main__":
    dst = '10.0.0.2'
    tmp=''
    dir = 'C:\\Users\\Heyang\\Spyder\\elk\\pcap'
    pathdict={(1,2):1,(2,3):2,(3,4):3,(4,'h2'):'end'}  

    while 1:
        time.sleep(5)
        f = find_file(dir,tmp)
        if f.split('.')[-1] != 'pcap':
            print("no file")
            tmp = ''
            continue
        else:
            tmp = f           
        pcaps = rdpcap(f)
        flow = {}
        flow_c = {}     
        for pkt in pcaps:
            if pkt.haslayer(IP) == 0:
                continue
            src = pkt[IP].src          
            flow_c[src] = flow_c.setdefault(src,0) + len(pkt)            
            if pkt.haslayer(Dot1Q) == 0:
                continue
            else:                
                tuple = pickhead(pkt)
                flow.setdefault(src,{})[tuple[2]]=(tuple[0],tuple[1])

                
        print(flow)
        print(flow_c)
        l = tolist(flow,flow_c,pathdict,dst)  
        with open("pathinfo.json","w") as f:
            json.dump(l,f)
            print("file written")
        


            
    
            
        
        
