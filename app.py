import os
from pprint import pprint

from flask import Flask, render_template, request, json, make_response
import json as simplejson
#import simplejson
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
#import module.database
#project_root = os.path.dirname(__name__)
#template_path = os.path.join(project_root)

mysql = MySQL()
app = Flask(__name__)
#app = Flask(__name__,template_folder=template_path)
# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = '1a_login_db'
#app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = '1234'
app.config['MYSQL_DATABASE_DB']         = 'users'
mysql.init_app(app)

#conectiondb()
cnx = mysql.connect()
cursor = cnx.cursor()
query = ("""CREATE DATABASE IF NOT EXISTS users;""")
query1 = ("""DROP TABLE IF EXISTS `user`;""")
query2 = ("""CREATE TABLE `user` ( `id` int(50) NOT NULL AUTO_INCREMENT, `username` varchar(255) DEFAULT NULL, `email` varchar(255) NOT NULL UNIQUE, `password` varchar(255) NOT  NULL, PRIMARY KEY (`id`)) ;""")
query3 = ("""DROP TABLE IF EXISTS `usersapp`;""")
query4 = ("""CREATE TABLE `usersapp` ( `id` int(50) NOT NULL AUTO_INCREMENT, `name` varchar(255) DEFAULT NULL, `lastname` varchar(255) DEFAULT NULL , `id_code` int NOt NULL UNIQUE, `email` varchar(255) DEFAULT NULL , `id_type` varchar(255) DEFAULT NULL, PRIMARY KEY (`id`) );""")
cursor.execute(query)
cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
cursor.execute(query4)
cnx.commit()
cursor.close()
cnx.close()

@app.route('/login',methods=['GET'])
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users.user")
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        cursor.close()
        conn.close()
        for item in data:
            dataTempObj = {
               'id'        : item[0],
                'name'      : item[1],
                'email'     : item[2],
                'password'  : item[3]
            }
            dataList.append(dataTempObj)
        resp = make_response(json.dumps(dataList))
        resp.headers["Content-Type"] = "application/json" 
        return resp
        #return json.dumps(dataList)
    else:
        conn.close()
        return 'error'
 








# POSTMAN
#get login by id
@app.route('/login/<id>', methods=['GET'])
def get(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM users.user Where id = %s""", (id))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    #dataList = []
    if data is not None:
        
        dataTempObj = {
            'id'        : data[0],
            'name'      : data[1],
            'email'     : data[2],
            'password'  : data[3]
        }
        
        resp = make_response(json.dumps(dataTempObj))
        resp.headers["Content-Type"] = "application/json" 
        return resp
    else:
        return 'error, id no encontrado'

@app.route('/login',methods=['POST'])
def signIn():
    # open connection
    # # read request from UI
    # _name   = request.form['name']
    # _email  = request.form['email']
    # _pass   = request.form['pass']
    request_json     = request.get_json()
    _name           = request_json.get('name')
    _email           = request_json.get('email')
    _pass           = request_json.get('pass')
#    _hash_pass = generate_password_hash(_pass)

    if _name and _email and _pass:
        insert(_name,_email,_pass)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM users.user Where email = %s""", (_email))
        data = cursor.fetchall()[0]
        #dataList = []
        
        cursor.close() 
        conn.close()

        if data is not None:
            
            dataTempObj = {
                'id'        : data[0],
                'name'      : data[1],
                'email'     : data[2],
                'password'  : data[3]
            }
            
            resp = make_response(json.dumps(dataTempObj))
            resp.headers["Content-Type"] = "application/json" 
        return resp

        #return json.dumps(dataTempObj)
    else:
        return json.dumps({'error':'Ingrese los datos requeridos'})

def insert(user,email,password):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO users.user (
                username,
                email,
                password
            ) 
            VALUES (%s,%s,%s)""",(user,email,password))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/login/update/<id>',methods=['PATCH'])
def update(id):
    request_json = request.get_json()
    _name           = request_json.get('name')
    _email           = request_json.get('email')
    _pass           = request_json.get('pass')

    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE user SET username = %s, email = %s, password = %s WHERE id = %s",(_name,_email,_pass,int(id)))
    conn.commit()
    conn.close()
    if(result):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM users.user Where email = %s""", (_email))
        data = cursor.fetchall()[0]
        #dataList = []
        
        cursor.close() 
        conn.close()

        if data is not None:
            
            dataTempObj = {
                'id'        : data[0],
                'name'      : data[1],
                'email'     : data[2],
                'password'  : data[3]
            }
            
            resp = make_response(json.dumps(dataTempObj))
            resp.headers["Content-Type"] = "application/json" 
        return resp

        #return json.dumps({'updated':'true'})
    else:
        return json.dumps({'updated':'false'})

@app.route('/login/delete/<id>',methods=['DELETE'])
def delete(id):
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM users.user Where id = %s""", (id))
    data = cursor.fetchall()[0]
    #dataList = []
    
    cursor.close() 
    conn.close()

    if data is not None:
        
        dataTempObj = {
            'id'        : data[0],
            'name'      : data[1],
            'email'     : data[2],
            'password'  : data[3]
        }
        
        resp = make_response(json.dumps(dataTempObj))
        resp.headers["Content-Type"] = "application/json" 
    
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM user WHERE id = %s",int(id))
    conn.commit()
    cursor.close()
    conn.close()
    if(result):
        return resp
        #return json.dumps({'delete':'success'})
    else:
        return json.dumps({'delete':'failure'})


#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('error.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0")