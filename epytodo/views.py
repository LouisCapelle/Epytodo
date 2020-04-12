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

@app.route('/', methods=['GET'])
def index():
    return render_template("templates.html")

@app.route('/to_do', methods=['GET'])
def to_do():
    return render_template("to_do.html")

@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/add_user', methods=['GET'])
def add_user():
    return render_template("add_user.html")

if __name__ == "__main__":
    app.run()