from flask import Flask, render_template, request
import os
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def maison():
    print(request.get_data())
    return json.dumps(request.get_data())
if __name__ == '__main__':
    app.run(debug=True)
