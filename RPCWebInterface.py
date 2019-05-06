from flask import Flask
from flask import request

from RPCHandler import RPCHandler
from uuid import uuid4

app = Flask(__name__)

handler = RPCHandler()

@app.route("/math", methods=["POST"])
def math():
    return handler.request(request.get_json())

@app.route("/test", methods=["GET"])
def test():
    return 'hello world'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)