from GoldStarDAL.goldstar import *
from flask import Flask, request, redirect, jsonify, render_template, url_for, session, request
app = Flask(__name__)
from json import dumps

@app.route("/")
def hello_world():
	return 'Hello!'

if __name__ == "__main__":
	app.run()
