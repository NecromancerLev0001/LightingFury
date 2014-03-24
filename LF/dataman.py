'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from time import sleep, time
from random import randint
from sqlite3 import dbapi2 as sqlite

from sqlstmt import *
from sweep import LazySweeper, INTERVAL

class DataMan(object):
    
    conn = sqlite.connect(':memory:', check_same_thread=False)
    cur = conn.cursor()
    sweeper = LazySweeper()
   
    def __init__(self, userID):
        self.createPeerTbl()
        self.createMsgTbl()
        self.userID = userID
        self.sweeper.addWork(self.cutMsg)
    
    def __del__(self):
        self.conn.close()
    
    def _execSql(self, sql):
        tCur = self.cur.execute(sql)
        self.conn.commit()
        return tCur
        
    def cutMsg(self):
        self.cur.execute(DELETE_MSG_BY_TIME % str(time() - INTERVAL * 2))
        self.conn.commit()
    
    def createPeerTbl(self):
        self._execSql(CREATE_PEER_TBL)
        for stmt in PEER_INDX_LIST:
            self._execSql(stmt)
    
    def regPeer(self, peerInfo):
        if self.isDupPeer(peerInfo['peer_id']):
            return False
        self._execSql(INSERT_PEER % \
                      (peerInfo['subject_id'],
                       peerInfo['peer_id'],
                       peerInfo['public_ip'],
                       peerInfo['public_svport'],
                       peerInfo['local_svport'],
                       peerInfo['accept_flg'],))
        return True
    
    def isDupPeer(self, userID):
        self._execSql(DUP_PEER % userID)
        if self.cur.fetchall():
            return True
        else:
            return False
        
    def insertPeer(self, peerInfo):
        self._execSql(INSERT_PEER % peerInfo)
    
    def updatePeerUseByID(self, id, useFlg):
        self._execSql(UPDATE_PEER_USE_BY_ID % (useFlg, id))
    
    def updatePeerUseByAddr(self, ip, port, useFlg):
        self._execSql(UPDATE_PEER_USE_BY_ADDR % (useFlg, ip, port))

    def insertPeers(self, peers):
        for p in peers:
            self._execSql(INSERT_PEER % p)

    def getAllPeers(self):
        tCur = self._execSql(SELECT_ALL_PEERS)
        return tCur.fetchall()
    
    def getServers(self):
        tCur = self._execSql(SELECT_SERVERS % self.userID)
        return tCur.fetchall()
    
    def getSamplePeers(self):
        tCur = self._execSql(SELECT_SAMPLE_PEERS)
        return tCur.fetchall()
    
    def deletePeerByID(self, id):
        self._execSql(DELETE_PEER_BY_ID % id)
        print('DataMan.deleteMsgByTime{0}'.format(self.getAllPeers()))
    
    def deletePeerByAddr(self, addrInfo):
        self._execSql(DELETE_PEER_BY_ADDR % addrInfo)
        
    # MSG_TBL
    def createMsgTbl(self):
        self._execSql(CREATE_MSG_TBL)
        for stmt in MSG_INDX_LIST:
            self._execSql(stmt)

    def insertMsg(self, msg):
        self._execSql(INSERT_MSG % (msg['type1'],
                                    msg['type2'],
                                    msg['subject_id'],
                                    msg['owner_id'],
                                    msg['time'],
                                    msg['msg'].replace("'","''"),))
        self.sweeper.sweep()

    def deleteMsgByTime(self, tm):
        self._execSql(DELETE_MSG_BY_TIME % tm)
    
    def isDupMsg(self, msg):
        self._execSql(DUP_MSG % (msg['type1'],
                                 msg['type2'],
                                 msg['subject_id'],
                                 msg['owner_id'],
                                 msg['time']))
        if self.cur.fetchall():
            return True
        return False        

    def regMsg(self, msg):
        if self.isDupMsg(msg):
            return False
        self.insertMsg(msg)
        return True
    
    def getAllMsg(self):
        tCur = self._execSql(SELECT_ALL_MSG0)
        return tCur.fetchall()


def test_msg(dman):
    msg_info1 = {'type1' : 'TYPE1',
                 'type2' : 'TYPE2',
                 'subject_id' : 'FIRST_TEST',
                 'owner_id': 'kkkkkkkkjdlfkjalsdjflas',
                 'time' : '111111172938475927', 
                 'msg': 'hi~ all~~ bangga~ bangga~',}
    msg_info2 = {'type1' : 'TYPE1',
                 'type2' : 'TYPE2',
                 'subject_id' : 'FIRST_TEST',
                 'owner_id':'qqqqqqqasjdlfkjalsdjflas',
                 'time': '222222222938475927', 
                 'msg': 'fuck you man~',}
    dman.insertMsg(msg_info1)
    dman.insertMsg(msg_info2)
    
    print(dman.isDupMsg(msg_info2))
    print(dman.regMsg(msg_info1))
    print(dman.getAllMsg())
    print(dman.getAllMsg())
    
    dman.deleteMsgByTime('222222222938475927')
    print(dman.getAllMsg())

    
def test_peer(dman):
    peer_info1 = ('FIRST_TESTER',
                  'kkkkkkklaksjdfkljaskldjfls',
                  '127.0.0.1', '12000', '12000', 'Y')
    peer_info2 = ('FIRST_TESTER',
                  'qqqqqqqqlaksjdfkljaskldjfls',
                  '127.0.0.1', '14000', '14000', 'Y')
    dman.insertPeer(peer_info1)
    dman.insertPeer(peer_info2)
    
    peer_info3 = 'qqqqqqqqlaksjdfkljaskldjfls'
    dman.deletePeerByID(peer_info3)
        
    peer_info4 = ('127.0.0.1', '12000')
    dman.deletePeerByAddr(peer_info4)
    d = dman.getAllPeers()
    print(d)


if __name__ == '__main__':
    dman = DataMan()
    test_peer(dman)
    test_msg(dman)
