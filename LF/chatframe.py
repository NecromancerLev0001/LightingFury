'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

import wx
from sweep import LazySweeper 

CUT_MSG_INTERVAL = 300

class ChatFrame(wx.Frame):
    
    processMsgFunc = None
    closeFunc = None
    sweeper = LazySweeper(CUT_MSG_INTERVAL)
    
    def __init__(self, *args, **kwargs):
        self.checkProcess()        
        super(ChatFrame, self).__init__(*args, **kwargs)
        self.CreateMenu()
        self.CreateControls()
        self.BindEvents()
        self.DoLayout()
        self.SetClientSize(wx.Size(350, 500))
        self.SetBackgroundColour((220, 220, 255))
        self.nickTextCtrl.SetFocus()
        self.sweeper.addWork(self.refreshHistory)
    
    def checkProcess(self):
        name = "LightingFury-%s" % wx.GetUserId()
        self.Checker = wx.SingleInstanceChecker(name)
        if self.Checker.IsAnotherRunning():
            raise Exception("Program instance is already running, aborting")
    
    def refreshHistory(self):
        chatHistory = self.chatBox.GetValue()
        chatHistory = chatHistory[len(chatHistory) / 2: ] 
        self.chatBox.SetValue(chatHistory)
        
    def CreateMenu(self):
        fileMenu = wx.Menu()
        menuList = [(wx.ID_ABOUT, '&About Lighting-Fury', 
                     'Information about this program', self.OnAbout),]
        for id, label, helpText, handler in menuList:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&Help') # Add the fileMenu to the MenuBar
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame
    
    def modTotal(self, cnt):
        self.totalTextCtrl.SetValue(cnt)
    
    def CreateControls(self):
        self.totalLabel = wx.StaticText(self, label="Total Peers: ")
        self.totalTextCtrl = wx.TextCtrl(self, value=u"0", 
                                        size=wx.Size(100, 24), 
                                        style=wx.TE_READONLY | wx.TE_CENTER)
        self.totalTextCtrl.SetBackgroundColour((210, 210, 210))
        self.chatBox = \
            wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.chatBox.SetBackgroundColour((240, 240, 255))
        self.nickLabel = wx.StaticText(self, label="Nick      :  ")
        self.nickTextCtrl = wx.TextCtrl(self, size=wx.Size(200, 24), 
                                        value=u"anonymous")
        self.nickTextCtrl.SetMaxLength(70)
        self.msgTextCtrl = \
            wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.msgTextCtrl.SetMaxLength(700)
        
    def BindEvents(self):
        evtList = [(self, wx.EVT_CLOSE, self.OnClose),
                   (self, wx.EVT_WINDOW_DESTROY, self.OnDestroy),
                   (self.msgTextCtrl, wx.EVT_TEXT_ENTER, self.OnTextEnter),]
        for control, event, handler in evtList:
            control.Bind(event, handler)
        
    def DoLayout(self):
        mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        line1Sizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        line1Sizer2= wx.BoxSizer(orient=wx.HORIZONTAL)

        line1Sizer1.Add(self.totalLabel, 0, wx.ALL | wx.ALIGN_LEFT, 0)
        line1Sizer1.Add(self.totalTextCtrl, 0, wx.ALL, 0)
        line1Sizer2.Add(self.nickLabel, 0, wx.ALL | wx.ALIGN_LEFT, 0)
        line1Sizer2.Add(self.nickTextCtrl, 0, wx.ALL, 0)
        controlList = \
            [(line1Sizer1, dict(border=5, flag=wx.ALL|wx.EXPAND)),
             (self.chatBox, 
              dict(border=5, flag=wx.ALL | wx.EXPAND, proportion=8)),
             (line1Sizer2, dict(border=5, flag=wx.ALL | wx.EXPAND)),
             (self.msgTextCtrl, 
              dict(border=5, flag=wx.ALL | wx.EXPAND, proportion=2)),] 
        for control, options in controlList:
            mainSizer.Add(control, **options)    
        self.SetSizerAndFit(mainSizer)        
        
    def OnAbout(self, event):
        msg = 'This is simple chatting program\n' \
              'You can chat with all if you cat\n\n' \
              'Developer : Su-JiN Lee(kanobaoha@gmail.com)\n'
        dialog = wx.MessageDialog(self, msg, 'About..', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        
    def OnDestroy(self, event):
        #print('Ondestroy')
        pass
    
        
    def OnClose(self, event):
        if self.closeFunc:
            self.closeFunc()
        else:
             self.Destroy()
    
    def OnTextEnter(self, evt): 
        msg = self.msgTextCtrl.GetValue().strip()
        if msg == "":
            return
        self.msgTextCtrl.Clear()
        self.processMsg(self.nickTextCtrl.GetValue().strip(), msg)
        
    def processMsg(self, nick, msg):
        if self.processMsgFunc:
            self.processMsgFunc(str('\n-%s-\n %s\n' % (nick, msg)))
        else:
            print('-%s-\n %s\n' % (nick, msg))
    
    def displayMsg(self, msg):
        self.sweeper.sweep()
        self.chatBox.AppendText('%s\n' % msg)
        
if __name__ == '__main__':
    app = wx.App(0)
    frame = ChatFrame(None, title='Lighting-Fury(For Test)')
    frame.Show()    
    app.MainLoop()
    