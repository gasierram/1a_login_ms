from flask import Flask
from flaskext.mysql import MySQL
from flask import Flask,request

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'db_login'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
@app.route("/")
def hello():
    return "Welcome to Python Flask App!"
 


@app.route("/Authenticate")
def Authenticate():
    userEmail = request.args.get('UserEmail')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where UserEmail='" + userEmail + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Logged in successfully"

if __name__ == "__main__":
    app.run()

