'''
Created on 2014. 3. 21.

@author: Su-jin Lee
'''

'''
PEER
 index
 > SUBJECT_ID  + PEER_ID
 > PUBLIC_IP + PUBLIC_PORT,
 > USE_FLG
 > ACCEPT_FLG
'''
CREATE_PEER_TBL = '''
                     CREATE TABLE PEER_TBL 
                        (SUBJECT_ID  TEXT, 
                         PEER_ID     TEXT,
                         PUBLIC_IP   TEXT,
                         PUBLIC_SVPORT TEXT,
                         LOCAL_SVPORT  TEXT,
                         ACCEPT_FLG  TEXT,
                         USE_FLG     TEXT ) 
                  '''
CREATE_PEER_INDX1 = '''
                        CREATE INDEX PEER_INDX1  
                          ON PEER_TBL(SUBJECT_ID, PEER_ID)
                    '''
CREATE_PEER_INDX2 = '''
                        CREATE INDEX PEER_INDX2  
                          ON PEER_TBL(PUBLIC_IP, PUBLIC_SVPORT)
                    '''
CREATE_PEER_INDX3 = '''
                        CREATE INDEX PEER_INDX3  
                          ON PEER_TBL(USE_FLG)
                    '''
CREATE_PEER_INDX4 = '''
                        CREATE INDEX PEER_INDX4  
                          ON PEER_TBL(ACCEPT_FLG)
                    '''
PEER_INDX_LIST = [CREATE_PEER_INDX1,
                  CREATE_PEER_INDX2, 
                  CREATE_PEER_INDX3,
                  CREATE_PEER_INDX4,]
INSERT_PEER = '''
                 INSERT INTO PEER_TBL
                   (SUBJECT_ID, PEER_ID, PUBLIC_IP, PUBLIC_SVPORT, 
                   LOCAL_SVPORT, ACCEPT_FLG, USE_FLG) 
                   VALUES('%s', '%s', '%s', '%s', '%s', '%s', 'N') 
              '''
INSERT_PEER = '''
                 INSERT INTO PEER_TBL
                   (SUBJECT_ID, PEER_ID, PUBLIC_IP, PUBLIC_SVPORT, 
                   LOCAL_SVPORT, ACCEPT_FLG, USE_FLG) 
                   VALUES('%s', '%s', '%s', '%s', '%s', '%s', 'N') 
              '''
SELECT_ALL_PEERS = '''
                     SELECT SUBJECT_ID, PEER_ID, PUBLIC_IP, PUBLIC_SVPORT, 
                            LOCAL_SVPORT, ACCEPT_FLG, USE_FLG  
                     FROM PEER_TBL
                  '''
SELECT_SAMPLE_PEERS = '''
                         SELECT SUBJECT_ID, PEER_ID, PUBLIC_IP, PUBLIC_SVPORT, 
                                LOCAL_SVPORT, ACCEPT_FLG
                         FROM PEER_TBL
                         WHERE ACCEPT_FLG = 'Y'
                         ORDER BY RANDOM()
                         LIMIT 50
                      '''
SELECT_SERVERS = '''
                     SELECT PEER_ID, PUBLIC_IP, PUBLIC_SVPORT  
                     FROM PEER_TBL
                     WHERE ACCEPT_FLG = 'Y'
                       AND USE_FLG = 'N'                     
                       AND PEER_ID <> '%s'
                     ORDER BY RANDOM()
                     LIMIT 50
                 '''
DELETE_PEER_BY_ID = '''
                       DELETE FROM PEER_TBL
                       WHERE SUBJECT_ID = 'TEST'
                         AND PEER_ID = '%s'
                     '''
DELETE_PEER_BY_ADDR = '''
                        DELETE FROM PEER_TBL
                        WHERE PUBLIC_IP = '%s'
                          AND PUBLIC_SVPORT = '%s'
                      '''
DUP_PEER = '''
             SELECT 1
             FROM PEER_TBL
             WHERE SUBJECT_ID = 'TEST'
               AND PEER_ID = '%s'
           ''' 
UPDATE_PEER_USE_BY_ID = '''
                             UPDATE PEER_TBL
                             SET USE_FLG = '%s'
                             WHERE SUBJECT_ID = 'TEST'
                               AND PEER_ID = '%s'
                        '''
UPDATE_PEER_USE_BY_ADDR = '''
                                UPDATE PEER_TBL
                                SET USE_FLG = '%s'
                                WHERE SUBJECT_ID = 'TEST'
                                  AND PUBLIC_IP = '%s'
                                  AND PUBLIC_SVPORT = '%s' 
                          '''

# MSG
# index
# > SUBJECT_ID + PEER_ID 
# > TIME
CREATE_MSG_TBL = '''
                    CREATE TABLE MSG_TBL 
                        (TYPE1      TEXT,
                         TYPE2      TEXT,
                         SUBJECT_ID TEXT, 
                         OWNER_ID    TEXT,
                         TIME       TEXT, 
                         MSG        TEXT)
                 '''
CREATE_MSG_INDX1 = '''
                        CREATE INDEX MSGR_INDX1
                          ON MSG_TBL(TYPE1, TYPE2)
                    '''
CREATE_MSG_INDX2 = '''
                        CREATE INDEX MSG_INDX2 
                          ON MSG_TBL(SUBJECT_ID, OWNER_ID)
                    '''
CREATE_MSG_INDX3 = '''
                        CREATE INDEX MSGR_INDX3
                          ON MSG_TBL(TIME)
                    '''
MSG_INDX_LIST = [CREATE_MSG_INDX1,
                 CREATE_MSG_INDX2,
                 CREATE_MSG_INDX3,]
INSERT_MSG = '''
                INSERT INTO MSG_TBL
                  (TYPE1, TYPE2, SUBJECT_ID, OWNER_ID, TIME, MSG) 
                  VALUES('%s', '%s', '%s', '%s', '%s', '%s')
             '''
DELETE_MSG_BY_TIME = '''
                       DELETE FROM MSG_TBL
                       WHERE TIME < '%s'
                     '''
DUP_MSG = '''
             SELECT 1
             FROM MSG_TBL
             WHERE TYPE1 = '%s'
               AND TYPE2 = '%s'
               AND SUBJECT_ID = '%s' 
               AND OWNER_ID = '%s'
               AND TIME = '%s'
          ''' 
SELECT_ALL_MSG = '''
                    SELECT TYPE1, TYPE2, SUBJECT_ID, 
                           OWNER_ID, TIME, MSG
                    FROM MSG_TBL 
                 '''
SELECT_ALL_MSG0 = '''
                     SELECT ROWID, TYPE1, TYPE2, SUBJECT_ID, 
                            OWNER_ID, TIME, MSG
                     FROM MSG_TBL 
                     ORDER BY RANDOM()
                  '''