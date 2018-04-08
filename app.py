from flask import Flask, request 
from flask_restful import Resource, Api, reqparse	
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import flash, render_template, redirect, url_for, session
import json
#from module.database import Database
app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello():
    return 'Hello World! I have been seen'


mysql = MySQL()
#Conectando MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = '1a_login_db'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#POST create
class login(Resource):
    def post(self):
        try:
            # Parse the arguments

            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address for Authentication')
            parser.add_argument('password', type=str, help='Password for Authentication')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AuthenticateUser',(_userEmail, ))
            data = cursor.fetchall()

            if(len(data)>0):
                if(str(data[0][3])==_userPassword):
                    conn.commit()
                    return json.dumps({'status':200,'UserId':str(data[0][0])})
                    #session['user'] = data[0][0]
                    #return redirect('/')
                else:
                    return json.dumps({'status':100,'message':'Authentication failure'})
            
        except Exception as e:
            return json.dumps({'error': str(e)})


api.add_resource(login, '/login')

#POST Create
class CreateUser(Resource):
    global cursor
    def post(self): 
        try: 
            #parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()

            #_hashed_password = generate_password_hash(_userPassword)

            cursor.callproc('sp_createUser',('',_userEmail,_userPassword))#_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
               # return {'Email': args['email'], 'Password': args['password']}
                return json.dumps(args).strip("\\")
            else:
                return json.dumps({'error':str(data[0])})    

        except Exception as e: 
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()
api.add_resource(CreateUser, '/CreateUser')

#Delete User
class DeleteUser(Resource):
    global cursor
    def post(self): 
        try: 
            #parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            #parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']

            conn = mysql.connect()
            cursor = conn.cursor()

            #_hashed_password = generate_password_hash(_userPassword)

            cursor.callproc('sp_deleteUser',(_userEmail,))#_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
               # return {'Email': args['email'], 'Password': args['password']}
                return json.dumps({'Se ha eliminado de login': args}).strip("\\")
            else:
                return json.dumps({'error':str(data[0])})    

        except Exception as e: 
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()
api.add_resource(DeleteUser, '/DeleteUser')

#GET login
class GetUsers(Resource):
    def post(self):
        try: 
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            args = parser.parse_args()

            _userEmail = args['email']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetAllItems',(_userEmail,))
            data = cursor.fetchall()

            users_list=[]
            for item in data:
                i = {
                    'id':item[0],
                    'user':item[1],
                    'email':item[2],
                    'password':item[3]
                }
                users_list.append(i)
            return json.dumps({'StatusCode':'200'})

        except Exception as e:
            return {'error': str(e)}

api.add_resource(GetUsers, '/GetUsers')

#POST Update
class UpdateUser(Resource):
    global cursor
    def post(self): 
        try: 
            #parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to update user')
            parser.add_argument('password', type=str, help='Password to update user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()

            #_hashed_password = generate_password_hash(_userPassword)

            cursor.callproc('sp_updateUser',('',_userEmail,_userPassword))#_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
               # return {'Email': args['email'], 'Password': args['password']}
                return json.dumps(args).strip("\\")
            else:
                return json.dumps({'error':str(data[0])})    

        except Exception as e: 
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()
api.add_resource(UpdateUser, '/UpdateUser')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    #app.run(debug=True,)
    app.run(host="0.0.0.0")