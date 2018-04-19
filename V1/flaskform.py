from baseObject import baseObject
from user import user
from project import project
from team import team
from assignment import assignment
import time
import os

from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import request,session, redirect, url_for, escape,send_from_directory

import pymysql # run pip install pymysql if this fails
import json

app = Flask(__name__, static_url_path='')

logos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/Images'
configure_uploads(app, logos)


global SESSION_TIME 
SESSION_TIME = 10000


def record(msg):
    print msg

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route("/test", methods=['GET', 'POST'])
def test():
    if session.get('login_time') is not None:
        if time.time() - session.get('login_time') < SESSION_TIME:
            return "Login ok " + str(time.time() - session.get('login_time')) + str(session['user_data'])
        else:
            return "Not logged in"

#USER ROUTES
@app.route('/user/<uid>', methods=['GET','POST'])
def edit_user(uid):
    if checkSession(3):
        return redirect("/")

    if session['currentPage'] != "/user/" + uid:
        session['lastPage'] += ", " + session['currentPage']
    session['currentPage'] = "/user/" + uid
    print session['lastPage']
    print session['currentPage']

    u = user()
    emsg = ''
    assignMsg = ''
    teamMsg = ''
    assignmentSel = request.args.get('assignmentSelector')
    if assignmentSel == None:
        assignmentSel = 0
    if request.args.get('action') == 'update':
        u.getById(uid)
        u.data[0]['fname'] = request.form.get('fname')
        u.data[0]['lname'] = request.form.get('lname')
        u.data[0]['email'] = request.form.get('email')
        u.data[0]['role'] = request.form.get('role')
        u.data[0]['pw'] = request.form.get('pw')
        u.data[0]['pw2'] = request.form.get('pw2')
        u.data[0]['phoneNumber'] = request.form.get('phoneNumber')
        u.data[0]['gradDate'] = request.form.get('gradDate')
        u.data[0]['major'] = request.form.get('major')
        if u.verify_update():
            u.update()
            emsg = "<p style='color:green'>User updated.</p>"
        else:
            emsg = "<p style='color:red'>" + u.getErrorHTML() + "</p>"
    if request.args.get('action') == 'insert':
        u.createBlank()
        u.data[0]['fname'] = request.form.get('fname')
        u.data[0]['lname'] = request.form.get('lname')
        u.data[0]['email'] = request.form.get('email')
        u.data[0]['role'] = request.form.get('role')
        u.data[0]['pw'] = request.form.get('pw')
        u.data[0]['pw2'] = request.form.get('pw2')
        u.data[0]['phoneNumber'] = request.form.get('phoneNumber')
        u.data[0]['gradDate'] = request.form.get('gradDate')
        u.data[0]['major'] = request.form.get('major')
        if u.verify_new():
            u.insert()
            emsg = '<p style="color:green">User added.</p>'
        else:
            emsg = "<p style='color:red'>" + u.getErrorHTML() + "</p>"
    if request.args.get('team') == 'add':
        t = team()
        t.createBlank()
        t.data[0]['project'] = request.form.get('project')
        t.data[0]['user'] = uid
        if t.verify_new(t.data[0]['project']):
            t.insert()
            teamMsg = '<p style="color:green">Project added.</p>'
        else:
            teamMsg = "<p style='color:red'>" + t.getErrorHTML() + "</p>"
    if request.args.get('team') == 'remove':
        t = team()
        t.deleteByUser(uid, str(request.form.get('project')))
        teamMsg = '<p style="color: green; margin-bottom: 1em">' + t.returnUserName(uid) + " has been removed from " + t.returnProjectName(request.form.get('project')) + "</p>"
    if request.args.get('assignment') == "add":
        a = assignment()
        a.createBlank()
        a.data[0]['title'] = request.form.get('title')
        a.data[0]['description'] = request.form.get('description')
        a.data[0]['assignedTo'] = uid
        a.data[0]['dueDate'] = request.form.get('dueDate')
        a.data[0]['project'] = request.form.get('project')
        if a.verify_new():
            a.insert()
            assignMsg = '<p style="color: green; margin-bottom: 1em">Assignment Added</p>'
        else:
            assignMsg = '<p style="color: red; margin-bottom: 1em">' + a.getErrorHTML() + "</p>"
    if request.args.get('back') == "true":
        updatePath()

    if uid == 'new':
        u.createBlank()
        w = 'Add New User'
        act = 'insert'
        hide = "display: none"
        col1 = "col-sm-4"
        col3 = "<div class='col-sm-4'></div>"
        cta = "Add User"
    else:
        u.getById(uid)
        w = 'Account Information'
        act = 'update'
        hide = ""
        col1 = "col-sm-8"
        col3 = ""
        cta = "Update Account Information"

    html = '''<div class="row">
    <div class="col-sm-2">
        <form id="backFunction" action="''' + goBack() + '''?back=true" method="POST">
                <input type="submit" class="button-secondary" value="Back">
        </form>
    </div>
    <div class="col-sm-8">
        <h1 align="center" id="user_title_main" style="''' + hide +'''">''' + u.data[0]['fname'].upper() + ''' ''' + u.data[0]['lname'].upper() + '''</h1>
    </div>
    <div class="col-sm-2"></div>
    </div>
    <h3 align="center" style="margin: 0;''' + hide + '''">''' + u.data[0]['major'] + '''</h3>
    <div class='row'>
    <div class="''' + col1 + '''">
        <h2 style="''' + hide +'''">Projects</h2>
        <p style="''' + hide + '''">''' + teamMsg + '''</p>
            <div style="''' + hide + '''" id="userProjects">'''

    t = team()
    html += t.getProjects(uid)

    html += '''</div>
        <h2 style="''' + hide + '''">Assignments</h2>
        <p style="''' + hide + '''">''' + assignMsg + '''</p>
        <div id="userAssignments" style="''' + hide + '''">'''

    a = assignment()
    html += a.getUserAssignments(uid, assignmentSel)
    


    html += '''
    </div>
    </div>
    <div align='center' class='col-sm-4'>
    <h2 id='user_form_title'>''' + w + '''</h2>''' + emsg + '''
    <form align='left' id='user_form' action="/user/''' + str(uid) + '''?action=''' + act + '''" method="POST">
        <p class='labels'>First Name</p>
        <input name="fname" required type="text" value="''' + u.data[0]['fname'] + '''"/><br/>
        <p class='labels'>Last Name</p>
        <input name="lname" required type="text" value="''' + u.data[0]['lname'] + '''"/><br/>
        <p class='labels'>Email</p>
        <input name="email" required type="text" value="''' + u.data[0]['email'] + '''"/><br/>
        <p class='labels'>Password</p>
        <input name="pw" type="password" value=""/><br/>
        <p class='labels'>Retype Password</p>
        <input name="pw2" type="password" value=""/><br/>
        <p class='labels'>Role</p>'''+ u.getRoleMenu() +'''
        <p class='labels'>Phone Number</p>
        <input name='phoneNumber' required type="text" value="''' + u.data[0]['phoneNumber'] + '''"/><br/>
        <p class='labels'>Expected Graduation</p>
        <input name='gradDate' type='text' id="datepicker" placeholder="YYYY" value="''' + str(u.data[0]['gradDate'])  + '''"/>
        <p class='labels'>Major</p>
        <input name='major' type='text' value="''' + u.data[0]['major']  + '''"/>

        <br><br>
        <input type="submit" class='button-primary' value="''' + cta + '''"/>

    </form>
    <a href="/users?delete=''' + uid + '''" onclick="return confirm('Are you sure you want to delete this user?')" style="color: #C2C2C2; font-size: 80%;''' + hide + '''">Delete User</a>
    </div>''' + col3 + '''
    </div>

    '''
    return header() + html + footer()

