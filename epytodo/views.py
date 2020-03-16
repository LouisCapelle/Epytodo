##
## EPITECH PROJECT, 2020
## main
## File description:
## main
##

from flask import Flask, render_template
app = Flask(__name__)
app.config.from_object('config')

@app.route('/connection')
def connetion():
    return 'connection'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()