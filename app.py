from flask import Flask, request, jsonify
import urllib3, json, requests

app = Flask(__name__)


@app.route('/')
def getPrice():
    return ' Hello from Yfarm'