@app.route("/users", methods=['GET', 'POST'])
def listusers(): 
    if checkSession(2):
        return redirect("/")

    session['lastPage'] = ''
    session['currentPage'] = "/users"
    print session['currentPage']

    u = user()

    dmsg = ''

    if request.args.get('delete') in u.getListOfIds():
        id = request.args.get('delete')
        u.deleteById(id)
        dmsg = "User has been deleted"

    html = '''<p style="color: green">''' + dmsg + '''</p>
    <a href="user/new">+ Create new user</a>
    <table style='width: 100%;' id='user_table'>
        <tr align="center" style="background-color: #2EB4ED; color: #EAEAEA; font-size: 1.13em">
            <td><b>Name</b></td>
            <td><b>Email</b></td>
            <td><b>Phone Number</b></td>
            <td><b>Role</b></td>
        </tr>'''
        
    u.getAll('role DESC')

    if len(u.data) == 0:
        html = '''<p style="color: green">''' + dmsg + '''</p>
            <p>There are no users to display</p>
        '''
    else:
        i = 0
        for row in u.data:
            c = "#2EB4ED"
            if i % 2 == 0:
                c = "#016C9B"
            html += '''
            <tr align="center" style="color: #EAEAEA; background-color:''' + c + '''">
                <td><a href="/user/''' + str(row['id']) +'''">''' + str(row['fname']) + ''' ''' + str(row['lname']) +'''</a></td>
                <td>''' + str(row['email']) +'''</td>
                <td>''' + str(row['phoneNumber']) +'''</td>
                <td>''' + u.returnRole(str(row['role'])) + '''</td>
            </tr>'''
            i += 1
        html += '''
        </table>
        '''

    return header() + html + footer()
