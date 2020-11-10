import sqlite3
import requests
import bottle

'''
Role dependent database program
Techs: enter new data
Admins: view all data

3 pages: Login, tech page, admin page

Table: Members
Db: ??? travel expenses?
'''

#Global variables
db = 'placeholder'

## Connect to db
def connect():
    con = sqlite3.connect(db)
    cur = con.cursor()
    return cur
#################

##login page script
@route('/login', method='POST')
def login():
    user = request.forms.get('username')         # get form data
    pw = request.forms.get('password')
    pw = pw.encode('utf-8')
    pw = hashlib.sha1(pw).hexdigest()         # hash the password  
    sql = 'SELECT role FROM members WHERE username = ? AND password = ?'
    data = (user, pw)
    connect()
    cur.execute(sql, data)
    if role == 'admin':
        response.set_cookie('username', secret = str(hashlib.sha1(pw)))
        return template('admin', data)              # admin template
    elif role == 'tech':
        request.set_cookie('username', secret = str(hashlib.sha1(pw)))
        return template('enter_trip_data', data)    # tech template
    else:
        return "login failed"
##########


#Admin
def show_data():
    if request.get_cookie('username', secret=str(hashlib.sha1(pw))):
        connect()
        data = 'SELECT  * from trips'
        data = cur.execute(data)
        return template(admin, data)
    else:
        pass




#Tech
record = [None]
#record.append(None)   # None substitutes for auto-incrementing id
record.append(request.forms.get('Employee ID'))  # get posted new student data
record.append(request.forms.get('Date'))
record.append(request.forms.get('Destination'))
record.append(request.forms.get('Miles'))
record.append(request.forms.get('Gallons Used'))

INSERT INTO trips VALUES(?, ?, ?, ?, ?, ?)
cur.execute(sql, record)

