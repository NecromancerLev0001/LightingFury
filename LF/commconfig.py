'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

LOCAL_MODE = 1
TEST_MODE = 2
REAL_MODE = 3

MODE = LOCAL_MODE
#MODE = TEST_MODE
#MODE = REAL_MODE

VERSION = '0.0.0'

if MODE == LOCAL_MODE:
    SINGLE_INSTANCE_MODE = False
    DUMMY_SVPORT = 51234 
    DUMMY_PUBLIC_IP = '127.0.0.1'
    PEER_SVPORT = 0
    MAX_PEER_CNT = 8
    OPT_PEER_CNT = 5
    MIN_PEER_CNT = 3
    DEFAULT_ACCEPT_FLG = 'Y'

if MODE == TEST_MODE:
    SINGLE_INSTANCE_MODE = True
    DUMMY_SVPORT = 51234
    DUMMY_PUBLIC_IP = '54.186.99.255'
    PEER_SVPORT = 59981
    MAX_PEER_CNT = 8
    OPT_PEER_CNT = 5
    MIN_PEER_CNT = 3
    DEFAULT_ACCEPT_FLG = 'N'

if MODE == REAL_MODE:
    SINGLE_INSTANCE_MODE = True
    DUMMY_SVPORT = 51234
    DUMMY_PUBLIC_IP = '54.186.99.255'
    PEER_SVPORT = 59981
    MAX_PEER_CNT = 30
    OPT_PEER_CNT = 10
    MIN_PEER_CNT = 5
    DEFAULT_ACCEPT_FLG = 'N'
    
    