#END USER ROUTES

#HOME ROUTE
@app.route("/", methods=['GET', 'POST'])
def login():

    session['currentPage'] = "/"
    session['lastPage'] = ""
    print session['currentPage']


    print request.args.get('action')
    msg = '''
    <div class="login">'''
    if request.args.get('action') == 'login':
        u = user()
        if u.tryLogin(request.form.get('email'), request.form.get('password')):
            session['login_time'] = time.time()
            session['user_data'] = u.data[0]
            return header() + mainMenu() + "<script src='../static/js/clock.js'></script>" + footer()
        else:
            msg = '''<div class="login">
            <p style="color: red; margin: 0" align='center'>Login Failed</p>'''
    elif request.args.get('action') == 'logout':
        session['login_time'] = None
        session['user_data'] = None
        msg = '''
        <div class="login">'''
    elif checkSession(1) == False:
        return header() + mainMenu() + "<script src='../static/js/clock.js'></script>" + footer()

    return  '''<html>
    <head>
        <title>My Page</title>
        <link rel="stylesheet" href="../static/stylesheets/style.css">
        <link rel="stylesheet" href="../static/stylesheets/bootstrap.css">
        <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    </head>
    <body>
    ''' + msg + '''
            <form action="/?action=login" method="POST" id='login'>
                <p class='labels'>Email:</p>
                <input type="text" name="email"/>
                <p class='labels'>Password:</p>
                <input type="password" name="password"/>
                <br><br>
                <input type="submit" class="button-secondary" value="Login"/>
            </form>
        </div>
    ''' + footer()
#END HOME ROUTE

