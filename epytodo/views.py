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

is_signed: bool = False

@app.route('/connection')
def connetion():
    return 'connection'

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/task/add', methods=['POST'])
def create_task():
    result = ""
    data = request.get_json()
    if request.method == 'POST':
        try:
            title = data['title']
            begin = data['begin']
            end = data['end']
            status = data['status']
            cursor = connect.cursor()
            cursor.execute('INSERT INTO task (title, begin, end, status) VALUES (%s, %s, %s, %s)', (title, begin, end, status))
            connect.commit()
            cursor.close
            connect.close
            return "TASK_ID_ADD_RES"
        except Exception as error:
            print("Error: ", error)
            return "TASK_ID_ADD_ERR"
    else:
        return "TASK_ID_ADD_ERR"
    return 0

@app.route('/task/<int:id>', methods=['GET'])
def view_task_id(id):
    result: str = None
    try:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM task WHERE task_id = '{}';".format(id))
        result = cursor.fetchall()
        cursor.close
        connect.close
        if result:
            return jsonify(result)
        else:
            return "error"
    except Exception as error:
        print("Error: ", error)
        return "error"

def check_user(username: str, password: str):
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(1) FROM user WHERE username = '{}';".format(username))
    result = cursor.fetchall()
    cursor.close
    connect.close
    if result:
        if (check_password(username) == password):
            return True
    else:
        return False

def check_password(username: str):
    cursor = connect.cursor()
    cursor.execute("SELECT password FROM user WHERE username = '{}'".format(username))
    password = cursor.fetchall()
    cursor.close
    connect.close
    return(password[0][0])
    

@app.route('/signin', methods=['POST'])
def signin_user():
    result: str = None
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        check_user(username, password)
        if check_user(username, password):
            is_signed = True
            return "signin successful"
        else:
            return "error"
    except Exception as error:
        print("Error: ", error)
        return "error"

if __name__ == "__main__":
    app.run()