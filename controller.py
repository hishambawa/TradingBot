from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/get")
def test():
    return "Flask is running"

@app.route('/post',methods = ['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        print(data["test"])

        return "done"