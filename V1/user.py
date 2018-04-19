from baseObject import baseObject
import pymysql
import hashlib

class user(baseObject):
    def __init__(self):
        tn = 'grayden_user_table'
        pk = 'id'
        self.roleList = [['Admin', '3'],['Manager', '2'], ['Intern', '1'], ['Disabled','0']]
        self.setupObject(tn,pk)
        
    def verify_new(self,n=0):
        self.errors = []
        if self.data[n]['fname'] == '':
            self.errors.append("You must enter a first name")
        if self.data[n]['lname'] == '':
            self.errors.append("You must enter a last name")      
        if self.data[n]['email'] == '':
            self.errors.append("You must enter an email")
        elif '@' not in self.data[n]['email']:
            self.errors.append("Email invalid.")
        u = user()
        if u.getByEmail(self.data[n]['email']):
            self.errors.append("Email already exists")

        if self.data[n]['pw'] != self.data[n]['pw2']:
            self.errors.append("Passwords do not match")
        if len(self.data[n]['pw']) < 4:
            self.errors.append("Password must be greater than 4 characters")
        
        self.data[n]['pw'] = self.hashPassword(self.data[n]['pw'])

        if self.data[n]['phoneNumber'] == '':
            self.errors.append("You must enter a phone number")
        
        if len(self.errors)>0:
            return False
        else:
            return True


    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['fname'] == '':
            self.errors.append("You must enter a first name")
        if self.data[n]['lname'] == '':
            self.errors.append("You must enter a last name")
        if len(self.data[n]['pw']) == 0:
            del self.data[n]['pw']
        elif len(self.data[n]['pw']) > 0:
            if self.data[n]['pw'] != self.data[n]['pw2']:
                self.errors.append("Passwords do not match")
            if len(self.data[n]['pw']) < 4:
                self.errors.append("Password must be greater than 4 characters")
            self.data[n]['pw'] = self.hashPassword(self.data[n]['pw'])

        if self.data[n]['email'] == '':
            self.errors.append("You must enter an email.")
        elif '@' not in self.data[n]['email']:
            self.errors.append("Email invalid.")

        if self.data[n]['phoneNumber'] == '':
            self.errors.append("You must enter a phone number")

        if len(self.errors)>0:
            return False
        else:
            return True


    def hashPassword(self, pw):
        m = hashlib.md5()
        m.update(pw)
        return m.hexdigest() 


    def tryLogin(self,un,pw):
        self.data = []
        pw = self.hashPassword(pw)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `email` = %s AND `pw` = %s LIMIT 0,1;"
        cur.execute(sql,(un,pw))
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()

    def deleteByEmail(self,email):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM " + self.tn +" WHERE `email` = %s;"
        cur.execute(sql,(email))
        cur.close()  

    def getRoleMenu(self):
        if self.data[0]['role'] == '':
            self.data[0]['role'] = 0
        buf = "<select name='role'>"
        for role in self.roleList:
            if str(self.data[0]['role']) == role[1]:
                sel = 'selected="true"'
            else:
                sel = ''
            buf += '<option ' + sel + 'value="' + role[1] + '">' + role[0] + '</option>'
        buf += '</select>'
        return buf

    def returnRole(self,r):
        for item in self.roleList:
                if r == item[1]:
                    return item[0]

    def getByEmail(self,un):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE `email` = %s LIMIT 0,1;"
        cur.execute(sql,un)
        for row in cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        else:
            return False
        cur.close()


            