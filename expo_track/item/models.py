from ..app import db
from ..utils import get_current_time

class Item(db.Model):
    'An item under control of a team that can be checkout'

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(1024))

    # Current status of item, should match newest action on item
    status = db.Column(db.Integer, nullable=False)
    
    # Arbitrary number for tracking item
    tracking_number = db.Column(db.Integer)

    owner = db.relationship('Team', backref=db.backref('owned_items', lazy='dynamic'))
    owner_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    actions = db.relationship('Action', backref=db.backref('item'), cascade='all, delete, delete-orphan')

class Action(db.Model):
    'An action performed by an individual on an item at an event'

    __table_name__ = 'action'

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    # When action occurred, leave null to get current time
    date = db.Column(db.DateTime, default=get_current_time, nullable=False)

    # What status changed on the item
    status = db.Column(db.Integer, nullable=False)

    # Arbitrary note, such as to explain a missing item
    note = db.Column(db.String(1024))

    # Who performed the action
    person = db.relationship('Person', backref=db.backref('actions', lazy='dynamic'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    # Which event this event is related to
    event = db.relationship('Event', backref=db.backref('actions', lazy='dynamic'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    # Location where this action occurred
    location = db.relationship('Location', backref=db.backref('actions', lazy='dynamic'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
