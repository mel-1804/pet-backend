from datetime import datetime
from flask import request, jsonify
import os
from datetime import timedelta
import cloudinary
import cloudinary.uploader
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Users, Pets, Vaccines, Dewormings, Weight_control, Medical_history, UserCalendarEvent
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mibasededatos.db'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

expire = timedelta(minutes=60)

# --------------------------------------------HOME


@app.route('/', methods=['GET'])
def home():
    return "Welcome"

# ---------------------------------------------GET

@app.route('/getUser/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = Users.query.filter_by(id=id).first()

    return jsonify({
        'status': 'Success',
        'data': user.serialize()
    }), 201


@app.route('/getPet/<int:id>', methods=['GET'])
def get_pet_by_id(id):
    pet = Pets.query.filter_by(id=id).first()

    return jsonify({
        'status': 'Success',
        'data': pet.serialize()
    }), 201


@app.route('/getVaccine/<int:id>', methods=['GET'])
def get_vaccine_by_id(id):
    vaccine = Vaccines.query.filter_by(id=id).first()

    return jsonify({
        'status': 'Success',
        'data': vaccine.serialize()
    }), 201


@app.route('/getVaccinesByPet/<int:pet_id>', methods=['GET'])
def get_vaccines_by_pet(pet_id):
    vaccines = Vaccines.query.filter_by(pet_id=pet_id).all()

    return jsonify({
        'status': 'Success',
        'data': [vaccine.serialize() for vaccine in vaccines]
    }), 200


@app.route('/getDeworming/<int:id>', methods=['GET'])
def get_deworming_by_id(id):
    deworming = Dewormings.query.filter_by(id=id).first()

    return jsonify({
        'status': 'Success',
        'data': deworming.serialize()
    }), 201


@app.route('/getDewormingsByPet/<int:pet_id>', methods=['GET'])
def get_dewormings_by_pet(pet_id):
    dewormings = Dewormings.query.filter_by(pet_id=pet_id).all()

    return jsonify({
        'status': 'Success',
        'data': [deworming.serialize() for deworming in dewormings]
    }), 200


@app.route('/getWeight_control/<int:id>', methods=['GET'])
def get_weight_control_by_id(id):
    weight_control = Weight_control.query.filter_by(id=id).first()

    return jsonify({
        'status': 'Success',
        'data': weight_control.serialize()
    }), 201


@app.route('/getMedical_history/<int:id>', methods=['GET'])
def get_medical_history_by_id(id):
    medical_history = Medical_history.query.filter_by(id=id).first()

    return jsonify({
        'status': 'Success',
        'data': medical_history.serialize()
    }), 201


@app.route('/getEventsByUserId/<int:id>', methods=['GET'])
def get_events_by_user_id(id):
    events = UserCalendarEvent.query.filter_by(
        user_id=id).all()
    serialized_events = [event.serialize() for event in events]
    return jsonify(serialized_events), 200




# --------------------------------------------POST

@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.form
    image = request.files.get('image')

    user_exists = Users.query.filter_by(email=data['email']).first()

    if user_exists:
        return {
            'message': 'User already exists',
        }, 409

    try:
        user = Users()
        user.rut = data['rut']
        user.name = data['name']
        user.lastName = data['lastName']
        user.email = data['email']
        user.password = bcrypt.generate_password_hash(data['password'])
        user.direction = data['direction']
        user.comuna = data['comuna']
        user.region = data['region']
        user.cellphone = data['cellphone']
        password_hash = bcrypt.generate_password_hash(data['password'])
        user.password = password_hash

        if image:
            upload_result = cloudinary.uploader.upload(
                image, folder='petCenter/users', fetch_format="auto", quality="auto", width=500, crop="fill", height=500)

            user.image = upload_result['secure_url']

        db.session.add(user)
        db.session.commit()
        token = create_access_token(
            identity=user.serialize(), expires_delta=expire)

        return {
            'message': 'User created successfully',
            'token': token,
            'user': user.serialize()
        }, 201

    except Exception as e:
        print(f"Error: upload image to Cloudinary: {e}")
        return {
            'message': 'Error uploading image',
            'error': str(e)
        }, 500


@app.route('/updateUser', methods=['POST'])
def update_user():
    data = request.form
    image = request.files.get('image')

    user = Users.query.filter_by(id=data['user_id']).first()
    if not user:
        return {
            'message': 'User not found',
        }, 404

    user.name = data.get('name', user.name)
    user.lastName = data.get('lastName', user.lastName)

    try:
        if image:
            if user.image:
                public_id = user.image.split(
                    '/')[-1].split('.')[0]
                cloudinary.uploader.destroy(public_id)

            upload_result = cloudinary.uploader.upload(
                image, folder='petCenter/users', fetch_format="auto", quality="auto", width=500, crop="fill", height=500
            )
            user.image = upload_result['secure_url']

        db.session.commit()
        token = create_access_token(
            identity=user.serialize(), expires_delta=expire)

        return {
            'message': 'User updated successfully',
            'token': token,
            'user': user.serialize()
        }, 200

    except Exception as e:
        print(f"Error updating image in Cloudinary: {e}")
        return {
            'message': 'Error updating user or image',
            'error': str(e)
        }, 500


@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if user:
            user.is_active = False

            db.session.commit()
            return jsonify({"message": "User has been deactivated."}), 200
        else:
            return jsonify({"error": "User not found."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deactivating user: {str(e)}"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Users.query.filter_by(email=data['email']).first()

    if not user.is_active:
        return jsonify({'message': 'Invalid email or password',
                        'status': 'Failed'}), 401

    if user is not None:
        if bcrypt.check_password_hash(user.password, data['password']):
            token = create_access_token(
                identity=user.serialize(), expires_delta=expire)

            return jsonify({'status': 'Success', 'data': user.serialize(), 'token': token}), 200
        else:
            return jsonify({'message': 'Invalid email or password', 'status': 'Failed'}), 401
    else:
        return jsonify({'message': 'Invalid email or password', 'status': 'Failed'}), 401


@app.route('/createPet', methods=['POST'])
def create_pet():
    data = request.form
    image = request.files.get('image')
    pet = Pets()
    user = Users.query.filter_by(id=data['user_id']).first()

    pet.name = data['name']
    pet.animal = data['animal']
    pet.race = data['race']
    pet.birthday = data['birthday']
    if image:
        upload_result = cloudinary.uploader.upload(
            image, folder='petCenter/pets', fetch_format="auto", quality="auto", width=500, crop="fill", height=500)

        pet.image = upload_result['secure_url']

    user.owned_pets.append(pet)

    db.session.add(pet)
    db.session.commit()

    return {
        'message': 'Pet created successfully',
        "data": user.serialize()
    }, 201



    


@app.route('/createVaccine', methods=['POST'])
def create_vaccine():
    data = request.form
    image = request.files.get('image')

    try:
        vaccine = Vaccines()
        vaccine.pet_id = data['pet_id']
        vaccine.date = data['date']
        vaccine.weight = data['weight']
        vaccine.vaccine = data['vaccine']
        vaccine.next_vaccine = data['nextVaccine']

        if image:
            try:
                upload_result = cloudinary.uploader.upload(
                    image, folder='petCenter/vaccine', fetch_format="auto", quality="auto", width=500)

                vaccine.image = upload_result.get('secure_url')
            except Exception as img_error:
                return jsonify({
                    'message': 'Error uploading image to Cloudinary',
                    'error': str(img_error)
                }), 400
        else:
            vaccine.image = data.get('image')

        db.session.add(vaccine)
        db.session.commit()

        return jsonify({
            'message': 'Vaccine created successfully',
            'data': vaccine.serialize()
        }), 201

    except Exception as e:
        print(f"Error creating vaccine record: {e}")
        return jsonify({
            'message': 'Error creating vaccine record',
            'error': str(e)
        }), 400


@app.route('/createDeworming', methods=['POST'])
def create_deworming():
    data = request.json
    deworming = Dewormings()

    deworming.pet_id = data['pet_id']
    deworming.date = data['date']
    deworming.medicine = data['medicine']
    deworming.dose = data['dose']
    deworming.weight = data['weight']
    deworming.next_deworming = data['nextDeworming']

    db.session.add(deworming)
    db.session.commit()

    return {
        'message': 'Deworming created successfully'
    }, 201


@app.route('/createWeight_control', methods=['POST'])
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


@app.route('/createMedical_history', methods=['POST'])
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


@app.route('/createEvents/<int:id>', methods=['POST'])
def create_event(id):
    data = request.json
    user_id = data.get('user_id')
    description = data.get('description')
    event_date = datetime.fromisoformat(data.get('event_date'))

    new_event = UserCalendarEvent(
        user_id=user_id,
        description=description,
        event_date=event_date,
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.serialize()), 200




# ---------------------------------------------PUT

@app.route('/updateEvent/<int:event_id>', methods=["PUT"])
def update_event(event_id):
    data = request.json
    user_id = data.get('user_id')
    event = UserCalendarEvent.query.get(event_id)

    if event and event.user_id == user_id:
        if 'date' in data:
            event.date = data['date']
        if 'description' in data:
            event.description = data['description']

        db.session.commit()

        events = UserCalendarEvent.query.filter_by(user_id=user_id).all()
        serialized_events = [event.serialize() for event in events]

        return jsonify({
            "message": "Evento actualizado con éxito",
            "events": serialized_events
        }), 200
    else:
        return jsonify({"error": "Evento no encontrado o no pertenece al usuario"}), 404




#--------------------------------------------------------DELETE

@app.route('/deletePet', methods=['DELETE'])
def delete_pet():
    try:
        data = request.json
        pet_id = data.get('petId')
        user_id = data.get('userId')

        user = Users.query.filter_by(id=user_id).first()
        pet = Pets.query.filter_by(id=pet_id).first()

        if not user or not pet:
            return jsonify({"message": "User or pet not found"}), 404

        if pet.image:
            public_id = pet.image.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(f'petCenter/pets/{public_id}')

        db.session.delete(pet)
        db.session.commit()

        updated_user = user.serialize()

        return jsonify({
            "message": "Pet deleted successfully",
            "data": updated_user
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@app.route('/deleteEvent/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    data = request.json
    user_id = data.get('user_id')
    event = UserCalendarEvent.query.get(event_id)

    if event and event.user_id == user_id:
        db.session.delete(event)
        db.session.commit()

        remaining_events = UserCalendarEvent.query.filter_by(
            user_id=user_id).all()
        serialized_events = [event.serialize() for event in remaining_events]

        return jsonify({
            "message": "Evento eliminado con éxito",
            "events": serialized_events
        }), 200
    else:
        return jsonify({"error": "Evento no encontrado o no pertenece al usuario"}), 404



if __name__ == "__main__":
    app.run(host='localhost', port=5004, debug=True)
