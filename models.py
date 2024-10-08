from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

users_pets = db.Table('users_pets', 
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key = True),
    db.Column('pets_id', db.Integer, db.ForeignKey('pets.id'), primary_key = True)
)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(80), nullable=False)
    comuna = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    cellphone = db.Column(db.Integer, nullable=True)
    password = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(50), nullable=True)
    owned_pets = db.relationship('Pets', secondary = users_pets, backref = 'users')
    
    def serialize(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
            'direction': self.direction,
            'comuna': self.comuna,
            'region': self.region,
            'cellphone': self.cellphone,  
            'password': self.password,  
            'image': self.image,
            'owned_pets': [pet.serialize() for pet in self.owned_pets]
        }


class Pets(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    animal = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    # vaccines_pet = db.relationship('Vaccines', backref='pet_vaccines', db.ForeignKey('vaccines.id'))
    vaccines_id = db.Column('vaccines', db.Integer, db.ForeignKey('vaccines.id'))
    # dewormings_pet = db.relationship('Deworming', backref='pet_dewormings', db.ForeingKey('dewormings.id'))
    dewormings_id = db.Column('dewormings', db.Integer, db.ForeignKey('dewormings.id'))
    # weights_pet = db.relationship('weight', backref='pet_weights', db.ForeingKey = 'Weights.id')
    weights_pet_id = db.Column('weight_control', db.Integer, db.ForeignKey('weight_control.id'))
    # med_historys_pet = db.relationship('med_history', backref='pet_med_historys', db.ForeingKey = 'Med_historys.id')
    medical_history_id = db.Column('medical_history', db.Integer, db.ForeignKey('medical_history.id'))
    # events_pet = db.relationship('event', backref='pet_events', db.ForeingKey = 'Events.id')
    events_id = db.Column('events', db.Integer, db.ForeignKey('events.id'))
    related_users = db.relationship('Users', secondary = users_pets, backref = 'pets_linked')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'animal': self.animal,
            'race': self.race,
            'birthday': self.birthday,
            'image': self.image,
            'vaccines_pet': [vaccine.serialize() for vaccine in self.vaccines_pet],
            'dewormings_pet': [deworming.serialize() for deworming in self.dewormings_pet],
            'weights_pet': [weight.serialize() for weight in self.weights_pet],
            'medical_history_pet': [medical_history.serialize() for medical_history in self.medical_history_pet],
            'events_pet': [events.serialize() for event in self.events_pet],
            'related_users': [user.serialize() for user in self.related_users]
        }


class Vaccines(db.Model):
    __tablename__ = "vaccines"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    vaccine = db.Column(db.String(50), nullable=False)
    next_vaccine = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_vaccines')

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'weight': self.weight,
            'vaccine': self.vaccine,
            'next_vaccine': self.next_vaccine,
            'image': self.image
        }


class Dewormings(db.Model):
    __tablename__ = "dewormings"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    medicine = db.Column(db.Integer, nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    next_deworming = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_dewormings')
        
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'medicine': self.medicine,
            'dose': self.vaccine,
            'weight': self.weight,
            'next_deworming': self.next_deworming
        }


class Weight_control(db.Model):
    __tablename__ = "weight_control"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    food = db.Column(db.Integer, nullable=False)
    food_dose = db.Column(db.String(50), nullable=False)
    water_dose = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_weight_control')

    
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'weight': self.weight,
            'food': self.food,
            'food_dose': self.food_dose,
            'water_dose': self.water_dose
        }


class Medical_history(db.Model):
    __tablename__ = "medical_history"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    food = db.Column(db.Integer, nullable=False)
    food_dose = db.Column(db.String(50), nullable=False)
    water_dose = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_medical_history')
    
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'weight': self.weight,
            'food': self.food,
            'food_dose': self.food_dose,
            'water_dose': self.water_dose
        }


class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    event_time = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    pets = db.relationship('Pets', backref='pets_events')
        
    def serialize(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'event_time': self.event_time,
            'duration': self.duration
        }


