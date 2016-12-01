import wx
import socket
import sys
import threading
from Classes import *


TRAY_TOOLTIP = 'VEXDisplay Web Server'
TRAY_ICON = os.path.join(os.getcwd(),'icon.png')

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        #self.frame.Bind(wx.EVT_CLOSE,self.on_exit)
        #self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        
    
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Get Web Address', self.on_show_IP)
        menu.AppendSeparator()
        create_menu_item(menu, 'Settings', self.on_configure_server)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    #def on_left_down(self, event):
    #    print 'Tray icon was left-clicked.'

    def on_configure_server(self, event):
        self.frame.Show(True)
        self.frame.Restore()
        
    def on_show_IP(self,event):
        ip = socket.gethostbyname(socket.gethostname())
        dlg = wx.MessageDialog(self.frame, "The VEXDisplay Server Address is: http://" + ip + ":" + self.frame.Settings.port, "VEXDisplay Server", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        
               
    def on_exit(self, event):
        self.frame.Hide()
        wx.CallAfter(self.Destroy)
        self.frame.Close()   
        sys.exit(0)

class SettingFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self.Settings = Settings()
        self.Settings.uploadDir = os.path.join(os.getcwd(),"raw")
        self.ws = WebServer(self.Settings.port, True, self.Settings.uploadDir, self.Settings.eventName)
        self.t1 = None
        
        
        
        self.SetToolTip(wx.ToolTip('VEXDisplay Web Server'))
        self.SetTitle('VEXDisplay Web Server Settings')
        self.SetSize(wx.Size(460,330))
        self.SetBackgroundColour((255,255,255))
        self.Bind(wx.EVT_ICONIZE, self.on_iconify)
        self.Bind(wx.EVT_CLOSE,self.on_exit)    
        self.segoeUIBold = wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="Segoe UI")
        self.segoeUIRegular = wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="Segoe UI")
        
        
        self.settings_lbl_header = wx.StaticText(self,-1)
        self.settings_lbl_header.SetFont(self.segoeUIBold)
        self.settings_lbl_header.SetLabel("Configure Settings")
        self.settings_lbl_header.SetPosition(((self.GetSize()[0]-self.settings_lbl_header.GetSize()[0])/2,10))
        
        
        self.settings_lbl_Port = wx.StaticText(self,-1)
        self.settings_lbl_Port.SetFont(self.segoeUIRegular)
        self.settings_lbl_Port.SetLabel("Server Port: ")
        self.settings_lbl_Port.SetPosition((20,162))
        
        self.TxtbxPort = wx.TextCtrl(self, value=self.Settings.port, pos=(self.settings_lbl_Port.GetSize()[0]+25,160), size=(self.GetSize()[0]-self.settings_lbl_Port.GetSize()[0]-25-25,self.settings_lbl_Port.GetSize()[1]+4))
        self.TxtbxPort.SetFont(self.segoeUIRegular)        
        
        
        
        
        self.settings_lbl_EventName = wx.StaticText(self,-1)
        self.settings_lbl_EventName.SetFont(self.segoeUIRegular)
        self.settings_lbl_EventName.SetLabel("Event Name: ")
        self.settings_lbl_EventName.SetPosition((20,62))   
        
        self.TxtbxEventName = wx.TextCtrl(self, value=self.Settings.eventName, pos=(self.settings_lbl_EventName.GetSize()[0]+25,60), size=(self.GetSize()[0]-self.settings_lbl_EventName.GetSize()[0]-25-25,self.settings_lbl_EventName.GetSize()[1]+4))
        self.TxtbxEventName.SetFont(self.segoeUIRegular)
        
    
    
        self.settings_lbl_UploadDir = wx.StaticText(self,-1)
        self.settings_lbl_UploadDir.SetFont(self.segoeUIRegular)
        self.settings_lbl_UploadDir.SetLabel("Upload Folder: ")
        self.settings_lbl_UploadDir.SetPosition((20,112))   
        
        self.TxtbxUploadDir = wx.TextCtrl(self, value=self.Settings.uploadDir, pos=(self.settings_lbl_UploadDir.GetSize()[0]+25,110), size=(self.GetSize()[0]-self.settings_lbl_UploadDir.GetSize()[0]-25-25,self.settings_lbl_UploadDir.GetSize()[1]+4))
        self.TxtbxUploadDir.SetFont(self.segoeUIRegular) 

        
        self.BtnApply = wx.Button(self,label="Start",pos=(25,200))
        self.BtnApply.SetFont(self.segoeUIRegular)
        self.BtnApply.SetSize((self.BtnApply.GetSize()[0]+10,self.BtnApply.GetSize()[1]+10))
        self.BtnApply.SetPosition(((self.GetSize()[0]-self.BtnApply.GetSize()[0])/2,self.BtnApply.GetPosition()[1]+5))
        
        self.BtnApply.Bind(wx.EVT_BUTTON, self.on_apply_settings)
        
        
        self.BtnRefetch = wx.Button(self,label="Re-Sync Data",pos=(25,248))
        self.BtnRefetch.SetFont(self.segoeUIRegular)
        self.BtnRefetch.SetSize((self.BtnRefetch.GetSize()[0]+50,self.BtnRefetch.GetSize()[1]+10))
        self.BtnRefetch.SetPosition(((self.GetSize()[0]-self.BtnRefetch.GetSize()[0])/2,self.BtnRefetch.GetPosition()[1]+5))
        self.BtnRefetch.Disable()
        
        self.BtnApply.Bind(wx.EVT_BUTTON, self.on_apply_settings)        
        self.BtnRefetch.Bind(wx.EVT_BUTTON,self.on_refetch_data)
        #self.Refresh()
    def on_refetch_data(self,e):
        self.BtnRefetch.Disable()
        self.ws.refetch()
        self.BtnRefetch.Enable()
    def on_apply_settings(self, e):
        if(self.BtnApply.GetLabel() == "Start"):
            self.BtnApply.SetLabel("Stop")
            self.TxtbxEventName.Disable()
            self.TxtbxPort.Disable()
            self.TxtbxUploadDir.Disable()
            
            self.Settings.eventName = self.TxtbxEventName.GetValue()
            self.Settings.port = self.TxtbxPort.GetValue()
            self.Settings.uploadDir = self.TxtbxUploadDir.GetValue()
            
            self.ws = WebServer(int(self.Settings.port),True,self.Settings.uploadDir,self.Settings.eventName)
            self.t1 = threading.Thread(target=self.ws.start)
            self.t1.start()
            self.BtnRefetch.Enable()
            #self.ws.start()
            
        elif(self.BtnApply.GetLabel() == "Stop"):
            self.BtnApply.SetLabel("Start")
            self.TxtbxEventName.Enable()
            self.TxtbxPort.Enable()
            self.TxtbxUploadDir.Enable()
            self.BtnRefetch.Disable()
            self.ws.stop()
            self.t1.join()
    
    def on_iconify(self, e):
        self.Hide() 
    def on_exit(self, event):
        dlg = wx.MessageDialog(self, "Are you sure you want to exit?", "Exit Confirmation", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()      
        if (result):
            if(self.BtnApply.GetLabel() == "Stop"):
                self.ws.stop()
                self.t1.join()
            sys.exit(0)
        else:
            self.on_iconify(event)    
    
def startServer(server):
    server.start()
    
def stopServer(server):
    server.stop()

app = wx.App(False)
mainFrame = SettingFrame()
app.SetTopWindow(mainFrame)
mainFrame.Show()
TaskBarIcon(mainFrame)
app.MainLoop()
##BUILD USING C:\Python27\python setup.py py2exe