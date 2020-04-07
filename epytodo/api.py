##
## EPITECH PROJECT, 2020
## api
## File description:
## api
##

from flask import Flask, render_template, jsonify, request, session
from datetime import timedelta
import pymysql as sql
from .views import app

connect = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='root', db='epytodo')
app.secret_key = "caca"
app.permanent_session_lifetime = timedelta(minutes = 5)

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

@app.route('/user/task/add', methods=['POST'])
def create_task():
    result: dict = {}
    data = request.get_json()
    if 'id' in session:
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
            result['result'] = "new task added"
            return jsonify(result)
        except Exception as error:
            result['error'] = "internal error"
            print(error)
            return jsonify(result)
    else:
        result['error'] = "you must be logged in"
        return jsonify(result)
    return 0

def get_task_result_json(res: str):
    result: dict = {}
    data: dict = {}
    data['title'] = res[1]
    data['begin'] = res[2]
    data['end'] = res[3]
    data['status'] = res[4]
    result['result'] = data
    return jsonify(result)

@app.route('/user/task/<int:id>', methods=['GET'])
def view_task_id(id: int):
    result: str = None
    error: dict = {}
    if 'id' in session:
        try:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM task WHERE task_id = '{}';".format(id))
            result = cursor.fetchone()
            cursor.close
            connect.close
            if result:
                return get_task_result_json(result)
            else:
                error['error'] = "task id does not exists"
                return jsonify(error)
        except Exception as error:
            print(error)
            error['error'] = "internal error"
            return jsonify(error)
    else:
        error['error'] = "you must be logged in"
        return jsonify(error)

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

def get_user_id(username: str):
    cursor = connect.cursor()
    cursor.execute("SELECT user_id FROM user WHERE username = '{}';".format(username))
    id = cursor.fetchall()
    cursor.close
    connect.close
    return(id[0][0])

@app.route('/signin', methods=['POST'])
def signin_user():
    result: dict = {}
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        if (check_is_correct_password(username, password) and 'id' not in session):
            session['id'] = get_user_id(username)
            result['result'] = "signin successful"
            return jsonify(result)
        elif 'id' in session:
            result['error'] = "you're already signed"
            return jsonify(result)
        else:
            result['error'] = "login or password does not match"
            return jsonify(result)
    except Exception as error:
        result['error'] = "internal error"
        print(error)
        return jsonify(result)

@app.route('/signout', methods=['POST'])
def signout_user():
    result: dict = {}
    try:
        if 'id' in session:
            session.pop('id', None)
            result['result'] = "signout successful"
            return jsonify(result)
        else:
            result['error'] = "you must be logged in"
            return jsonify(result)
    except Exception as error:
        result['error'] = "internal error"
        return jsonify(result)

def delete_request(id: int):
    result: dict = {}
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM task WHERE task_id = {};".format(id))
        connect.commit()
        cursor.close
        connect.close
        result['result'] = "task deleted"
        return jsonify(result)
    except Exception as error:
        result['error'] = "internal error"
        return jsonify(result)

@app.route('/user/task/del/<int:id>', methods=['POST'])
def delete_task_id(id: int):
    result: dict = {}
    if 'id' in session:
        try:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM task WHERE task_id = '{}';".format(id))
            data = cursor.fetchone()
            cursor.close
            connect.close
            if data:
                return delete_request(id)
            else:
                result['error'] = "task id does not exists"
                return jsonify(result)
        except Exception as error:
            result['error'] = "internal error"
            return jsonify(result)
    else:
        result['error'] = "you must be logged in"
        return jsonify(result)
    return

def mod_task():
    return 

@app.route('/user/task/<int:id>', methods=['POST'])
def modify_task_id(id: int):
    result: dict = {}
    data = request.get_json()
    if 'id' in session:
        try:
            cursor = connect.cursor()
            cursor.execute("UPDATE task SET title = '{}', begin = '{}', end = '{}', status = '{}' WHERE id = {};".format(id))
            data = cursor.fetchone()
            cursor.close
            connect.close
            if data:
                return mod_task(id)
            else:
                result['error'] = "task id does not exists"
                return jsonify(result)
        except Exception as error:
            result['error'] = "internal error"
            return jsonify(result)
    else:
        result['error'] = "you must be logged in"
        return jsonify(result)
    return