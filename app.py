from flask import Flask, request 
from flask_restful import Resource, Api, reqparse	
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import flash, render_template, redirect, url_for, session

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
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

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

            _hashed_password = generate_password_hash(_userPassword)

            cursor.callproc('sp_createUser',('',_userEmail,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return{'Email': args['email'], 'Password': args['password']}
            else:
                return {'error':str(data[0])}    

        except Exception as e: 
            return {'error': str(e)}
        
        finally:
            cursor.close() 
            conn.close()

api.add_resource(CreateUser, '/CreateUser')

class ReadUser(Resource):
    
    def get(self):
        try: 
            global cursor
            def Authenticate():
                userEmail = request.args.get('email')
                password = request.args.get('password')
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT * from tbl_user where email='" + userEmail + "' and password='" + password + "'")
                data = cursor.fetchone()
                if data is None:
                    return "Username or Password is wrong"
                else:
                    return "Logged in successfully"

        except Exception as e: 
            return {'error': str(e)}
        finally:
            cursor.close() 
            conn.close()

api.add_resource(ReadUser, '/ReadUser')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True,)
