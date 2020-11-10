'''
Role dependent database program
Techs: enter new data
Admins: view all data

3 pages: Login, tech page, admin page
'''




emp_id = request.forms.get('emp_id')


data = {'title': 'Welcome'}
if role == 'admin':
    response.set_cookie('username', str(hashlib.sha1(pw)))
    return template('admin', data)              # admin template
elif role == 'tech':
    response.set_cookie('username', str(hashlib.sha1(pw)))
    return template('enter_trip_data', data)    # tech template
else:
    return "login failed"




##login
@route('/login', method='POST')
def login():
    user = request.forms.get('username')         # get form data
    pw = request.forms.get('password')
    pw = pw.encode('utf-8')
    pw = hashlib.sha1(pw).hexdigest()         # hash the password  

##########


#sql statements

#Obtain role from sql database using username and password
sql = 'SELECT role FROM members WHERE username = ? AND password = ?'

data = (user, pw)
cur.execute(sql, data)



#Admin
data = SELECT  * from trips

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

