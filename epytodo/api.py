##
## EPITECH PROJECT, 2020
## api
## File description:
## api
##

from flask import Flask, render_template, jsonify, request
import pymysql as sql

app = Flask(__name__)
app.config.from_object('config')
connect = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='root', db='epytodo')

