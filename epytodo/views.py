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

def check_user_exists(username: str):
    temp: str = None
    try:
        cursor = connect.cursor()
        cursor.execute("SELECT COUNT(1) FROM user WHERE username = '{}';".format(username))
        temp = cursor.fetchall()
        cursor.close
        connect.close
        if int(temp[0][0]) > 0:
            return True
        else:
            return False
    except Exception as error:
        print(error)

@app.route('/register', methods=['POST'])
def register_user():
    result:dict = {}
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        if (check_user_exists(username) == True):
            result['error'] = "account already exists"
            return jsonify(result)
        else:
            cursor = connect.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES ('{}', '{}');".format(username, password))
            connect.commit()
            cursor.close
            connect.close
            result['result'] = "account created"
            return jsonify(result)
    except Exception as error:
        print(error)
        result['error'] = "internal error"
        return jsonify(result)

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
            cursor.execute("INSERT INTO task (title, begin, end, status) VALUES ({}, {}, {}, {});".format(title, begin, end, status))
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

def check_is_correct_password(username: str, password: str):
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(1) FROM user WHERE username = '{}';".format(username))
    result = cursor.fetchall()
    cursor.close
    connect.close
    if result[0][0] > 0 and get_password(username) == password:
        return True
    else:
        return False

def get_password(username: str):
    cursor = connect.cursor()
    cursor.execute("SELECT password FROM user WHERE username = '{}';".format(username))
    password = cursor.fetchall()
    cursor.close
    connect.close
    return(password[0][0])

@app.route('/signin', methods=['POST'])
def signin_user():
    result: dict = {}
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        print(check_is_correct_password(username, password))
        if (check_is_correct_password(username, password) and app.config['IS_SIGNED'] == False):
            app.config['IS_SIGNED'] = True
            result['result'] = "signin successful"
            return jsonify(result)
        elif app.config['IS_SIGNED']:
            result['error'] = "you're already signed"
            return jsonify(result)
        else:
            result['error'] = "login or password does not match"
            return jsonify(result)
    except Exception as error:
        print(error)
        result['error'] = "internal error"
        return jsonify(result)

@app.route('/signout', methods=['POST'])
def signout_user():
    try:
        if app.config['IS_SIGNED'] == 1:
            app.config['IS_SIGNED'] = 0
            return "signout successfull"
        else:
            return "you must be logged"
    except Exception as error:
        print("Error: ", error)
        return "error"

if __name__ == "__main__":
    app.run()