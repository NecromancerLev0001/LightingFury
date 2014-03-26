'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from time import time, sleep
from twisted.internet import reactor
from natpunch import *
from lfprotocol import *
from LF.config import *

class Communication:
    connAddrObj = {}
    connObjAdd = {}
    connTmObj = {}
    connObjTm = {}
    terminateFlg = False
    
    def getConnCnt(self):
        return len(self.connAddrObj)
    
    def addPeer(self, ip, port, obj):
        sleep(0.01)
        addr = '%s:%s' % (ip, port)
        tm = str(time())
        self.connAddrObj[addr] = obj
        self.connObjAdd[obj] = addr
        self.connTmObj[tm] = obj
        self.connObjTm[obj] = tm
        self.sweepConn(len(self.connAddrObj))
        
    def delPeer(self, obj):
        addr = self.connObjAdd[obj]
        tm = self.connObjTm[obj]
        ip, port = addr.split(':') 
        del self.connAddrObj[addr]
        del self.connTmObj[tm]
        del self.connObjAdd[obj]
        del self.connObjTm[obj]
        return ip, port
    
    def sweepConn(self, cnt):
        if cnt <= MAX_PEER_CNT:
            return
        disconnCnt = cnt - OPT_PEER_CNT
        disconnList = sorted(self.connTmObj.iterkeys())[:disconnCnt]
        for i in disconnList:
            self.connTmObj[str(i)].transport.loseConnection()
    
    def removePeer(self, obj):
        ip, port = self.delPeer(obj)
        self.processor.removePeer(ip, port)
        if len(self.connAddrObj) <= MIN_PEER_CNT and not self.terminateFlg:
            self.processor.genConn(len(self.connAddrObj) - MIN_PEER_CNT - 1)
            
    def __init__(self, processor):
        LFProtocol.verifyFunc = processor.verify
        self.processor = processor
        self.server = LFServerFactory() 
        self.client = LFClientFactory()
        self.server.setComm(self)
        self.client.setComm(self)
        self.localIP = UPnP_get_ip()
        if UPnP_test(1):
            self.natFlg = 'Y'
        else:
            self.natFlg = 'N'
        self.externalPort = 0
        
    def getStopFunc(self):
        return self.Stop 
    
    def shotMsg(self, msg, target=None, exclude=None):
        m = str(msg)
        if target:
            self.connAddrObj[target].sendLine(m)
            return
        for addr, peer in self.connAddrObj.items():
            if addr != exclude:
                peer.sendLine(m)
            
    def tryConnect(self, ip, port):
        if reactor.connectTCP(ip, port, self.client): #@UndefinedVariable
            return 'Y'
        return 'N'
    
    def tryDisconnect(self, target):
        self.connAddrObj[target].transport.loseConnection()
    
    def terminateConn(self):
        self.terminateFlg = True
        for addr, peer in self.connAddrObj.items():
            peer.transport.loseConnection()
        
    def Stop(self):
        self.processor.genBye()
        self.terminateConn()
        if self.natFlg == 'Y':
            UPnP_close_port(self.externalPort)
        reactor.callLater(1.5, reactor.stop) #@UndefinedVariable

def main_ver00():
    pass

if __name__ == '__main__':
    main_ver00()