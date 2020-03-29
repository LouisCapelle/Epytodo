##
## EPITECH PROJECT, 2020
## main
## File description:
## main
##

from flask import Flask, render_template, jsonify, request
import pymysql as sql

app = Flask(__name__)
app.config.from_object('config')
connect = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='root', db='epytodo')

@app.route('/connection')
def connetion():
    return 'connection'

@app.route('/users')
def get_all_users():
    result = ""
    try: 
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
        cursor = connect.cursor()
        cursor.execute("SELECT * from task")
        result = cursor.fetchall()
        cursor.close
        connect.close
    except Exception as error:
        print("Error: ", error)
        return (error)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register_user():
    result = ""
    data = request.get_json()
    if request.method == 'POST':
        try:
            username = data['username']
            password = data['password']
            cursor = connect.cursor()
            cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)', (username, password))
            connect.commit()
            cursor.close
            connect.close
            return "REGISTER_RES"
        except Exception as error:
            print("Error: ", error)
            return "REGISTER_ERR"
    else:
        return "REGISTER_ERR"
    return 0

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()