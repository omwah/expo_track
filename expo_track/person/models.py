from ..app import db

class Person(db.Model):
    'An individual somehow involved with items, with optional contact information'

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)

    given_name = db.Column(db.String(128), nullable=False)
    family_name = db.Column(db.String(128))

    contacts = db.relationship('Contact', backref=db.backref('person'), cascade='all, delete, delete-orphan')

class Contact(db.Model):
    'Contact information for a person'

    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    type = db.Column(db.Integer)

    address = db.Column(db.String(512))
    phone_number = db.Column(db.String(32))
    email_address = db.Column(db.String(256))
