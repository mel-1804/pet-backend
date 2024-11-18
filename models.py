from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

users_pets = db.Table('users_pets',
                      db.Column('users_id', db.Integer, db.ForeignKey(
                          'users.id'), primary_key=True),
                      db.Column('pets_id', db.Integer, db.ForeignKey(
                          'pets.id'), primary_key=True)
                      )


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(80), nullable=False)
    comuna = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    cellphone = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String, nullable=False)
    image = db.Column(db.String(50), nullable=True)
    owned_pets = db.relationship('Pets', secondary=users_pets, backref='users')
    is_active = db.Column(db.Boolean, default=True)

    def serialize(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'name': self.name,
            'lastName': self.lastName,
            'email': self.email,
            'direction': self.direction,
            'comuna': self.comuna,
            'region': self.region,
            'cellphone': self.cellphone,
            'image': self.image,
            'owned_pets': [pet.serialize() for pet in self.owned_pets],
            'is_active': self.is_active
        }


class Pets(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    animal = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'animal': self.animal,
            'race': self.race,
            'birthday': self.birthday,
            'image': self.image
        }


class Vaccines(db.Model):
    __tablename__ = "vaccines"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    date = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    vaccine = db.Column(db.String(50), nullable=False)
    next_vaccine = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'date': self.date,
            'weight': self.weight,
            'vaccine': self.vaccine,
            'nextVaccine': self.next_vaccine,
            'image': self.image
        }


class Dewormings(db.Model):
    __tablename__ = "dewormings"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    date = db.Column(db.String(50), nullable=False)
    medicine = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    next_deworming = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_dewormings')

    def serialize(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'date': self.date,
            'medicine': self.medicine,
            'dose': self.dose,
            'weight': self.weight,
            'nextDeworming': self.next_deworming
        }


class Weight_control(db.Model):
    __tablename__ = "weight_control"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    date = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    food = db.Column(db.Integer, nullable=False)
    food_dose = db.Column(db.String(50), nullable=False)
    water_dose = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_weight_control')

    def serialize(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'date': self.date,
            'weight': self.weight,
            'food': self.food,
            'food_dose': self.food_dose,
            'water_dose': self.water_dose
        }


class Medical_history(db.Model):
    __tablename__ = "medical_history"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    date = db.Column(db.String(50), nullable=False)
    disease_type = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    symptoms = db.Column(db.String(50), nullable=False)
    diagnosis = db.Column(db.String(50), nullable=False)
    medicine = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    frecuency = db.Column(db.String(50), nullable=False)
    since = db.Column(db.String(50), nullable=False)
    until = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pets', backref='pets_medical_history')

    def serialize(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'date': self.date,
            'disease_type': self.disease_type,
            'area': self.area,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
            'medicine': self.medicine,
            'dose': self.dose,
            'frecuency': self.frecuency,
            'since': self.since,
            'until': self.until
        }


class UserCalendarEvent(db.Model):
    __tablename__ = "user_calendar_events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(255), nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)
    users = db.relationship('Users', backref='user_calendar_events')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'event_date': self.event_date.isoformat(),
        }
