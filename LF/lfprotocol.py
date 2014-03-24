'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from ast import literal_eval
from time import time, sleep
from twisted.internet.protocol import ServerFactory, ClientFactory
from twisted.protocols.basic import LineReceiver

class LFProtocol(LineReceiver):
    def verifyMsg(self, msg):
        if self.verifyFunc:
            self.verifyFunc(msg)
        else:
            print('LFProtocol.verifyFunc: {0}'.format(msg))
            
    def connectionMade(self):
        ip = self.transport.getPeer().host
        port = self.transport.getPeer().port
        self.factory.comm.addPeer(ip, port, self)

    def connectionLost(self, reason):
        self.factory.comm.removePeer(self)
        
    def lineReceived(self, line):    
        msg = literal_eval(line)
        msg['peer_ip'] = self.transport.getPeer().host
        msg['peer_port'] = self.transport.getPeer().port
        self.verifyMsg(msg)

class LFServerFactory(ServerFactory):
    protocol = LFProtocol
    
    def setComm(self, comm):
        self.comm = comm

class LFClientFactory(ClientFactory):
    protocol = LFProtocol

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        
    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        self.comm.addPeer(addr.host, addr.port, p)
        return p
        
    def setComm(self, comm):
        self.comm = comm
 