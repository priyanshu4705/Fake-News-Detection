from flask import Flask
from app.config import DEBUG, HOST, PORT
from app.views import view

app = Flask(__name__)
app.register_blueprint(view)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