#PROJECT ROUTES
@app.route('/project/<pid>', methods=['GET','POST'])
def edit_project(pid):
    if checkSession(3):
        return redirect("/")

    if session['currentPage'] != "/project/" + pid:
        session['lastPage'] += ", " + session['currentPage']
    session['currentPage'] = "/project/" + pid
    print session['lastPage']
    print session['currentPage']

    p = project()
    emsg = ''
    teamMsg = ''
    assignMsg = ''

    assignmentSel = request.args.get('assignmentSelector')
    if assignmentSel == None:
        assignmentSel = 0

    if request.args.get('action') == 'update':
        p.getById(pid)
        p.data[0]['name'] = request.form.get('name')
        p.data[0]['description'] = request.form.get('description')
        p.data[0]['status'] = request.form.get('status')
        if 'logo' in request.files:
            p.data[0]['logo'] = request.files['logo'].filename
        if p.verify_update():
            p.update()
            if 'logo' in request.files:
                file_save = logos.save(request.files['logo'])
            emsg = "<p style='color:green'>Project updated.</p>"
        else:
            emsg = "<p style='color:red'>" + p.getErrorHTML() + "</p>"
    if request.args.get('action') == 'insert':
        p.createBlank()
        p.data[0]['name'] = request.form.get('name')
        p.data[0]['description'] = request.form.get('description')
        p.data[0]['status'] = request.form.get('status')
        if ('logo' in request.files):
            filename = logos.save(request.files['logo'])
            p.data[0]['logo'] = filename
        if p.verify_new():
            p.insert()
            emsg = '<p style="color:green">Project added.</p>'
        else:
            emsg = "<p style='color:red'>" + p.getErrorHTML() + "</p>"
    if request.args.get('team') == 'add':
        t = team()
        t.createBlank()
        t.data[0]['user'] = request.form.get('user')
        t.data[0]['position'] = request.form.get('position')
        t.data[0]['project'] = pid
        print t.data
        if t.verify_new(pid):
            print t.data
            t.insert()
            teamMsg = '<p style="color: green; margin-bottom: 1em">User Added</p>'
        else:
            teamMsg = '<p style="color: red; margin-bottom: 1em">' + t.getErrorHTML() + "</p>"
    if request.args.get('team') == 'remove':
        t = team()
        t.deleteByUser(request.form.get('user'), pid)
        teamMsg = '<p style="color: green; margin-bottom: 1em">' + t.returnUserName(request.form.get('user')) + " has been removed from this project</p>"
    if request.args.get('assignment') == "add":
        a = assignment()
        a.createBlank()
        a.data[0]['title'] = request.form.get('title')
        a.data[0]['description'] = request.form.get('description')
        a.data[0]['assignedTo'] = request.form.get('user')
        a.data[0]['dueDate'] = request.form.get('dueDate')
        a.data[0]['project'] = pid
        if a.verify_new():
            a.insert()
            assignMsg = '<p style="color: green; margin-bottom: 1em">Assignment Added</p>'
        else:
            assignMsg = '<p style="color: red; margin-bottom: 1em">' + a.getErrorHTML() + "</p>"
    if request.args.get('back') == "true":
        updatePath()

    if pid == 'new':
        p.createBlank()
        w = 'Add New Project'
        act = 'insert'
        hide = "display: none"
        col1 = "col-sm-4"
        col3 = "<div class='col-sm-4'></div>"
        cta = "Add Project"
    else:
        p.getById(pid)
        w = 'Project Information'
        act = 'update'
        hide = ""
        col1 = "col-sm-8"
        col3 = ""
        cta = "Update Project"
    if p.data[0]['logo'] == '':
        src = ""
    else:
        src = "src='../static/Images/" + p.data[0]['logo'] + "'"

    html = '''<div class="row">
    <div class="col-sm-2">
        <form id="backFunction" action="''' + goBack() + '''?back=true" method="POST">
                <input type="submit" class="button-secondary" value="Back">
        </form>
    </div>
    <div class="col-sm-8">
        <h1 id="user_title_main" align="center" style="''' + hide +'''">''' + p.data[0]['name'].upper() + '''</h1>
    </div>
    <div class="col-sm-2"></div>
    </div>
    <div class='row'>
    <div class="''' + col1 + '''">
        <h2 style="''' + hide +'''">Team</h2>''' + teamMsg + '''
        <div style="''' + hide + '''" id="projectTeam">'''
    
    t = team()
    html += t.getTeam(pid)

    html += '''</div>
        <h2 style="''' + hide +'''">Assignments</h2>
        <div style="''' + hide + '''" id="projectAssignments">'''

    a = assignment()
    html += a.getProjectAssignments(pid, assignmentSel)

    html += '''
        </div>
        </div>
        <div align='center' class='col-sm-4'>
        <h2 id='user_form_title'>''' + w + '''</h2>''' + emsg + '''
        <form align='left' enctype="multipart/form-data" id='project_form' action="/project/''' + str(pid) + '''?action=''' + act + '''" method="POST">
            <p class='labels'>Name</p>
            <input name="name" required type="text" value="''' + p.data[0]['name'] + '''"/><br/>
            <p class='labels'>Description</p>
            <textarea name="description" style="width:100%; height: 12em" required form="project_form">''' + p.data[0]['description'] + '''</textarea>
            <p class='labels'>Status</p>''' + p.getStatusMenu() + '''
            <p class='labels'>Logo</p>
            <img id="project_logo" ''' + src + '''/><br/>
            <input name="logo" type="file" accept="image/*"/ value="''' + p.data[0]['logo'] + '''">
            <br>

            <input type="submit" class='button-primary' value="''' + cta + '''"/>

        </form>
        <a href="/projects?delete=''' + pid + '''" onclick="return confirm('Are you sure you want to delete ''' + p.data[0]['name'] + '''?');" style="color: #C2C2C2; font-size: 80%; ''' + hide + '''">Delete Project</a>
        </div>''' + col3 + '''
        </div>

        '''
    return header() + html + footer()



