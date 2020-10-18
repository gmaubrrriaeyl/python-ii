import wx 
import sqlite3 


# Dialog box for inputting records
class MyDialog(wx.Dialog):

    def __init__(self):

        wx.Dialog.__init__(self, None, title="Insert New Record", size = (500, 300))

        #Fields
        lbl = wx.StaticText(self, label='Enter Record Data', pos=(120, 10))
        self.tid = wx.TextCtrl(self, -1, '', pos=(20, 40))
        wx.StaticText(self, -1, 'ID', pos=(130, 45))
        self.stop_date = wx.TextCtrl(self, -1, '', (20, 80))
        wx.StaticText(self, -1, 'Stop Date', (130, 85))
        self.stop_time = wx.TextCtrl(self, -1, '', (20, 120))
        wx.StaticText(self, -1, 'Stop Time', (130, 125))
        self.actual_speed = wx.TextCtrl(self, -1, '', (20, 160))
        wx.StaticText(self, -1, 'Actual Speed', (130, 165))
        self.posted_speed = wx.TextCtrl(self, -1, '', (230, 40))
        wx.StaticText(self, -1, 'Posted Speed', (340, 45))
        self.miles_over = wx.TextCtrl(self, -1, '', (230, 80))
        wx.StaticText(self, -1, 'Miles Over', (340, 85))
        self.age = wx.TextCtrl(self, -1, '', (230, 120))
        wx.StaticText(self, -1, 'Age', (340, 125))
        self.violator_sex = wx.TextCtrl(self, -1, '', (230, 160))
        wx.StaticText(self, -1, 'Violator\'s Sex', (340, 165))

        okBtn = wx.Button(self, id=wx.ID_OK, pos=(180, 210))  # add wx.OK button



#Dataframe display, buttons
class DataList(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(900, 550))
        panel = wx.Panel(self, -1)
        
        self.table_name = wx.StaticText(panel, -1, 'Tickets', pos=(30, 5))
        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, pos=(20, 30), size=(850, 400))
        
        # set up columns
        self.list.InsertColumn(0, "ID", width = 60) 
        self.list.InsertColumn(1, "Stop Date", width = 90) 
        self.list.InsertColumn(2, "Stop Time", width = 90) 
        self.list.InsertColumn(3, "Actual Speed", width = 120) 
        self.list.InsertColumn(4, "Posted Speed", width = 120) 
        self.list.InsertColumn(5, "Miles Over", width = 90)
        self.list.InsertColumn(6, "Age", width = 60)
        self.list.InsertColumn(7, "Violator's sex", width = 120)

        # set up buttons
        display = wx.Button(panel, -1, 'Display', size=(-1, 30), pos=(40, 450))
        insert = wx.Button(panel, -1, 'Insert Record', size=(-1, 30), pos=(160, 450))
        cancel = wx.Button(panel, -1, 'Cancel', size=(-1, 30), pos=(340, 450))

        display.Bind(wx.EVT_BUTTON, self.OnDisplay )  # bind buttons to event handlers
        insert.Bind(wx.EVT_BUTTON, self.OnAdd )
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        #Count
        label1 = wx.StaticText(panel, -1, "Record Count:", pos=(600, 450)) 
        self.label2 = wx.StaticText(panel, -1, '', (680, 450))
        
        self.Centre()

    def getAllData(self):
        self.list.DeleteAllItems()    # empty the list control
        con = sqlite3.connect('speeding_tickets.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM tickets')
        results = cur.fetchall()
        count = 0
        for row in results:
            self.list.Append(row)  # add record to list control
            count+=1
        self.label2.SetLabel(str(count)) 

        cur.close()
        con.close()


    def OnDisplay(self, event):
        try:
            self.getAllData()      # display whole table

        except sqlite3.Error as error:
            dlg = wx.MessageDialog(self, str(error), 'Error occured')
            dlg.ShowModal()       # display error message


    def OnAdd(self, event):
        dlg = MyDialog()      # create an instance of MyDialog
        btnID = dlg.ShowModal()
        if btnID == wx.ID_OK:
            tid = dlg.tid.GetValue()  # get data from controls on dialog box
            stop_date = dlg.stop_date.GetValue()
            stop_time = dlg.stop_time.GetValue()
            actual_speed = dlg.actual_speed.GetValue()  # get data from controls on dialog box
            posted_speed = dlg.posted_speed.GetValue()
            miles_over = dlg.miles_over.GetValue()
            age = dlg.age.GetValue()
            violator_sex = dlg.violator_sex.GetValue()
            
            
        if tid != "" and stop_date != "" and stop_time != "" and actual_speed != "" and posted_speed != "" and miles_over != "" and age != "" and violator_sex != "":   # only if no blank values

            try:
                con = sqlite3.connect('speeding_tickets.db')  # connect to db
                cur = con.cursor()

                sql = "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

                cur.execute(sql, (tid, stop_date, stop_time, actual_speed, posted_speed, miles_over, age, violator_sex))
                con.commit()          # complete the transaction

                self.getAllData()     # display all data

            except sqlite3.Error as error:
                dlg = wx.MessageDialog(self, str(error), 'Error occured')
                dlg.ShowModal()        # display error message

        dlg.Destroy()


    def OnCancel(self, event):
        self.Close()  # exit program

        
app = wx.App()
dl = DataList(None, -1, 'Tickets Table')
dl.Show()
app.MainLoop()
