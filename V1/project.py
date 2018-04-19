from baseObject import baseObject
import pymysql
import os
from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import request,session, redirect, url_for, escape,send_from_directory

class project(baseObject):
    def __init__(self):
        tn = 'grayden_project_table'
        pk = 'id'
        self.setupObject(tn,pk)
        self.statusList = [['Active', '1'],['Inactive', '0']]
        
    def verify_new(self,n=0):
        self.errors = []
        if self.data[n]['name'] == '':
            self.errors.append('You must enter a name')
        if self.data[n]['description'] == '':
            self.errors.append('You must enter a description')
        if self.data[n]['status'] == '':
            self.errors.append('You must enter the project\'s status')

        p = project()
        p.getAll()

        for row in p.data:
            if row['name'] == self.data[n]['name']:
                self.errors.append('Project is already in database')

        if len(self.errors)>0:
            return False
        else:
            return True

    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['name'] == '':
            self.errors.append('You must enter a name')
        if self.data[n]['description'] == '':
            self.errors.append('You must enter a description')
        if self.data[n]['status'] == '':
            self.errors.append('You must enter the project\'s status')
        
        if len(self.errors)>0:
            return False
        else:
            return True 

    def getStatusMenu(self):
        if self.data[0]['status'] == '':
            self.data[0]['status'] = 1
        buf = "<select name='status'>"
        for status in self.statusList:
            if str(self.data[0]['status']) == status[1]:
                sel = 'selected="true"'
            else:
                sel = ''
            buf += '<option ' + sel + 'value="' + status[1] + '">' + status[0] + '</option>'
        buf += '</select>'
        return buf

    def returnStatus(self, s):
        for item in self.statusList:
                if s == item[1]:
                    return item[0]


        