@app.route("/projects", methods=['GET', 'POST'])
def listprojects(): 
    if checkSession(2):
        return redirect("/")

    session['lastPage'] = ''
    session['currentPage'] = "/projects"
    print session['lastPage']
    print session['currentPage']

    p = project()

    dmsg = ''

    if request.args.get('delete') in p.getListOfIds():
        id = request.args.get('delete')
        p.deleteById(id)
        dmsg = "Project has been deleted"

    html = '''<p style="color: green">''' + dmsg + '''</p>
    <a href="project/new">+ Create new project</a>
    <table style='width: 100%;' id='user_table'>
        <tr align="center" style="background-color: #2EB4ED; color: #EAEAEA; font-size: 1.13em">
            <td><b>Name</b></td>
            <td><b>Status</b></td>
        </tr>'''
        
    
    p.getAll('status DESC')
    if len(p.data) == 0:
        html = '''<p style="color: green">''' + dmsg + '''</p>
        <p>There are no projects to display</p>'''
    else:
        i = 0
        for row in p.data:
            c = "#2EB4ED"
            if i % 2 == 0:
                c = "#016C9B"
            html += '''
            <tr align="center" style="color: #EAEAEA; background-color:''' + c + '''">
                <td><a href="/project/''' + str(row['id']) +'''">''' + str(row['name']) + '''</a></td>
                <td>''' + p.returnStatus(str(row['status'])) +'''</td>
            </tr>'''
            i += 1
        html += '''
        </table>
        '''

    return header() + html + footer()
#END PROJECT ROUTES


