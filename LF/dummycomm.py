'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from time import time, sleep
from twisted.internet import reactor

from lfprotocol import *
from comm import Communication
from LF.config import *

class DummyComm(Communication):
        
    def run(self, gui=None):
        bindPort = DUMMY_SVPORT
        p = reactor.listenTCP(bindPort, self.server) #@UndefinedVariable
        reactor.callInThread(self.test, p.port) #@UndefinedVariable
        reactor.run() #@UndefinedVariable
        
    def test(self, port):
        testMsg = {'type2': 'test',
                   'local_ip': self.localIP,
                   'public_ip': DUMMY_PUBLIC_IP,
                   'public_svport': DUMMY_SVPORT,
                   'local_svport': DUMMY_SVPORT,
                   'mapping_port': DUMMY_SVPORT,
                   'accept_flg': 'Y',
                   'nat_flg': 'N', }
        self.processor.genTestMsg(testMsg)
                
