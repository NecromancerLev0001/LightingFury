'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from LF.process import Processor
from LF.usercomm import UserComm
from LF.chatframe import ChatFrame
from LF.chatapp import ChatApp

def main_ver():
    processor = Processor()
    gui = ChatApp(0)
    comm = UserComm(processor) 
    
    processor.shotFunc = comm.shotMsg
    processor.comm = comm
    processor.gui = gui
    gui.setProcessMsgFunc(processor.processMsg)
    gui.setCloseFunc(comm.getStopFunc())  
    
    comm.run(gui)


if __name__ == '__main__':
    main_ver()