from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_helmet import FlaskHelmet
import mongoengine as db
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from Controllers.UserController import register_user
from Routes.User import user_routes
from Routes.Task import task_routes
from Routes.Admin import admin_routes
from data.tasks import tasks


app = Flask(__name__)
CORS(app, origin='http://localhost:3000', supports_credentials=True)
helmet = FlaskHelmet(app)

load_dotenv()

app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv("MONGO_DB"),
}
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.connect(host=os.getenv("MONGO_DB"))

app.register_blueprint(user_routes, url_prefix='/auth')
app.register_blueprint(task_routes, url_prefix='/task')
app.register_blueprint(admin_routes, url_prefix='/admin')

@app.route('/auth/register', methods=['POST'])
def register_user_route():
    return register_user()

@app.route('/', methods=['GET'])
def home():
    return 'This is a Flask response'

if __name__ == '__main__':
    app.run(debug=True)
