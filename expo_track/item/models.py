from ..app import db
from ..utils import get_current_time

class Item(db.Model):
    'An item under control of a team that can be checkout'

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(1024))

    tracking_number = db.Column(db.Integer)

    owner = db.relationship('Team', backref=db.backref('owned_items', lazy='dynamic'))
    owner_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    actions = db.relationship('Action', backref=db.backref('item'))

class Action(db.Model):
    'An action performed by an individual on an item at an event'

    __table_name__ = 'action'

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    type = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=get_current_time, nullable=False)
    note = db.Column(db.String(1024))

    person = db.relationship('Person', backref=db.backref('actions', lazy='dynamic'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    event = db.relationship('Event', backref=db.backref('actions', lazy='dynamic'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    location = db.relationship('Location', backref=db.backref('actions', lazy='dynamic'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
