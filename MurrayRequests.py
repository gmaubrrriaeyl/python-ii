import wx 
import sqlite3 
import requests
import datetime

"""
two labels: current datae, net gains/loses
6 columns: Company, Symbol, Purchase Price, Current Price, Shares, Gain/Loss
2 buttons: display data, close progrma
"""

#Dataframe display, buttons
class DataList(wx.Frame):

    #Class variables
    url = 'https://finnhub.io/api/v1/quote?symbol='
    key = '' #Must have a key for program to work. Easy, free to obtain at finnhub.io.
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(680, 500))
        self.uberPanel = wx.Panel(self)
        self.SetMinSize(self.GetSize())

        self.panel1 = wx.Panel(self.uberPanel, -1)
        self.panel2 = wx.Panel(self.uberPanel, -1)
        self.panel3 = wx.Panel(self.uberPanel, -1)
        
        ##Top section, date + net
        x = datetime.datetime.now()
        date = x.strftime("Current time: %A %B %d, %Y at %H:%M")
        self.time = wx.StaticText(self.panel1, -1, str(date))
        self.net_value = wx.StaticText(self.panel1, -1, '')


        ##Middle Section, listctrl
        self.table_name = wx.StaticText(self.panel2, -1, 'Stocks Table')
        self.list = wx.ListCtrl(self.panel2, -1, style=wx.LC_REPORT, size = wx.DefaultSize)
        
        # set up columns
        self.list.InsertColumn(0, "Company", format=wx.LIST_FORMAT_LEFT) 
        self.list.InsertColumn(1, "Symbol", format=wx.LIST_FORMAT_CENTRE) 
        self.list.InsertColumn(2, "Purchase Price", format=wx.LIST_FORMAT_CENTRE) 
        self.list.InsertColumn(3, "Current Price", format=wx.LIST_FORMAT_CENTRE) 
        self.list.InsertColumn(4, "Shares", format=wx.LIST_FORMAT_CENTRE) 
        self.list.InsertColumn(5, "Gains/Losses", format=wx.LIST_FORMAT_CENTRE)
        for i in range(6):
            self.list.SetColumnWidth(i, -2)


        ##Bottom section, buttons
        self.display = wx.Button(self.panel3, -1, 'Display', size=(-1, 30))
        self.cancel = wx.Button(self.panel3, -1, 'Close', size=(-1, 30))

        self.display.Bind(wx.EVT_BUTTON, self.updateLabels)  # bind buttons to event handlers
        self.display.Bind(wx.EVT_BUTTON, self.OnDisplay )  # bind buttons to event handlers
        
        self.cancel.Bind(wx.EVT_BUTTON, self.OnCancel)


        ##Sizer
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        #1
        vsizer1.Add(self.time, 0, wx.ALL, border = 5)
        vsizer1.Add(self.net_value, 0, wx.ALL, border = 5 )
        self.panel1.SetSizer(vsizer1) #Adds sizer to panel
        #2
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(self.table_name, 0, wx.ALL, border = 5)
        vsizer2.Add(self.list, 1, wx.ALL, border = 5)
        self.panel2.SetSizer(vsizer2) #Adds sizer to panel
        #3
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add(self.display, 0, wx.ALL, border = 20)
        hsizer3.Add(self.cancel, 0, wx.ALL, border = 20)
        self.panel3.SetSizer(hsizer3) #Adds sizer to panel
        
        uberSizer = wx.BoxSizer(wx.VERTICAL)
        uberSizer.Add(self.panel1,0,wx.EXPAND|wx.ALL,border = 10)
        uberSizer.Add(self.panel2,1,wx.EXPAND|wx.ALL,border=10)
        uberSizer.Add(self.panel3,0,wx.EXPAND|wx.ALL,border=10)
        self.uberPanel.SetSizer(uberSizer) 

    ## Functions
    def requestData(): # Retrieves stock data from finnhub.io
        stock = []
        stock_prices = []
        con = sqlite3.connect('tech_stocks.db')
        cur = con.cursor()

        cur.execute('SELECT symbol FROM dow_stocks')
        results = cur.fetchall()
        for row in results:
            row = stock.append(list(row))
        
        for i in stock: #Requests finnhub
            r = requests.get(str(DataList.url)+"{}&token=".format('='.join(i)) + str(DataList.key))
            x = r.json()
            z = float((round(x['c'],2)))
            stock_prices.append((z,))

        count = 0
        for i in stock_prices:
            sql = str("UPDATE dow_stocks SET current_price = (?) WHERE symbol = '{}'").format('='.join(stock[count]))
            cur.execute(sql, i)
            count += 1
        con.commit()     

            
    def getAllData(self):

        self.list.DeleteAllItems()    # empty the list control
        con = sqlite3.connect('tech_stocks.db')
        cur = con.cursor()



        try:
            cur.execute('ALTER TABLE dow_stocks ADD COLUMN current_price REAL')
        except:
            pass #Not the best way, but hey, no IF DOESN'T EXIST for ALTER TABLE, so..

        DataList.requestData()
        
        cur.execute('SELECT company, symbol, purchase_price, current_price, shares, (round((current_price * shares) - (purchase_price * shares), 2)) AS net FROM dow_stocks')
        
        results = cur.fetchall()
        count = 0
        for row in results:
            self.list.Append(row)  # add record to list control
            count+=1

        for i in range(6):
            if i == 0:
                self.list.SetColumnWidth(i, -1)
            else:
                self.list.SetColumnWidth(i, -2)
            

        cur.close()
        con.close()


    def OnDisplay(self, event):
        try:
            self.getAllData()      # display whole table

        except sqlite3.Error as error:
            dlg = wx.MessageDialog(self, str(error), 'Error occured')
            dlg.ShowModal()       # display error message
        event.Skip()


    def updateLabels(self, event): #updates net, date
        con = sqlite3.connect('tech_stocks.db')
        cur = con.cursor()
        sql = 'SELECT SUM(round(((current_price * shares) - (purchase_price * shares)), 2)) AS total FROM dow_stocks'
        cur.execute(sql)
        y = cur.fetchone()
        self.net_value.SetLabel(str('Net Value: ') + str(y).strip('(),'))
        
        x = datetime.datetime.now()
        date = x.strftime("Last updated: %A %B %d, %Y at %H:%M")
        self.time.SetLabel(str(date))
        
        event.Skip()

        
    def OnCancel(self, event):
        self.Close()  # exit program

if __name__ == '__main__':
    app = wx.App()
    dl = DataList(None, -1, 'Stocks Table')
    dl.Show()
    dl.SetMinSize(dl.GetSize()) #Cannot shrink window smaller than initial size
    app.MainLoop()
