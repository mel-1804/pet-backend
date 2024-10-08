from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Users, Pets, Vaccines, Dewormings, Weight_control, Medical_history, Events
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mibasededatos.db'
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


#--------------------------------------------HOME
@app.route('/', methods = ['GET'])
def home():
    return "Welcome"

#---------------------------------------------GET
@app.route('/createUser', methods = ['POST'])
def create_user():
    data = request.json
    user = Users()

    user.rut = data['rut']
    user.name = data['name']
    user.lastname = data['lastname']
    user.email = data['email']
    user.password = data['password']
    user.direction = data['direction']
    user.comuna = data['name']
    user.region = data['region']
    user.cellphone = data['cellphone']

    db.session.add(user)
    db.session.commit()

    return {
      'message': 'User created successfully'
    }, 201

#--------------------------------------------POST

#---------------------------------------------PUT


if __name__ == "__main__":
  app.run(host='localhost', port=5004, debug=True)