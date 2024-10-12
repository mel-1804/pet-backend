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
@app.route('/getUser/<int:id>', methods = ['GET'])
def get_user_by_id(id):
    user = Users.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': user.serialize()
    }), 201


@app.route('/getPet/<int:id>', methods = ['GET'])
def get_pet_by_id(id):
    pet = Pets.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': pet.serialize()
    }), 201


@app.route('/getVaccine/<int:id>', methods = ['GET'])
def get_vaccine_by_id(id):
    vaccine = Vaccines.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': vaccine.serialize()
    }), 201

@app.route('/getDeworming/<int:id>', methods = ['GET'])
def get_deworming_by_id(id):
    deworming = Dewormings.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': deworming.serialize()
    }), 201


@app.route('/getWeight_control/<int:id>', methods = ['GET'])
def get_weight_control_by_id(id):
    weight_control = Weight_control.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': weight_control.serialize()
    }), 201


@app.route('/getMedical_history/<int:id>', methods = ['GET'])
def get_medical_history_by_id(id):
    medical_history = Medical_history.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': medical_history.serialize()
    }), 201


@app.route('/getEvent/<int:id>', methods = ['GET'])
def get_event_by_id(id):
    event = Events.query.filter_by(id=id).first()

    return jsonify({
      'status': 'Success',
      'data': event.serialize()
    }), 201



#--------------------------------------------POST
@app.route('/createUser', methods = ['POST'])
def create_user():
    data = request.json
    user = Users()

    user.rut = data['rut']
    user.name = data['name']
    user.lastName = data['lastName']
    user.email = data['email']
    user.password = data['password']
    user.direction = data['direction']
    user.comuna = data['comuna']
    user.region = data['region']
    user.cellphone = data['cellphone']

    db.session.add(user)
    db.session.commit()

    return {
      'message': 'User created successfully'
    }, 201

@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    user = Users.query.filter_by(email = data['email']).first()

    # print(f'este es el print {type(user.password)}, {type(data['password'])}')

    # validar que el usuario exista
    # validar que la contraseña coincida con el del usuario
    if user is not None:
      if user.password == data['password']:
        return {'status': 'Success', 'data': user.serialize()}
      else:
        return {'message': 'Invalid email or password', 'status': 'Failed'}
    else:
      return {'message': 'Invalid email or password', 'status': 'Failed'}

    

   
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

@app.route('/createWeight_control', methods = ['POST'])
def create_weight_control():
    data = request.json
    weight_control = Weight_control()

    weight_control.pet_id = data['pet_id']
    weight_control.date = data['date']
    weight_control.weight = data['weight']
    weight_control.food = data['food']
    weight_control.food_dose = data['food_dose']
    weight_control.water_dose = data['water_dose']    
    
    db.session.add(weight_control)
    db.session.commit()

    return {
      'message': 'Weight_control created successfully'
    }, 201


@app.route('/createMedical_history', methods = ['POST'])
def create_medical_history():
    data = request.json
    medical_history = Medical_history()

    medical_history.pet_id = data['pet_id']
    medical_history.date = data['date']
    medical_history.disease_type = data['disease_type']
    medical_history.area = data['area']
    medical_history.symptoms = data['symptoms']
    medical_history.diagnosis = data['diagnosis']    
    medical_history.medicine = data['medicine']    
    medical_history.dose = data['dose']    
    medical_history.frecuency = data['frecuency']    
    medical_history.since = data['since']    
    medical_history.until = data['until']    
    
    db.session.add(medical_history)
    db.session.commit()

    return {
      'message': 'Medical_history created successfully'
    }, 201      


@app.route('/createEvents', methods = ['POST'])
def create_events():
    data = request.json
    events = Events()

    events.pet_id = data['pet_id']
    events.event_type = data['event_type']
    events.when = data['when']
    events.duration = data['duration']  
    
    db.session.add(events)
    db.session.commit()

    return {
      'message': 'Events created successfully'
    }, 201


#---------------------------------------------PUT


if __name__ == "__main__":
  app.run(host='localhost', port=5004, debug=True)