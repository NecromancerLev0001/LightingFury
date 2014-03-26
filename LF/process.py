'''
Created on 2014. 3. 21.

@author: Su-jin Lee
'''

from time import time
from ast import literal_eval
from hashlib import sha1
from random import random

from dataman import DataMan
from LF.config import *

class Processor(object):
    acceptFlg = 'N'
    gui = None

    def __init__(self):
        self.peerCnt = 0
        self.connection = 0
        self.userID = sha1(str(time()) + str(random())).hexdigest()
        self.dataMan = DataMan(self.userID)
        self.processSysList = {'test': self._sysTest,
                               'sample': self._sysSample,
                               'hello': self._sysHello,
                               'ver_err': self._sysVerErr,
                               'bye': self._sysBye, }
    
    def verify(self, msg):
        if not self.dataMan.regMsg(msg):
            return
        if msg['type1'] == 'sys':
            self.processSys(msg)
        elif msg['type1'] == 'msg':
            self._reflectMsg(msg)
            self.display(msg['msg'])
    
    def processSys(self, msg):
        self.processSysList[msg['type2']](msg)
        
    def _reflectMsg(self, msg):
        exclude = '%s:%s' % (msg['peer_ip'], msg['peer_port'])
        self.comm.shotMsg(msg, None, exclude)
    
    def genTestMsg(self, msg):
        self.publicIP = msg['public_ip']
        self.publicSvPort = msg['public_svport']
        self.localSvPort = msg['local_svport']
        self.mappingPort = msg['mapping_port']
        testMsg = self.__makeMsg({'type1': 'sys',
                                  'type2': 'test',
                                  'version': VERSION,
                                  'local_ip': msg['local_ip'],
                                  'nat_flg': msg['nat_flg'],})
        self.comm.shotMsg(testMsg)        
        
    def __makeMsg(self, msg):
        tMsg = {'type2': '',
                'subject_id': 'TEST',
                'owner_id': self.userID,
                'time': time(),
                'msg': '',}
        x = tMsg.update(msg)
        return tMsg
    
    def _sysTest(self, msg):
        ''' < test acceptable 
            < provide sample peers ( + public_addr, peer_cnt)
        '''
        if not self._checkVersion(msg):
            return            
        self.acceptFlg = DEFAULT_ACCEPT_FLG
        self.NatFlg = msg['nat_flg']
        if msg['local_ip'] == msg['peer_ip'] or self.NatFlg == 'Y':
            self.acceptFlg = 'Y'
        peers = str(self.dataMan.getSamplePeers())
        sampleMsg = self.__makeMsg({'type1': 'sys',
                                    'type2': 'sample',
                                    'public_ip': msg['peer_ip'],
                                    'peer_cnt': self.peerCnt,
                                    'sample': peers,
                                    'accept_flg': self.acceptFlg})
        target = '%s:%s' % (msg['peer_ip'], msg['peer_port']) 
        self.comm.shotMsg(sampleMsg, target)
        
    def _checkVersion(self, msg):
        if msg['version'] == VERSION:
            return True
        verErrMsg = self.__makeMsg({'type1': 'sys',
                                    'type2': 'ver_err', })
        target = '%s:%s' % (msg['peer_ip'], msg['peer_port']) 
        self.comm.shotMsg(verErrMsg, target)
        return False
        
    def _sysVerErr(self, msg):
        self.display('==========Version error!==========')
        self.display('=====Upgrade program please..=====')
    
    def _sysSample(self, msg):
        ''' > register peers > try connect '''
        self.publicIP = msg['public_ip']
        self.peerCnt = msg['peer_cnt']
        self.modPeerCnt(str(self.peerCnt))
        self.acceptFlg = msg['accept_flg']
        sample = literal_eval(msg['sample'])
        self.dataMan.insertPeers(sample)
        self.genConn(OPT_PEER_CNT)
        self._genHello()
    
    def genConn(self, genCnt):
        ''' > try connect '''
        self.peerCnt = self.peerCnt + 1 
        svPeers = self.dataMan.getServers()
        connCnt = 0
        for id, ip, port in svPeers:
            if self.tryConnect(id, ip, port):
                connCnt = connCnt + 1
            if connCnt >= genCnt:
                break
            
    def tryConnect(self, id, ip, port):
        if self.comm.tryConnect(ip, int(port)) == 'Y':
            self.dataMan.updatePeerUseByID(id, 'Y')
            return True
        self.dataMan.deletePeerByID(id)
        return False        
    
    def _sysHello(self, msg):
        ''' > increase peer count > reflect msg '''
        if self.dataMan.regPeer(msg):
            self.peerCnt = self.peerCnt + 1
            self.modPeerCnt(str(self.peerCnt))
        self._reflectMsg(msg)
        if msg['accept_flg'] == 'Y' and \
           self.peerCnt < 50 and \
           self.comm.getConnCnt() < MIN_PEER_CNT:
            self.tryConnect(msg['peer_id'], msg['public_ip'], msg['public_svport'])
    
    def _genHello(self):
        ''' > shot hello msg '''
        helloMsg = self.__makeMsg({'type1': 'sys',
                                   'type2': 'hello',
                                   'peer_id': self.userID,
                                   'public_ip': self.publicIP,
                                   'public_svport': self.publicSvPort,
                                   'local_svport': self.localSvPort,
                                   'accept_flg': self.acceptFlg,})
        self.comm.shotMsg(helloMsg)
        self.display('==========connection complete==========')
    
    def _sysBye(self, msg):
        ''' > decrease peer count, delete peer info > reflect msg '''
        self.dataMan.deletePeerByID(msg['owner_id'])
        self.peerCnt = self.peerCnt - 1 
        self.modPeerCnt(str(self.peerCnt))
        self._reflectMsg(msg)
    
    def genBye(self):
        ''' > shot bye msg '''
        byeMsg = self.__makeMsg({'type1': 'sys',
                                 'type2': 'bye',})
        self.comm.shotMsg(byeMsg)
    
    def processMsg(self, msg):
        shotMsg = self.__makeMsg({'type1': 'msg',
                                  'msg': msg})
        self.dataMan.regMsg(shotMsg)
        self.comm.shotMsg(shotMsg)
        self.display(msg)
    
    def display(self, msg):
        if self.gui:
            self.gui.displayMsg(msg)
        else:
            pass
            
    def removePeer(self, ip, port):
        self.dataMan.updatePeerUseByAddr(ip, port, 'N')
                    
    def modPeerCnt(self, cnt):
        if self.gui:
            self.gui.modPeerCnt(cnt)

