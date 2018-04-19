from baseObject import baseObject
from user import user
from project import project
from team import team
import pymysql
import time
import datetime

from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import request,session, redirect, url_for, escape,send_from_directory


class assignment(baseObject):
    def __init__(self):
        tn = 'grayden_assignment_table'
        pk = 'id'
        self.setupObject(tn,pk)
        self.statusList = [['Complete', '1'], ['Incomplete', '0']]
        self.viewList = [['Incomplete', '0'], ['Complete', '1'], ['All', '2']]
        
    def verify_new(self,n=0):
        self.errors = []

        if self.data[n]['title'] == '':
            self.errors.append('You must give this assignment a title')
        if self.data[n]['dueDate'] == '':
            self.errors.append('You must enter the assignment\'s due date')
        if self.data[n]['assignedTo'] == "18":
            self.errors.append('You must select a user to assign this to')
        self.data[n]['dateAssigned'] = datetime.datetime.now()
        self.data[n]['assignedBy'] = str(session['user_data']['id'])

        if len(self.errors)>0:
            return False
        else:
            return True

    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['title'] == '':
            self.errors.append('You must give this assignment a title')
        if self.data[n]['dueDate'] == '':
            self.errors.append('You must enter the assignment\'s due date')
        if self.data[n]['assignedTo'] == "18":
            self.errors.append('You must select a user to assign this to')
        if str(self.data[n]['status']) == "1":
            self.errors.append('This assignment has already been completed')
        if len(self.errors)>0:
            return False
        else:
            return True 


    def returnStatus(self, s):
        for item in self.statusList:
                if s == item[1]:
                    return item[0]
        
    def returnUserName(self, uid):
        u = user()
        u.getById(uid)
        return u.data[0]['fname'] + " " + u.data[0]['lname']

    def returnProjectName(self, pid):
        p = project()
        p.getById(pid)
        return p.data[0]['name']

    def returnProjectList(self, id):
        if self.data[0]['project'] == "":
            self.data[0]['project'] = "9"
        p = project()
        p.getAll()
        buf = "<select name='project'>"
        for row in p.data:
            if str(self.data[0]['project']) == str(row['id']):
                sel = 'selected="true"'
            else:
                sel = ""
            buf += "<option " + sel + " value='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        buf += "</select>"
        return buf

    def returnUserList(self, id):
        if self.data[0]['assignedTo'] == "":
            self.data[0]['assignedTo'] = "18"
        u = user()
        u.getAll()
        buf = "<select name='assignedTo'>"
        for row in u.data:
            if str(self.data[0]['assignedTo']) == str(row['id']):
                sel = "selected='true'"
            else:
                sel = ""
            buf += "<option " + sel + " value='" + str(row['id']) + "'>" + str(row['fname']) + " " + str(row['lname']) +"</option>"
        buf += "</select>"
        return buf

    def markComplete(self):
        self.data[0]['status'] = '1'
        self.data[0]['dateCompleted'] = datetime.datetime.now()

    def getAllByUser(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `assignedTo` = %s;"
        cur.execute(sql,(id))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def getIncompleteByUser(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `assignedTo` = %s AND `status` = %s;"
        cur.execute(sql,(id, "0"))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def getCompleteByUser(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `assignedTo` = %s AND `status` = %s;"
        cur.execute(sql,(id, "1"))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()


    def getAllByProject(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `project` = %s;"
        cur.execute(sql,(id))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def getIncompleteByProject(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `project` = %s AND `status` = %s;"
        cur.execute(sql,(id, "0"))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def getCompleteByProject(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `project` = %s AND `status` = %s;"
        cur.execute(sql,(id, "1"))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def returnAssignmentSelector(self):
        html = '''<select name="assignmentSelector" onChange="submitForm('assignmentToggle')">'''
        active = request.args.get("assignmentSelector")
        for item in self.viewList:
            sel = ''
            if item[1] == str(active):
                sel = "selected='true' "
            html += '''<option ''' + sel + '''value="''' + item[1] + '''">''' + item[0] + '''</option>'''

        html += "</select>"
        return html


    def getUserAssignments(self, id, s):
        if id == "new":
            return ""
        self.data = []
        u = user()
        u.getById(id)
        t=team()
        msg = ''

        if str(s) == "2":
            self.getAllByUser(id)
            msg = '''<p>''' + u.data[0]['fname'] + ''' does not have any assignments</p>'''
        elif str(s) == "0":
            self.getIncompleteByUser(id)
            msg = '''<p>''' + u.data[0]['fname'] + ''' does not have any incomplete assignments</p>'''
        elif str(s) == "1":
            self.getCompleteByUser(id)
            msg = '''<p>''' + u.data[0]['fname'] + ''' has not completed an assignment</p>'''
   
        html = '''
            <div class="row">
                <div class="col-sm-0"></div>
                <div class="col-sm-4">
                    <form id="assignmentToggle" action="/user/''' + str(u.data[0]['id']) + '''" method="GET">'''
        
        html += self.returnAssignmentSelector()

        html += '''
                    </form>
                </div>
                <div class="col-sm-8"></div>
            </div>
        '''
        if len(self.data) == 0:
            html += msg
        else: 
            i = 0
            html += '''
                <table id="user_table" style="width:100%;">
                    <tr style="background-color: #2EB4ED; color: #EAEAEA" align="left">
                        <td class="col-sm-5"><b>Assignment<b></td>
                        <td class="col-sm-3"><b>Project<b></td>
                        <td class="col-sm-4"><b>Due Date</b></td>
                    </tr>'''
            for row in self.data:
                c = "#2EB4ED"
                if i % 2 == 0:
                    c = "#016C9B"
                html += '''
                <tr align="left" style="color: #EAEAEA; background-color:''' + c + '''">
                    <td class="col-sm-5"><a href="../assignment/''' + str(row['id']) +'''">''' + str(row['title']) + '''</a></td>
                    <td class="col-sm-3"><a href="../project/''' + str(row['project']) + '''">''' + self.returnProjectName(row['project']) +'''</a></td>
                    <td class="col-sm-4">''' + str(row['dueDate']) +'''</td>
                </tr>'''
                i += 1

            html += "</table>"

        html += '''
        <div class="row" style="margin-top: 2em" align="center">
            <div class="col-sm-1"></div>
            <div class="col-sm-3">
                <p class="button-primary" id="addAssignmentButton" onclick="toggleAddAssignment()">Create Assignment</p>
            </div>
            <div class="col-sm-1"></div>
            <div class="col-sm-3"></div>
            <div class="col-sm-4"></div>
        </div>
        '''
        html += '''<div class="row" id="assignmentForm">
                <div class="col-sm-1"></div>
                <form id="addAssignment" style="display: none" action="/user/''' + str(u.data[0]['id']) + '''?assignment=add" method="POST" class="col-sm-5">
                    <p class="labels">Title</p>
                    <input type="text" required name="title">
                    <p class="labels">Description</p>
                    <textarea style="height: 10em; width: 100%;" name="description" form="addAssignment"></textarea>
                    <p class="labels">Project</p>''' + t.returnProjectList(u.data[0]['id']) + '''
                    <p class="labels">Due Date</p>
                    <input type="text" id="datepicker" required name="dueDate"/>
                    <br><br>
                    <input type="submit" value="Create" class="button-primary"/>
                </form>
                <div class="col-sm-6"></div>
            </div>'''



        return html

    def getProjectAssignments(self, id, s):
        if id == "new":
            return ""
        self.data = []
        p = project()
        t = team()
        p.getById(id)
        msg = ''

        if str(s) == "2":
            self.getAllByProject(id)
            msg = '''<p>''' + p.data[0]['name'] + ''' does not have any assignments</p>'''
        elif str(s) == "0":
            self.getIncompleteByProject(id)
            msg = '''<p>''' + p.data[0]['name'] + ''' does not have any incomplete assignments</p>'''
        elif str(s) == "1":
            self.getCompleteByProject(id)
            msg = '''<p>''' + p.data[0]['name'] + ''' has not completed an assignment</p>'''

        html = '''
            <div class="row">
                <div class="col-sm-0"></div>
                <div class="col-sm-4">
                    <form id="assignmentToggle" action="/project/''' + str(p.data[0]['id']) + '''" method="GET">'''
        
        html += self.returnAssignmentSelector()

        html += '''
                    </form>
                </div>
                <div class="col-sm-8"></div>
            </div>
        '''

        if len(self.data) == 0:
            html += msg
        else:
            i = 0
            html += '''
                <table style="width:100%" id="user_table">
                <tr align="left" style="background-color:#2EB4ED; color:#EAEAEA; font-size: 1.13em;">
                    <td><b>Assignment<b></td>
                    <td><b>Assigned To</b></td>
                    <td><b>Due Date</b></td>
                </tr>
            '''
            for row in self.data:
                c = '#2EB4ED'
                if i % 2 == 0:
                    c = '#016C9B'
                html += '''<tr style="background-color:''' + c + '''; color:#EAEAEA">
                    <td><a href="../assignment/''' + str(row['id']) + '''">''' + row['title'] +'''</a></td>
                    <td><a href="../user/''' + str(row['assignedTo']) + '''">''' + self.returnUserName(row['assignedTo']) + '''</a></td>
                    <td>''' + str(row['dueDate']) +'''</td>
                </tr>'''
                i += 1
            html += "</table>"

        html += '''
        <div class="row" style="margin-top: 2em" align="center">
            <div class="col-sm-1"></div>
            <div class="col-sm-3">
                <p class="button-primary" id="addAssignmentButton" onclick="toggleAddAssignment()">Create Assignment</p>
            </div>
            <div class="col-sm-1"></div>
            <div class="col-sm-3"></div>
            <div class="col-sm-4"></div>
        </div>

        '''

        html += '''<div class="row" id="assignmentForm">
                <div class="col-sm-1"></div>
                <form id="addAssignment" action="/project/''' + str(p.data[0]['id']) + '''?assignment=add" method="POST" class="col-sm-5">
                    <p class="labels">Title</p>
                    <input type="text" required name="title">
                    <p class="labels">Description</p>
                    <textarea style="height: 10em; width: 100%;" name="description" form="addAssignment"></textarea>
                    <p class="labels">User</p>''' + t.returnTeamList(p.data[0]['id']) + '''
                    <p class="labels">Due Date</p>
                    <input type="text" id="datepicker" required name="dueDate"/>
                    <br><br>
                    <input type="submit" value="Create" class="button-primary"/>
                </form>
                <div class="col-sm-6"></div>
            </div>'''
        return html




