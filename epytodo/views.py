##
## EPITECH PROJECT, 2020
## main
## File description:
## main
##

from flask import Flask, render_template, jsonify, request
import json
from .api import *
import pymysql as sql

def get_all_task_from_user():
    result: dict = {}
    data: dict = {}
    i = 0;
    if 'id' in session:
        try:
            cursor = connect.cursor()
            cursor.execute('SELECT fk_task_id FROM user_has_task WHERE fk_user_id = {};'.format(session['id']));
            temp = cursor.fetchall()
            cursor.close
            connect.close
            for ids in temp:
                cursor = connect.cursor()
                cursor.execute("SELECT * FROM task WHERE task_id = '{}';".format(ids[0]))
                temp = cursor.fetchone()
                cursor.close
                connect.close
                data['title'] = temp[1]
                data['begin'] = temp[2]
                data['end'] = temp[3]
                data['status'] = temp[4]
                result[i] = data
                i += 1
            return str(result)
        except Exception as error:
            return jsonify(error)
    else:
        result['error'] = "you must be logged in"
        return jsonify(result)

@app.route('/', methods=['GET'])
def index():
    return render_template("templates.html")

@app.route('/to_do', methods=['GET'])
def to_do():
    temp = get_all_task_from_user()
    result = json.dumps(temp)
    res = json.loads(result)
    print(res[0])
    return render_template("to_do.html")

@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/add_user', methods=['GET'])
def add_user():
    return render_template("add_user.html")

if __name__ == "__main__":
    app.run()