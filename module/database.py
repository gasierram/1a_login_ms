import pymysql

class Database:
    def connect(self):
        return pymysql.connect("1a_login_db","root","1234","users" )
    

