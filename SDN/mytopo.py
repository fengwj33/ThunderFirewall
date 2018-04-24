#!/usr/bin/python

 
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.nodelib import NAT
from mininet.node import RemoteController, OVSSwitch,Controller
import os
class mytopo( Topo ):
 
    def build( self ):
        NAT_IP="10.0.0.254"
        nat1 = self.addNode( 'nat1', cls=NAT, ip=NAT_IP, inNamespace=False )

        h1_1 = self.addHost( 'h1_1',defaultRoute='via ' + NAT_IP )
        h1_2 = self.addHost( 'h1_2',defaultRoute='via ' + NAT_IP )
        h1_3 = self.addHost( 'h1_3',defaultRoute='via ' + NAT_IP )
        h2_1 = self.addHost( 'h2_1',defaultRoute='via ' + NAT_IP )
        h2_2 = self.addHost( 'h2_2',defaultRoute='via ' + NAT_IP )
        h2_3 = self.addHost( 'h2_3',defaultRoute='via ' + NAT_IP )
        gs1 = self.addHost( 'gs1',ip='10.0.0.10',defaultRoute='via ' + NAT_IP)
        gs2 = self.addHost( 'gs2',ip='10.0.0.11',defaultRoute='via ' + NAT_IP )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )

        s3 = self.addSwitch( 's3', failMode='standalone' )
        self.addLink(s1,s3)
        self.addLink(s2,s3)
        self.addLink(h1_1,s1)
        self.addLink(h1_2,s1)
        self.addLink(h1_3,s1)
        self.addLink(h2_1,s2)
        self.addLink(h2_2,s2)
        self.addLink(h2_3,s2)

        self.addLink(s3,nat1)
        self.addLink(gs1,s3)
        self.addLink(gs2,s3)
def runmytopo():
 
    topo = mytopo()

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='127.0.0.1' ),
        switch=OVSSwitch,
        autoSetMacs=True )
    
    net.start()
    switch = net.switches[ 0 ]
    #switch.cmd("ifconfig 's1' 10.0.0.100")
    #for host in net.hosts:
        #host.cmd("/usr/sbin/sshd -D &")
    c0=net.get("c0")
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([])
    #h1_1=net.get('h1_1')
    #os.popen('ovs-vsctl add-port s3 enp7s0')     
    
    CLI( net )
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    runmytopo()

topos = {
    'mytopo': mytopo
}
