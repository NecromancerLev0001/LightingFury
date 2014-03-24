'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from LF.process import Processor
from LF.dummycomm import DummyComm

def main_ver():
    processor = Processor()
    comm = DummyComm(processor)

    processor.shotFunc = comm.shotMsg
    processor.comm = comm
    
    comm.run()


if __name__ == '__main__':
    main_ver()
