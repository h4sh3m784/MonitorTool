from flask import Flask
from flask import request

from RPCHandler import RPCHandler
from uuid import uuid4
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

handler = RPCHandler()

@app.route("/math", methods=["POST"])
def math():
    logging.debug(request.data + " " + "first")
    return handler.request(request.data)

@app.route("/test", methods=["GET"])
def test():
    return 'hello world'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)