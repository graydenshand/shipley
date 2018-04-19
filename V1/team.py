from baseObject import baseObject
from user import user
from project import project
import pymysql
import time
import datetime

from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import request,session, redirect, url_for, escape,send_from_directory


class team(baseObject):
    def __init__(self):
        tn = 'grayden_project_team'
        pk = 'id'
        self.setupObject(tn,pk)
        
    def verify_new(self,pid,n=0):
        self.errors = []
        data = self.data
        if self.data[n]['user'] in self.getTeamList(str(pid)):
            self.errors.append('User already on project team')
        self.data = data
        if self.data[n]['user'] == '18':
            self.errors.append('Select a user to add')
        if self.data[n]['project'] == '9':
            self.errors.append('Select a project to add')

        if len(self.errors)>0:
            return False
        else:
            return True

    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['user'] in self.getTeamList(str(pid)):
            self.errors.append('User already on project team')
        if self.data[n]['user'] == "":
            self.errors.append('Select a user to add')
        
        if len(self.errors)>0:
            return False
        else:
            return True 

    def returnUserName(self, uid):
        u = user()
        u.getById(uid)
        return u.data[0]['fname'] + " " + u.data[0]['lname']

    def returnProjectName(self, pid):
        p = project()
        p.getById(pid)
        if len(p.data) > 0:
            return p.data[0]['name']

    def getAllByProject(self, pid):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `project` = %s;"
        cur.execute(sql,pid)
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def returnUserList(self, pid):
        u = user()
        u.getAll('role DESC')
        buf = "<select name='user'>"
        for row in u.data:
            if str(row['id']) not in self.getTeamList(pid):
                if str(row['id']) == "18":
                    sel = "selected='true'"
                else:
                    sel = ""
                buf += "<option " + sel + " value='" + str(row['id']) + "'>" + str(row['fname']) + " " + str(row['lname']) +"</option>"
        buf += "</select>"
        return buf

    def returnTeamList(self, pid):
        u = user()
        u.getAll('role ASC')
        buf = "<select name='user'>"
        for row in u.data:
            if str(row['id']) in self.getTeamList(pid):
                if str(row['id']) == "18":
                    sel = "selected='true'"
                else:
                    sel = ""
                buf += "<option " + sel + " value='" + str(row['id']) + "'>" + str(row['fname']) + " " + str(row['lname']) +"</option>"
        buf += '''</select>'''
        return buf

    def getTeamList(self, pid):
        self.data=[]
        teamList = []
        self.getAllByProject(pid)
        for row in self.data:
            teamList.append(str(row['user']))
        return teamList

    def deleteByUser(self, uid, pid):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM " + self.tn +" WHERE `user` = %s AND `project` = %s;"
        cur.execute(sql, (uid, pid))

    def getTeam(self, pid):
        self.data=[]
        self.getAllByProject(pid)
        html = '''<div class="row" align='center'>'''
        if len(self.getTeamList(pid)) == 0:
            html += '''<div class="col-sm-12" align='left'>
                <p>No users are assigned to this project</p>
            </div>
            '''        
        else: 
            i = 0
            for row in self.data:
                if i % 3 == 0 and i != 0:
                    html += '''</div>
                    <div class="row" align='center' style='margin-top: 2em'>'''
                html += '''<div class="col-sm-1"></div>
                <div class="col-sm-3" id="teamMember">
                    <a href="../user/''' + str(row['user']) + '''" style="color: #015478"><p>''' + self.returnUserName(str(row['user'])) + '''</p></a>
                </div>'''
                i += 1

        html += '''</div>
        <div class="row" style="margin-top: 2em" align="center">
            <div class="col-sm-3"></div>
            <div class="col-sm-3">
                <p class="button-primary" id="addTeamMemberButton" onclick="toggleAddTeamMemberForm()">Add User to Team</p>
            </div>
            <div class="col-sm-1"></div>
            <div class="col-sm-3">
                <p class="button-secondary" id="removeTeamMemberButton" onclick="toggleRemoveTeamMemberForm()">Remove User</p>
            </div>
            <div class="col-sm-2"></div>
        </div>

        <div class="row" id="teamForms">
            <div class="col-sm-3"></div>
            <form id="addTeamMember" action="/project/''' + str(pid) + '''?team=add" method="POST" class="col-sm-3">
                <p class="labels">User</p>''' + self.returnUserList(pid) + '''<br><br>
                <input type="submit" value="Add User" class="button-primary"/>
            </form>
            <div class="col-sm-1"></div>
            <form id="removeTeamMember" action="/project/''' + str(pid) + '''?team=remove" method="POST" class="col-sm-3">
                <p class="labels">User</p>''' + self.returnTeamList(pid) + '''<br><br>
                <input type="submit" value="Remove User" class="button-secondary"/>
            </form>
        </div>
        '''
        return html

    def getAllByUser(self, id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `user` = %s;"
        cur.execute(sql,id)
        for row in cur:
            self.data.append(row)
        if len(self.data) > 0:
            return True
        else:
            return False
        cur.close()

    def getProjectList(self, uid):
        self.data=[]
        projectList = []
        self.getAllByUser(uid)
        for row in self.data:
            projectList.append(str(row['project']))
        return projectList

    def returnProjectList(self, uid):
        p = project()
        p.getAll()
        buf = "<select name='project' required>"
        for row in p.data:
            if str(row['id']) in self.getProjectList(uid):
                if str(row['id']) == "9":
                    sel = "selected='true'"
                else:
                    sel = ""
                buf += "<option " + sel + " value='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        buf += '''</select>'''
        return buf

    def returnAvailableProjects(self, uid):
        p = project()
        p.getAll()
        buf = "<select name='project' required>"
        for row in p.data:
            if str(row['id']) not in self.getProjectList(uid):
                if str(row['id']) == "9":
                    sel = "selected='true'"
                else:
                    sel = ""
                buf += "<option " + sel + " value='" + str(row['id']) + "'>" + str(row['name']) + "</option>"
        buf += '''</select>'''
        return buf

    def getProjects(self, uid):
        if uid == "new":
            return ""
        self.data = []
        self.getAllByUser(uid)
        print self.data
        u = user()
        u.getById(uid)   

        html = '''<div class="row" align='center'>'''
        if len(self.data) == 0:
            html += '''
                <div class="col-sm-12" align='left'>
                    <p>''' + u.data[0]['fname'] + ''' is not assigned to any projects</p>
                </div>
            '''
        else:
            i = 0
            for row in self.data:
                if i % 3 == 0 and i != 0:
                    html += '''
                        </div>
                        <div class="row" align='center' style='margin-top: 2em'>'''
                html += '''
                    <div class="col-sm-1"></div>
                    <div class="col-sm-3" id="userProject">
                        <h3><a href="../project/''' + str(row['project']) + '''" style="color: #2EB4ED">''' + self.returnProjectName(row['project']) + '''</a></h3>
                    </div>'''
                i += 1


        html += '''</div>
        <div class="row" style="margin-top: 2em" align="center">
            <div class="col-sm-3"></div>
            <div class="col-sm-3">
                <p class="button-primary" id="addProjectButton" onclick="toggleAddTeamMemberForm()">Add Project</p>
            </div>
            <div class="col-sm-1"></div>
            <div class="col-sm-3">
                <p class="button-secondary" id="removeProjectButton" onclick="toggleRemoveTeamMemberForm()">Remove Project</p>
            </div>
            <div class="col-sm-2"></div>
        </div>

        <div class="row" id="teamForms" style="display: none">
            <div class="col-sm-3"></div>
            <form id="addTeamMember" action="/user/''' + str(uid) + '''?team=add" method="POST" class="col-sm-3">
                <p class="labels">Project</p>''' + self.returnAvailableProjects(uid) + '''<br><br>
                <input type="submit" value="Add" class="button-primary"/>
            </form>
            <div class="col-sm-1"></div>
            <form id="removeTeamMember" action="/user/''' + str(uid) + '''?team=remove" method="POST" class="col-sm-3">
                <p class="labels">Project</p>''' + self.returnProjectList(uid) + '''<br><br>
                <input type="submit" value="Remove" class="button-secondary"/>
            </form>
        </div>
        '''

        return html
