# -*- coding: utf-8 -*-
"""
@File    : fake_server.py
@Date    : 2024-03-22
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


# http://127.0.0.1:8082/issueCertificate
@app.route(rule='/issueCertificate', methods=['POST'])
def issue_certificate():
    print(request.json)
    print(request.headers)
    return jsonify({'result': 'ok'})


if __name__ == '__main__':
    app.run(port=8082)
