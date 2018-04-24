# -*- coding: UTF-8 -*-
import time
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib import hub

import socket
import pickle
import struct
import threading

UINT16_MAX = 0xffff
UINT32_MAX = 0xffffffff
UINT64_MAX = 0xffffffffffffffff

logEnable=True
def log(str):
    global logEnable
    if logEnable:
        print(str)

def send(csocket,msg):
    head=struct.pack('Q',len(msg))
    csocket.send(head)
    csocket.send(msg)
def rcv(csocket):
    rval=bytes()
    length=csocket.recv(8)
    if len(length)==0:
        return rval
    length=struct.unpack('Q',length)
    bsize=1024
    rem=length[0]
    while rem!=0:
        if rem>bsize:
            temp=csocket.recv(bsize)
        else:
            temp=csocket.recv(rem)
        rem-=len(temp)
        rval+=temp
    return rval 

class UserController():
    def __init__(self,app,userName,userMac):
        self.app=app
        self.userName=userName
        self.userMac=userMac
        self.datapath=0
        self.userPort=0
        self.Flows=[]
        self.inited=False
        self.locking=False
        log("UserController:"+userName+"-"+userMac+"\t\tstart")
        self.cbyte=0

    def initFlow(self,dp,userPort):
        self.inited=True
        self.datapath=dp
        self.userPort=userPort
        self.createFlowsList()

        log("UserController:"+self.userName+"-"+self.userMac+"\t\tinit")

    def createFlowsList(self):
        self.Flows=[]
        for ip in self.app.checkTable:
            self.Flows.append(FlowController(self.app,self.datapath,self.userPort,self.userMac,ip))

    def removeFlowsList(self):
        for flow in self.Flows:
            flow.removeFlow()
        self.Flows=[]

    def updateFlowsList(self):
        if not self.inited:
            return
        self.removeFlowsList()
        self.createFlowsList()
        if self.locking:
            self.lockAll()

    def unlockAll(self):
        self.locking=False
        for flow in self.Flows:
            flow.unlock()

    def lockAll(self):
        self.locking=True
        for flow in self.Flows:
            flow.lock()

    def getFlow(self):
        count=0
        for flow in self.Flows:
            count=count+flow.getFlowCount()

        dt=count-self.cbyte
        if dt<0:
            dt=0
        self.cbyte=count
        #return count
        return dt

class FlowController():
    def __init__(self,app,dp,userPort,userMac,dstIP):
        self.app=app
        self.datapath=dp
        self.userPort=userPort
        self.userMac=userMac
        self.dstIP=dstIP

        self.cookie=app.getcookie()

        self.FlowCounter=0

        log("FlowController:"+str(self.cookie)+"=>"+self.userMac+"-"+self.dstIP+"\t\tstart")

        self.unlock()

        self.app.regFlows(self,self.cookie)
    def removeFlow(self):
        self.app.delete_flow(self.datapath,self.cookie)
        self.app.unregFlows(self,self.cookie)

        log("FlowController:"+str(self.cookie)+"=>"+self.userMac+"-"+self.dstIP+"\t\tremoved")

    def unlock(self):
        datapath=self.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_type=0x800,eth_src=self.userMac,ipv4_dst=self.dstIP)
        actions = [parser.OFPActionOutput(self.app.WAN)]
        self.app.add_flow(datapath, 5, match, actions,self.cookie)
        match = parser.OFPMatch(eth_type=0x800,eth_dst=self.userMac,ipv4_src=self.dstIP)
        actions = [parser.OFPActionOutput(self.userPort)]
        self.app.add_flow(datapath, 5, match, actions,self.cookie)

        log("FlowController:"+str(self.cookie)+"=>"+self.userMac+"-"+self.dstIP+"\t\tunlock")

    def lock(self):
        datapath=self.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_type=0x800,eth_src=self.userMac,ipv4_dst=self.dstIP)
        actions = []
        self.app.add_flow(datapath, 5, match, actions,self.cookie)
        match = parser.OFPMatch(eth_type=0x800,eth_dst=self.userMac,ipv4_src=self.dstIP)
        self.app.add_flow(datapath, 5, match, actions,self.cookie)

        log("FlowController:"+str(self.cookie)+"=>"+self.userMac+"-"+self.dstIP+"\t\tlock")

    def update(self,count):
        self.FlowCounter=count

    def getFlowCount(self):
        return self.FlowCounter
