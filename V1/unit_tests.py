from baseObject import baseObject
from user import user
from assignment import assignment
from project import project
from team import team
import os
import paramiko
from shutil import copy2
import time
import datetime

#print u.fns
'''
newRow = {'fname':'John','lname':'Smith','email':'c@c.com'}

u.addRow(newRow)

print u.pk

if u.verify_new():
    print "Verify ok"
    u.insert()
else:
    print u.errors


newRow = {'name':'Tyler','lname':'Conlon','email':'c@c.com'}

u.addRow(newRow)
u.insert()

uid = u.data[0]['id']

u = user()
u.getById(uid)
u.data[0]['fname'] = "Bob"
u.update()

u = user()
u.getById(60)
u.data[0]['fname'] = "Bob"
u.update()

u = user()
u.deleteById(600)
u.getById(600)
u.getDataTable()


while True:
    u = user()

    un = raw_input("Enter email\n")
    pw = raw_input("Enter password\n")
    if u.tryLogin(un,pw):
        print "login ok"
    else:
        print "login failed"



u = user()
u.getById(600)
u.getDataTable()
'''

'''
u = user()
newRow = {'fname':'John','lname':'Smith','email':'a@a.com','pw':'u.hashPassword('123')'}
u.addRow()
u.insert()
'''

'''
u = user()
newRow = {'fname': 'Grayden', 'lname': 'Shand', 'email': 'shandgp@clarkson.edu', 'pw':'1234', 'pw2':'1234','role': '2', 'phoneNumber': '18024880083', 'gradDate': '2018-05-12', 'major': 'Innovation & Entrepreneurship', 'professionalInterests': '["Marketing","Product Development", "Data Analytics", "Software"]'}
u.addRow(newRow)
u.verify_new()
u.insert()
'''
'''
p = project() 
newRow = {'name':'stiBITZ', 'description': 'test', 'status': 2}
p.addRow(newRow)
p.verify_new()
p.insert()
'''
'''
a = assignment()
newRow = {'title': 'Create first Assignment', 'dueDate': '2018-04-08 14:30:00', 'description': 'Create an assignment to test your new object', 'status': '0'}
a.addRow(newRow)
a.verify_new()
a.insert()
'''

'''
a = assignment()
a.getById(4)
print a.data[0]['title']
'''
'''
a = assignment()
a.getAllByUser(3)
a.getDataTable()
'''
'''
t = team()
print t.data
newRow = {'project':'8', 'user':'16', 'position':'0'}
t.addRow(newRow)
print t.data
t.verify_new('8')
print t.data
'''
'''
t = team()
t.getAllByProject('8')
t.getDataTable()
'''
'''
t = team()
print t.getTeamList('8')
'''
t = team()
print t.getAllByUser('3')
























