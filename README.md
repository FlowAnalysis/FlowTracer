# FlowTracer

#### FlowTracer: An Effective Flow Trajectory Detection Solution Based on Probabilistic Packet Tagging in SDN-Enabled Networks,
published in *IEEE Transactions on Network and Service Management*.

please find the manuscript from [here](https://ieeexplore.ieee.org/document/8809253).

## How to build

1. Download Mininet

        root@localhost:~$ sudo apt-get update
        root@localhost:~$ sudo apt-get install mininet

2. Create topology class /topo/mytopo.py with /ovsrules/topo.json, please refer to http://mininet.org/walkthrough/

3. Setup topology with Mininet-OF1.3

        root@localhost:~$ sudo mn --topo ./topo/mytopo --mac --controller remote --switch ovsk,protocols=OpenFlow13
    
3. Configure switch with OVS-OF1.3

        root@localhost:~$ sudo ovs-vsctl set bridge s1 protocols=OpenFlow13
    
4. Install switch entries 

        root@localhost:~$ sudo python ./ovsrules/install_rules.py
        
5. Setup path reconstructor

        root@localhost:~$ mininet> h1 ./host/pathreconstruction/pcap.py &
    
6. Generate traffic

        root@localhost:~$ mininet> h2 python -m SimpleHTTPServer 80 &
        root@localhost:~$ mininet> h2 wget -O h1

7. Enjoy!
