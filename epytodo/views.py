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

@app.route('/', methods=['GET'])
def index():
    return render_template("templates.html")

@app.route('/add_user', methods=['GET'])
def add_user():
    return render_template("add_user.html")

if __name__ == "__main__":
    app.run()