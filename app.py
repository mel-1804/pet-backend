from flask import Flask, request, jsonify
from flask_migrate import Migrate
# from models import db, Users, Pets, Vaccines, Dewormings, Weight_control, Medical_history, Events
from models import db, Users, Pets, Vaccines
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
@app.route('/getUser/<int:id>', methods = ['GET'])
def get_user_by_id(id):
    user = Users.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': user.serialize()
    }), 201

#--------------------------------------------POST
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


@app.route('/createPet', methods = ['POST'])
def create_pet():
    data = request.json
    pet = Pets()
    user = Users.query.get(data['user_id'])

    pet.name = data['name']
    pet.animal = data['animal']
    pet.race = data['race']
    pet.birthday = data['birthday']
    pet.image = data['image']

    user.owned_pets.append(pet)
    
    db.session.add(pet)
    db.session.commit()

    return {
      'message': 'Pet created successfully'
    }, 201


@app.route('/createVaccine', methods = ['POST'])
def create_vaccine():
    data = request.json
    vaccine = Vaccines()

    vaccine.pet_id = data['pet_id']
    vaccine.date = data['date']
    vaccine.weight = data['weight']
    vaccine.vaccine = data['vaccine']
    vaccine.next_vaccine = data['next_vaccine']
    vaccine.image = data['image']
    
    db.session.add(vaccine)
    db.session.commit()

    return {
      'message': 'Vaccine created successfully'
    }, 201


@app.route('/createDeworming', methods = ['POST'])
def create_deworming():
    data = request.json
    deworming = Dewormings()

    deworming.pet_id = data['pet_id']
    deworming.date = data['date']
    deworming.medicine = data['medicine']
    deworming.dose = data['dose']
    deworming.weight = data['weight']
    deworming.next_deworming = data['next_deworming']
    
    
    db.session.add(deworming)
    db.session.commit()

    return {
      'message': 'Deworming created successfully'
    }, 201   






#---------------------------------------------PUT


if __name__ == "__main__":
  app.run(host='localhost', port=5004, debug=True)