'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from time import time, sleep
from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor

from natpunch import *
from lfprotocol import *
from comm import Communication
from commconfig import *

class UserComm(Communication):
    def run(self, gui=None):
        reactor.registerWxApp(gui) #@UndefinedVariable
        bindPort = self.portOpen()
        p = reactor.listenTCP(bindPort, self.server) #@UndefinedVariable
        self.tryConnect(DUMMY_PUBLIC_IP, DUMMY_SVPORT)
        reactor.callInThread(self.test, p.getHost().port) #@UndefinedVariable
        reactor.run() #@UndefinedVariable
        
    def portOpen(self):
        if self.natFlg == 'N' or not UPnP_open_port(PEER_SVPORT):
            self.natFlg = 'N'
            return 0
        self.externalPort = PEER_SVPORT
        return self.externalPort
    
    def test(self, port):
        sleep(1)
        testMsg = {'local_ip': self.localIP,
                   'public_ip': '',
                   'public_svport': port,
                   'local_svport': port,
                   'mapping_port': port,
                   'nat_flg': self.natFlg, }
        self.processor.genTestMsg(testMsg)
        
                
def main_ver00():
    pass

if __name__ == '__main__':
    main_ver00()