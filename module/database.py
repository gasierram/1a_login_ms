import pymysql

class Database:
    def connect(self):
        return pymysql.connect("localhost","root","1234","users" )
    
    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try: 
            if id == None:
                cursor.execute("SELECT * FROM tbl_user order by id asc")
            else: 
                cursor.execute("SELECT * FROM tbl_user where id = %s order by id asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
            
    def insert(self,data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("INSERT INTO tbl_user(name,email,password) VALUES(%s, %s, %s)", (data['name'],data['email'],data['password'],))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
            
    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("UPDATE tbl_user set name = %s, email = %s, password = %s where id = %s", (data['name'],data['email'],data['password'],id,))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
        
    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("DELETE FROM tbl_user where id = %s", (id,))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
