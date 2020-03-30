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
        cursor.close()
        connect.close()
        print(id)
        print(result)
        return jsonify(result)
    except Exception as error:
        print(id)
        print(result)
        print("Error: ", error)
        return "error"

if __name__ == "__main__":
    app.run()