class MSwitch(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MSwitch, self).__init__(*args, **kwargs)
        self.timecycle=1
        self.mac_to_port = {}
        self.datapaths = {}       
        self.monitor_thread = hub.spawn(self._monitor)
        self.userList={}
        self.WAN=1
        self.cookie=0
        self.checkTable=set(["10.0.0.10","10.0.0.11","10.0.0.12"])# 检查的目标ip地址

        
        self.flows={}
        #self.monitors={}
        threading.Thread(target=MSwitch.socketlistener,args=(self,)).start()
    

    def addUser(self,userName,userMac):
        self.userList[userName]=UserController(self,userName,userMac)

    def updateCheckTable(self,iptable):
        self.checkTable=set()
        for ip in iptable:
            self.checkTable.add(ip)
        for user in self.userList:
            uc=self.userList[user]
            uc.updateFlowsList()





























    def cmdthread(self,csocket):
        while True:
            cmd=rcv(csocket)
            if len(cmd)==0:
                return
            scmd=cmd.split(' ')
            if scmd[0]=="addUser":
                self.addUser(scmd[1],scmd[2])
                retval="addUser:"+scmd[1]+"\nMacAddress:"+scmd[2]
            elif scmd[0]=="updateCheckTable":
                self.updateCheckTable(scmd[1:])
                retval="update Success"
            elif scmd[0]=="getflow":
                byte=str(self.userList[scmd[1]].getFlow())
                retval=scmd[1]+":"+byte
            elif scmd[0]=="lock":
                self.userList[scmd[1]].lockAll()
                retval=scmd[1]+":"+"locked"
            elif scmd[0]=="unlock":
                self.userList[scmd[1]].unlockAll()
                retval=scmd[1]+":"+"unlocked"
            else:
                retval="command="+cmd
            send(csocket,retval)


            

    def socketlistener(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host="0.0.0.0"
        port=2345
        s.bind((host,port))
        s.listen(5)
        while True:
            clientsocket,addr=s.accept()
            print("#server#:",addr,"\t\t[start]")
            threading.Thread(target=MSwitch.cmdthread,args=(self,clientsocket,)).start()





    def getcookie(self):
        self.cookie=self.cookie+1
        return self.cookie
 
    def regFlows(self,flow,cookie):
        self.flows[cookie]=flow
        log("FlowController:"+str(flow.cookie)+"=>"+flow.userMac+"-"+flow.dstIP+"\t\tregisted")
    def unregFlows(self,flow,cookie):
        log("FlowController:"+str(flow.cookie)+"=>"+flow.userMac+"-"+flow.dstIP+"\t\tunregisted")
        pass





    @set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.logger.debug('register datapath:', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath:', datapath.id)
                del self.datapaths[datapath.id]

        print(self.datapaths)
    def add_flow(self, datapath, priority, match, actions,cookie=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        cookie_mask = UINT64_MAX
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
        match=match, instructions=inst,cookie=cookie,cookie_mask=cookie_mask)
        datapath.send_msg(mod)

    def delete_flow(self, datapath,cookie):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        cmd = ofp.OFPFC_DELETE
        cookie =cookie
        cookie_mask = UINT64_MAX
        match = ofp_parser.OFPMatch()
        inst = []

        flow_mod = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask, 0, cmd,
                                         0, 0, 0, UINT32_MAX, ofp.OFPP_ANY,
                                         ofp.OFPG_ANY, 0, match, inst)
        datapath.send_msg(flow_mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        



    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth.dst
        src = eth.src
        dpid = datapath.id


        ipps=pkt.get_protocols(ipv4.ipv4)
        if len(ipps)!=0:
            ip=ipps[0]
            if ip.dst in self.checkTable:
                #print(ip.src)
                #print(msg.data)
                #print(pkt)
                #print(pkt.data)
                #mf=MonitoredFlow(self,in_port,ip.src,ip.dst,self.timecycle,self.timelimit,self.timelock,datapath)
                #self.monitors[mf.getcookie()]=mf
                for user in self.userList:
                    uc=self.userList[user]
                    if uc.userMac==eth.src:
                        uc.initFlow(datapath,in_port)
                        break
                return



        

        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        actions = [parser.OFPActionOutput(out_port)]
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)


    def _request_flowstats(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        bytecount={}
        for i in range(1,self.cookie+1):
            bytecount[i]=-1
        for flow in body:
            if flow.cookie!=0:
                bytecount[flow.cookie]=bytecount[flow.cookie]+flow.byte_count
            if flow.cookie in self.flows:
                self.flows[flow.cookie].update(flow.byte_count)
        #print(bytecount)
        
        
        '''
        for i in range(1,self.cookie+1):
            if bytecount[i]!=-1:
                self.monitors[i].update(bytecount[i])
        '''

    def _monitor(self):
        while True:
            for datapath in self.datapaths.values():
                self._request_flowstats(datapath)
            hub.sleep(self.timecycle)



