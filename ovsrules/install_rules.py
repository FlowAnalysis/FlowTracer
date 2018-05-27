# -*- coding: utf-8 -*-
"""
Created on Thu May 24 17:21:31 2018

@author: Heyang
"""
import os
import json


def add_sw(file,slist):   
        priority=30
        p = 4             
        for s in slist:
            add_group_cmd="ovs-ofctl add-group "+s[0]+" group_id=1,type=select,selection_method=hash,fields'(nw_src,nw_dst,tcp_dst,tcp_src,dl_vlan,nw_ttl)',bucket=weight:4,push_vlan:0x8100,set_field:"+str(s[1]+4096)+"-\>vlan_vid,mod_nw_tos:"+str(p)+",normal,bucket=weight:"+str(10-p)+",dec_ttl,normal -O openflow15"                        
            file.write(add_group_cmd+"\n")
        for s in slist:
            add_flow_cmd="ovs-ofctl add-flow "+s[0]+" priority="+str(priority)+",nw_tos=8,ip,actions=normal"
            file.write(add_flow_cmd+"\n")
        priority -= 10       
        for s in slist:
            add_flow_cmd="ovs-ofctl add-flow "+s[0]+" priority="+str(priority)+",nw_tos=4,ip,actions=push_vlan:0x8100,set_field:"+str(s[1]+4096)+"-\>vlan_vid,mod_nw_tos:8,normal -O openflow15"
            file.write(add_flow_cmd+"\n")            
        priority -= 10        
        for s in slist:
            add_flow_cmd="ovs-ofctl add-flow "+s[0]+" priority="+str(priority)+",ip,actions=group:1 -O openflow15"
            file.write(add_flow_cmd+"\n")

def add_ho(file,slist):   
        priority=30            
        for s in slist:
            add_flow_cmd="ovs-ofctl add-flow "+s["name"]+" priority="+str(priority)+",ip,in_port:"+str(s["up_port"])+"actions=strip_vlan,strip_vlan,output:"+str(s["down_port"])
            file.write(add_flow_cmd+"\n")
        priority -= 10       
        for s in slist:
            add_flow_cmd="ovs-ofctl add-flow "+s["name"]+" priority="+str(priority)+",in_port:"+str(s["down_port"])+"actions=output:"+str(s["up_port"])
            file.write(add_flow_cmd+"\n")            

            
            
if __name__ == "__main__":
#    if len (sys.argv) < 2:
#        print("Please specify the topology file")
#        exit (1)
#    topo_file=sys.argv[1]
    topo_file="topo.json"  
    topo=json.load(open(topo_file))
    switchInfo = topo['switch']
    hostInfo = topo['host']
    print(switchInfo)
    print(hostInfo)
#    dst_path = "./script/"
#    if not os.path.exists (dst_path):
#        os.makedirs (dst_path)
        
    f = open("script.txt","w")
    add_sw(f,switchInfo)
    add_ho(f,hostInfo)
    f.close()
    f = open("script.txt","r")
    for line in f:
        print("adding rule:"+line)
        os.system(line)
    
        
        
        
        