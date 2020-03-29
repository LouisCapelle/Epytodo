##
## EPITECH PROJECT, 2020
## main
## File description:
## main
##

from flask import Flask, render_template, jsonify
import pymysql as sql

app = Flask(__name__)
app.config.from_object('config')

@app.route('/connection')
def connetion():
    return 'connection'

@app.route('/users')
def get_all_users():
    result = ""
    try: 
        connect = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='root', db='epytodo')
        cursor = connect.cursor()
        cursor.execute("SELECT * from user")
        result = cursor.fetchall()
        cursor.close
        connect.close
    except Exception as e:
        print("Error: ", e)  
    return jsonify(result)

@app.route('/tasks')
def get_all_tasks():
    result = ""
    try: 
        connect = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='root', db='epytodo')
        cursor = connect.cursor()
        cursor.execute("SELECT * from task")
        result = cursor.fetchall()
        cursor.close
        connect.close
    except Exception as e:
        print("Error: ", e)
    print(result)
    return jsonify(result)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()