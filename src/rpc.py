from flask import Flask
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)

@app.route("/math", methods=["POST"])
def math():
    data = request.data
    print(data)
    return str(add())

def add():
    return 1 + 1

if __name__ == "__main__":
    app.run("127.0.0.1", 5000)