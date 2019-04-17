from flask import Flask
from flask_cors import CORS
from flask import request

from RPCHandler import RPCHandler
from uuid import uuid4

app = Flask(__name__)
CORS(app)

handler = RPCHandler()

@app.route("/math", methods=["POST"])
def math():
    return handler.request(request.data)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, ssl_context='adhoc')