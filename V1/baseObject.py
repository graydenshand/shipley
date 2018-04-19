import pymysql

class baseObject(object):
    def setupObject(self,tn,pk):
        self.tn = tn
        self.pk = pk
        self.data = []
        self.errors = []
        self.fns = []
        self.conn = pymysql.connect(host='workzone.homeip.net', port=3306, user='ia626', passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
        self.getFieldNames()
    def getDataTable(self):
        buf = []
        l = []
        if len(self.data) < 1:
            print "[No Data]"
            return False
        for h in self.data[0]:
            l.append(h)
        buf.append(l)
        #buf.append( "\n--------------------------\n")
        for row in self.data:
            l = []
            for field,cell in row.iteritems():
                l.append(str(cell))
            buf.append(l)
        for x in buf:
            for y in x:
                print '{0:<15}'.format(y),
            print ""
        return True
    def addRow(self, row):
        self.data.append(row)
    def insert(self,n=0):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO " + self.tn + " ("
        i=0
        tk = ''
        values = []
        for fn in self.fns:
            if fn in self.data[n].keys():
                if i > 0:
                    sql+=','
                    tk += ','
                sql += '`' + fn + '`'
                values.append(self.data[n][fn])
                tk+= "%s"
                i+=1
            
        sql += ") VALUES (" + tk +");"
        #print sql
        #print values
        cur.execute(sql,(values))
        self.data[n][self.pk] = cur.lastrowid
        cur.close()
    def getFieldNames(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("DESCRIBE " + self.tn + ";")
        for field in cur:
            if len(field['Extra']) == 0:
                self.fns.append(field['Field'])
            if len(field['Extra']) > 0:
                self.pk = field['Field']
        cur.close()     
    def getAll(self, order=''):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        if order != '':
            sql = "SELECT * FROM " + self.tn +" ORDER BY " + order
        else:
            sql = "SELECT * FROM " + self.tn
        
        cur.execute(sql)
        self.data = []
        for row in cur:
            self.data.append(row)
        
        cur.close()
    def getById(self,id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + self.tn +" WHERE " + self.pk + " = %s LIMIT 0,1;"
        cur.execute(sql,(id))
        for row in cur:
            self.data.append(row)
        cur.close()
    def update(self,n=0):
        #self.data[n][self.pk]
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "UPDATE " + self.tn + " SET "
        i=0
        values = []
        for fn in self.fns:
            if fn in self.data[n].keys():
                if i > 0:
                    sql+=','
                sql += '`' + fn + '`=%s'
                values.append(self.data[n][fn])
                i+=1
        values.append(self.data[n][self.pk]) 
        sql += " WHERE `" + self.pk +"` = %s"
        #print sql
        #print values
        cur.execute(sql,(values))
        cur.close()
    def deleteById(self,id):
        self.data = []
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM " + self.tn +" WHERE " + self.pk + " = %s;"
        cur.execute(sql,(id))
        cur.close()            
        
    def getErrorHTML(self):
        return '<br>'.join(self.errors)

    def createBlank(self):
        newRow = {}
        for fn in self.fns:
            newRow[fn] = ''
        self.addRow(newRow)

        
        