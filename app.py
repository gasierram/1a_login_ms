import os
from pprint import pprint

from flask import Flask, render_template, request, json, make_response
import json as simplejson
#import simplejson
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
import hashlib
import datetime
import random, string
#import module.database
#project_root = os.path.dirname(__name__)
#template_path = os.path.join(project_root)

mysql = MySQL()
app = Flask(__name__)
#app = Flask(__name__,template_folder=template_path)
# mysql configuratoin
#app.config['MYSQL_DATABASE_HOST']       = '1a_login_db'
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = '1234'
app.config['MYSQL_DATABASE_DB']         = 'users'
mysql.init_app(app)

#conectiondb()
cnx = mysql.connect()
cursor = cnx.cursor()
query = ("""CREATE DATABASE IF NOT EXISTS users;""")
query1 = ("""CREATE TABLE IF NOT EXISTS `user` ( `token` varchar(255) NOT NULL, `id` varchar(255) NOT NULL, `date` date not null, PRIMARY KEY (`token`)) ;""")
cursor.execute(query)
cursor.execute(query1)
cnx.commit()
cursor.close()
cnx.close()


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

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
               'token'        : item[0],
               'id'      : item[1],
               'date'  : item[2]
            }
            dataList.append(dataTempObj)
        resp = make_response(json.dumps(dataList))
        resp.headers["Content-Type"] = "application/json" 
        return resp
        #return json.dumps(dataList)
    else:
        conn.close()
        return json.dumps({'error'})
 

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
            'token'        : data[0],
            'id'      : data[1],
            'date'  : data[2]
        }
        
        resp = make_response(json.dumps(dataTempObj))
        resp.headers["Content-Type"] = "application/json" 
        return resp
    else:
        return json.dumps({'error, id no encontrado'})

@app.route('/login',methods=['POST'])
def signIn():
    # open connection
    # # read request from UI
    # _name   = request.form['name']
    # _email  = request.form['email']
    # _pass   = request.form['pass']
    request_json     = request.get_json()
    _id           = request_json.get('id')
    #_token           = request_json.get('token')
    #_username           = request_json.get('username')
    #_date           = request_json.get('date')
#    _hash_pass = generate_password_hash(_pass)

    #if _token and _username and _date:
    if _id:
        #insert(_token,_username,_date)
        token = insert(_id)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
        #    """SELECT * FROM users.user Where username = %s""", (_username))
            """SELECT * FROM users.user Where id = %s""", (_id))
        data = cursor.fetchall()[0]
        #dataList = []
        
        cursor.close() 
        conn.close()

        if data is not None:
            
            dataTempObj = {
                'token'        : token,
                'id'      : data[1],
                'date'     : data[2],
            }
            
            resp = make_response(json.dumps(dataTempObj))
            resp.headers["Content-Type"] = "application/json" 
        return resp

        #return json.dumps(dataTempObj)
    else:
        return json.dumps({'error':'Ingrese los datos requeridos'})

def generate_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return token


#def insert(token,username,date):
def insert(id):
    token = generate_token()
#    token = "cdeefhg1234567" 
    sha_token = encrypt_string(token)
    today = datetime.datetime.today() 
    tomorrow  = today + datetime.timedelta(1)
    date = datetime.datetime.strftime(tomorrow,'%Y-%m-%d') 
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO users.user (
                token,
                id,
                date
            ) 
            VALUES (%s,%s,%s)""",(sha_token,id,date))
    conn.commit()
    cursor.close()
    conn.close()
    return token

@app.route('/login/update/<id>',methods=['PATCH'])
def update(id):
    request_json = request.get_json()
    _token           = request_json.get('token')
    _username           = request_json.get('username')
    _date          = request_json.get('date')

    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE user SET token = %s, username = %s, date = %s WHERE id = %s",(_token,_username,_date,int(id)))
    conn.commit()
    conn.close()
    if(result):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM users.user Where token = %s""", (_token))
        data = cursor.fetchall()[0]
        #dataList = []
        
        cursor.close() 
        conn.close()

        if data is not None:
            
            dataTempObj = {
                'id'        : data[0],
                'token'      : data[1],
                'username'     : data[2],
                'date'  : data[3]
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
            'token'      : data[1],
            'username'     : data[2],
            'date'  : data[3]
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
#return render_template('error.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")