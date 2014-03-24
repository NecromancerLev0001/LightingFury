'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from wx import App
from chatframe import ChatFrame

class ChatApp(App):
    
    def OnInit(self):
        self.frame = ChatFrame(None, -1, 'Lighting-Fury(Test Version)')
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True
    
    def setProcessMsgFunc(self, func):
        self.frame.processMsgFunc = func
        
    def setCloseFunc(self, func):
        self.frame.closeFunc = func
    
    def getDisplayMsgFunc(self):
        return self.frame.displayMsg
    
    def displayMsg(self, msg):
        self.frame.displayMsg(msg)
        
    def modPeerCnt(self, cnt):
        self.frame.modTotal(cnt)


def main00():
    gui = ChatApp(0)
    gui.MainLoop()
    
if __name__ == '__main__':
    main00()