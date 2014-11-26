from ..app import db

team_members = db.Table('team_members',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)

class Event(db.Model):
    'An event such as an exposition or conference'

    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))

    logo_filename = db.Column(db.String(1024))

    locations = db.relationship('Location', backref=db.backref('event', lazy='dynamic'))

class Location(db.Model):
    'A location such as a room at an event'

    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

class Team(db.Model):
    'A group of people working together at a primary location'

    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)

    members = db.relationship('Person', secondary=team_members, backref=db.backref('pages', lazy='dynamic'))

    primary_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    primary_location = db.relationship('Location', backref=db.backref('teams_housed', lazy='dynamic'))
