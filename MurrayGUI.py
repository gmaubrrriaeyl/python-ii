import wx
try:
    import pyperclip
except ImportError: 
    print('Install pyperclip library to use "Copy to clipboard" function')
    
class shipFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (480,500))

        self.panel = wx.Panel(self, -1) # First panel
               
        #Three Text Boxes
        self.txtctrl1 = wx.TextCtrl(self.panel, pos=(30, 30), size = (180, -1))
        self.label1 = wx.StaticText(self.panel, label="Name", pos=(220, 35)) 
        self.txtctrl2 = wx.TextCtrl(self.panel, pos=(30, 60), size = (260, -1))
        self.label2 = wx.StaticText(self.panel, label="Address", pos=(310, 65))
        self.txtctrl3 = wx.TextCtrl(self.panel, pos=(30, 90), size = (220, -1))
        self.label3 = wx.StaticText(self.panel, label="City, State, Zip", pos=(260, 95)) 
 
        #3 Radios, group 1
        self.Radio1 = wx.RadioButton(self.panel, label = '0 - 1.9 lbs: $5', pos = (30, 140), style = wx.RB_GROUP)
        self.Radio2 = wx.RadioButton(self.panel, label = '2 - 4.9 lbs: $8', pos = (30, 160))
        self.Radio3 = wx.RadioButton(self.panel, label = '5 - 10 lbs: $12.25', pos = (30, 180))

        #4 Radios, group 2
        self.Radio4 = wx.RadioButton(self.panel, label = 'Overland: $2.75', pos = (150, 140), style = wx.RB_GROUP)
        self.Radio5 = wx.RadioButton(self.panel, label = '3-Day Air: $6.15', pos = (150, 160))
        self.Radio6 = wx.RadioButton(self.panel, label = '2-Day Air: $10.80', pos = (150, 180))
        self.Radio7 = wx.RadioButton(self.panel, label = 'Overnight: $15.25', pos = (150, 200))  

        #2 Checkboxes
        self.cb1 = wx.CheckBox(self.panel, -1, label = 'Extra Padding: $5', pos = (30,230))
        self.cb2 = wx.CheckBox(self.panel, -1, label = 'Gift Wrapping: $8', pos = (30,250))
        
    
        #3 labels
        self.lbl1 = wx.StaticText(self.panel, label="Shipping Total", pos=(60, 340)) 
        self.lbl2 = wx.StaticText(self.panel, label="", pos=(60, 360))
        self.lbl3 = wx.StaticText(self.panel, label = "Shipping Label", pos=(240,340))
        self.lbl4 = wx.StaticText(self.panel, label = "", pos=(240,360))

        
        #4 buttons
        self.btn1 = wx.Button(self.panel, label="Calculate Total", pos=(20, 300))        
        self.btn2 = wx.Button(self.panel, label="Clear Form", pos=(130, 300))
        self.btn3 = wx.Button(self.panel, label = "Close", pos = (220, 300))
        self.btn4 = wx.Button(self.panel, label = "Copy label to clipboard", pos = (300,300))
        self.btn1.Bind(wx.EVT_BUTTON, self.calc_total) ## connect to function
        self.btn2.Bind(wx.EVT_BUTTON, self.clear_form) ## connect to function
        self.btn3.Bind(wx.EVT_BUTTON, self.close_frame) ## connect to function
        self.btn4.Bind(wx.EVT_BUTTON, self.copy_to_clipboard) ## connect to function
        
        ##Functions
        #Calculate total
        
    def calc_total(self, event):
        er1 = self.lbl4.SetLabel("Error in formatting. \nAre all fields entered corretly?")
        
        cost = 0
        if self.Radio1.GetValue():
            cost += 5
        elif self.Radio2.GetValue():
            cost += 8
        else:
            cost += 12.25
        
        if self.Radio4.GetValue():
            cost += 2.75
        elif self.Radio5.GetValue():
            cost += 6.15
        elif self.Radio6.GetValue():
            cost += 10.80
        else:
            cost += 15.25

        if self.cb1.GetValue():
            cost += 5
        if self.cb2.GetValue():
            cost += 8
        self.lbl2.SetLabel(str('$' + str(round(cost, 2))))
        adr1 = self.txtctrl3.GetValue()
        if not adr1.count(',')==2: #Error Catching
            return er1
        city, state, zc = adr1.split(',')
        if (self.txtctrl1.GetValue() == '' or self.txtctrl2.GetValue() == '' or ((city or state or zc) == '')):
            return er1 #Error Catching
        city = city.strip()
        state = state.strip()
        zc = zc.strip()
        label = self.txtctrl1.GetValue() + '\n' + self.txtctrl2.GetValue() + '\n' + city + ', ' + state + '\n' + zc
        self.lbl4.SetLabel(label)
        
    def copy_to_clipboard(self, event):
        pyperclip.copy(self.lbl4.GetLabel())    

    def clear_form(self, event):
        self.Radio1.SetValue(1)
        self.Radio4.SetValue(1)
        self.cb1.SetValue(0)
        self.cb2.SetValue(0)
        self.txtctrl1.SetValue('')
        self.txtctrl2.SetValue('')
        self.txtctrl3.SetValue('')
        self.lbl2.SetLabel('')
        self.lbl4.SetLabel('')
        
    def close_frame(self, event):
        self.Close()
        
if __name__=="__main__":
    app = wx.App()
    frame = shipFrame(None, 'Shipping Form')
    frame.Show(True)
    app.MainLoop()