#BEGIN ASSIGNMENT ROUTES
@app.route("/assignments", methods=['GET', 'POST'])
def listassignments(): 
    if checkSession(2):
        return redirect("/")

    session['lastPage'] = ''
    session['currentPage'] = "/assignments"
    print session['lastPage']
    print session['currentPage']

    a = assignment()

    dmsg = ''

    if request.args.get('delete') in a.getListOfIds():
        id = request.args.get('delete')
        a.deleteById(id)
        dmsg = "Assignment has been deleted"

    html = '''
    <p style="color: green">''' + dmsg + '''</p>
    <table style='width: 100%;' id='user_table'>
        <tr align="center" style="background-color: #2EB4ED; color: #EAEAEA; font-size: 1.13em">
            <td><b>Assignment</b></td>
            <td><b>Project</b></td>
            <td><b>Assigned To</b></td>
            <td><b>Status</b></td>
            <td><b>Due Date</b></td>
        </tr>'''
        
    a.getAll("status ASC")
    if len(a.data) == 0:
        html = '''<p style="color: green">''' + dmsg + '''</p>
        <p>There are no assignments to display</p>'''
    else:
        i = 0
        for row in a.data:
            c = "#2EB4ED"
            if i % 2 == 0:
                c = "#016C9B"
            html += '''
            <tr align="center" style="color: #EAEAEA; background-color:''' + c + '''">
                <td><a href="/assignment/''' + str(row['id']) +'''">''' + str(row['title']) + ''' </a></td>
                <td><a href="/project/''' + str(row['project']) + '''">''' + str(a.returnProjectName(row['project'])) + '''</a></td>
                <td><a href="/user/''' + str(row['assignedTo']) + '''">''' + str(a.returnUserName(row['assignedTo'])) + '''</a></td>
                <td>''' + a.returnStatus(str(row['status'])) +'''</td>
                <td>''' + str(row['dueDate']) +'''</td>
            </tr>'''
            i += 1
        html += '''
        </table>
        '''
    return header() + html + footer()


@app.route('/assignment/<aid>', methods=['GET','POST'])
def edit_assignment(aid):
    if checkSession(3):
        return redirect("/")

    if session['currentPage'] != "/assignment/" + aid:
        session['lastPage'] += ", " + session['currentPage']
    session['currentPage'] = "/assignment/" + aid
    print session['lastPage']
    print session['currentPage']


    a = assignment()
    emsg = ''
    if request.args.get('action') == 'update':
        a.getById(aid)
        a.data[0]['title'] = request.form.get('title')
        a.data[0]['description'] = request.form.get('description')
        a.data[0]['dueDate'] = request.form.get('dueDate')
        a.data[0]['project'] = request.form.get('project')
        a.data[0]['assignedTo'] = request.form.get('assignedTo')
        if request.form.get('completed') == "on":
            a.markComplete()
        if a.verify_update():
            a.update()
            emsg = "<p style='color:green'>Assignment updated.</p>"
        else:
            emsg = "<p style='color:red'>" + a.getErrorHTML() + "</p>"
    if request.args.get('action') == 'insert':
        a.createBlank()
        a.data[0]['title'] = request.form.get('title')
        a.data[0]['description'] = request.form.get('description')
        a.data[0]['dueDate'] = request.form.get('dueDate')
        a.data[0]['project'] = request.form.get('project')
        a.data[0]['assignedTo'] = request.form.get('assignedTo')
        if a.verify_new():
            a.insert()
            emsg = '<p style="color:green">Assignment Created.</p>'
        else:
            emsg = "<p style='color:red'>" + a.getErrorHTML() + "</p>"
    if request.args.get('back') == "true":
        updatePath()
    if aid == 'new':
        a.createBlank()
        w = 'Create New Assignment'
        act = 'insert'
        hide = "display: none"
        col1 = "col-sm-4"
        col3 = "<div class='col-sm-4'></div>"
        cta = "Create Assignment"
        complete = ""
        return redirect("/assignments")
    else:
        a.getById(aid)
        w = 'Assignment Information'
        act = 'update'
        hide = ""
        col1 = "col-sm-8"
        col3 = ""
        cta = "Update Assignment"
        if a.data[0]['status'] == 1:
            complete = '''<div align="center">
                <p>Assignment has been marked complete</p>
            </div>
            '''
        else:
            complete = '''<div align="center">
                <p>Check to Complete</p>
                <input name="completed" style="width: 10%; margin: auto" type="radio" value="on"/>
            </div>
            '''

    html = '''<div class="row">
        <div class="col-sm-2">
            <form id="backFunction" action="''' + goBack() + '''?back=true" method="POST">
                <input type="submit" class="button-secondary" value="Back">
            </form>
        </div>
        <div class="col-sm-8">
        </div>
        <div class="col-sm-2"></div>
    </div>
    <div class='row'>
    <div class="col-sm-4">
    </div>
    <div align='center' class='col-sm-4'>
    <h2 id='user_form_title'>''' + w + '''</h2>''' + emsg + '''
    <form align='left' id='assignment_form' action="/assignment/''' + str(aid) + '''?action=''' + act + '''" method="POST">
        <p class='labels'>Title</p>
        <input name="title" required type="text" value="''' + a.data[0]['title'] + '''"/><br/>
        <p class='labels'>Description</p>
        <textarea name="description" style="width: 100%; height: 10em" form='assignment_form'>''' + a.data[0]['description'] + '''</textarea>
        <p class='labels'>Due Date</p>
        <input name="dueDate" required type="text" id="datepicker" value="''' + str(a.data[0]['dueDate']) + '''"/><br/>
        <p class='labels'>Project</p> ''' + str(a.returnProjectList(a.data[0]['project'])) + '''
        <p class='labels'>Assigned To</p>''' + str(a.returnUserList(a.data[0]['assignedTo']))  + '''
        <br><br>''' + complete + '''<br>
        <input type="submit" class='button-primary' value="''' + cta + '''"/>
    </form>
    <a href="/assignments?delete=''' + aid + '''" onclick="return confirm('Are you sure you want to delete this assignment?')" style="color: #C2C2C2; font-size: 80%; ''' + hide + '''">Delete Assignmnet</a>
    </div> 
    <div class='col-sm-4'></div>
    </div>

    '''
    return header() + html + footer()

