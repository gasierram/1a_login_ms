from flaskext.mysql import MySQL
from flask import Flask, render_template, request, json, make_response
import module.database
mysql = MySQL()
app = Flask(__name__)
#app.config['MYSQL_DATABASE_HOST']       = '1a_login_db'
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = '1234'
app.config['MYSQL_DATABASE_DB']         = 'users'
mysql.init_app(app)


def conectiondb():
    cnx = mysql.connect()
    cursor = cnx.cursor()
    query = ("""CREATE DATABASE IF NOT EXISTS users;""")
    query1 = ("""DROP TABLE IF EXISTS `user`;""")
    query2 = ("""CREATE TABLE `user` ( `id` int(50) NOT NULL AUTO_INCREMENT, `username` varchar(255) DEFAULT NULL, `email` varchar(255) NOT NULL UNIQUE, `password` varchar(255) NOT  NULL, PRIMARY KEY (`id`)) ;""")
    query3 = ("""DROP TABLE IF EXISTS `usersapp`;""")
    query4 = ("""CREATE TABLE `usersapp` ( `id` int(50) NOT NULL AUTO_INCREMENT, `name` varchar(255) DEFAULT NULL, `lastname` varchar(255) DEFAULT NULL , `id_code` int NOt NULL UNIQUE, `email` varchar(255) DEFAULT NULL , `id_type` varchar(255) DEFAULT NULL, PRIMARY KEY (`id`) );""")
    query5 = ("""INSERT INTO users.user (username, email, password) 
                VALUES ("alejandrogustavo","mancera","chan")""")
    cursor.execute(query)
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    cursor.execute(query5)
    cnx.commit()
    cursor.close()
    cnx.close()