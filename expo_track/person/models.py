from ..app import db

class Person(db.Model):
    'An individual somehow involved with items, with optional contact information'

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)

    given_name = db.Column(db.String(128), nullable=False)
    family_name = db.Column(db.String(128))

    addresses = db.relationship('Address', backref=db.backref('person'), cascade='all, delete, delete-orphan')
    phone_numbers = db.relationship('Phone', backref=db.backref('person'), cascade='all, delete, delete-orphan')
    email = db.relationship('Email', backref=db.backref('person'), cascade='all, delete, delete-orphan')

class Address(db.Model):
    'An address of an a person'

    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    type = db.Column(db.Integer, nullable=False)

    address_1 = db.Column(db.String(128))
    address_2 = db.Column(db.String(128))
    address_3 = db.Column(db.String(128))

    city = db.Column(db.String(128))
    region = db.Column(db.String(128))
    postal_code = db.Column(db.String(16))

class Phone(db.Model):
    'A phone number of a person'

    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    type = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String(32), nullable=False)

class Email(db.Model):
    'An email address of a person'

    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    type = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(256), nullable=False)