#END ASSIGNMENT ROUTES

def header():
    return '''<html>
    <head>
        <meta charset="UTF-8">
        <title>Shipley Center</title>
        <link rel="stylesheet" href="../static/stylesheets/style.css">
        <link rel="stylesheet" href="../static/stylesheets/bootstrap.css">
        <link rel="stylesheet" href="../static/js/jquery-ui-1.12.1.custom/jquery-ui.css"
        <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    </head>
    <body class="main">
            <div id="header" class="row">
                <div id="logo" class="col-sm-3" style="padding:0">
                    <a href="/"><img src="../static/Images/LOGO-2.jpg"></a>
                </div>
                <div class="col-sm-3"></div>
                <div class="nav col-sm-6" align="center">
                    <ul>
                        <li><a href="/projects">Projects</a></li>
                        <li><a href="/users">Users</a></li>
                        <li><a href="/assignments">Assignments</a></li>
                        <li><a href="/?action=logout">Logout</a></li>
                    </ul>
                </div>
            </div>
    '''
def footer():
    return '''
        <script src="../static/js/jquery-ui-1.12.1.custom/external/jquery/jquery.js"></script>
        <script src="../static/js/jquery-ui-1.12.1.custom/jquery-ui.js"></script>
        <script src="../static/js/master.js"></script>
    </body>
    <div id="footer">
    </div>
</html>
    '''

def mainMenu():
    return'''
    <h1 style='font-size: 8em' id='clock' align='center'></h1>
    <h3 style='color: #C2C2C2'id='date' align='center'></h3>
    '''

def checkSession(n):
    if session.get('login_time') is not None:
        if time.time() - session.get('login_time') < SESSION_TIME and session['user_data']['role'] >= n:
            return False
        else:
            return True
    else:
        return True

def goBack():
        path = session['lastPage'].split(", ")
        print path
        anchor = path[len(path) - 1]
        print anchor
        return anchor

def updatePath():
    path = session['lastPage'].split(", ")
    path.pop()
    path.pop()
    path = ", ".join(path)
    print path
    session['lastPage'] = path
    print session['lastPage']
    
if __name__ == "__main__":
    app.secret_key = 'AdFGsdfgsdfgst545454^Y$^y54'
    app.run(debug=True)


