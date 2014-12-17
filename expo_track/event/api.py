from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required

from ..app import db
from ..utils import SafeUrlField
from ..user.decorators import has_permission

from models import Event, Location, Team

event_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'uri': SafeUrlField('event'),
}

location_fields = {
    'id': fields.String,
    'name': fields.String,
    'event_id': fields.String,
    'uri': SafeUrlField('location'),
}

team_fields = {
    'id': fields.String,
    'name': fields.String,
    'members': fields.Nested({ 'given_name': fields.String,
                              'family_name': fields.String,
                              'uri': SafeUrlField('person') }),
    'primary_location': fields.Nested(location_fields),
    'uri': SafeUrlField('team'),
}

def event_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str)
    return parser

class EventListResource(Resource):

    @login_required
    @marshal_with(event_fields)
    def get(self):
        events = Event.query.all()
        return events

    @login_required
    @has_permission('add_event')
    @marshal_with(event_fields)
    def post(self):
        args = event_parser().parse_args()

        event = Event(name=args.name, description=args.description)

        db.session.add(event)
        db.session.commit()

        return event

class EventResource(Resource):

    @login_required
    @marshal_with(event_fields)
    def get(self, id):
        return Event.query.filter(Event.id == id).first_or_404()

    @login_required
    @has_permission('edit_event')
    @marshal_with(event_fields)
    def put(self, id):
        args = event_parser().parse_args()
        
        event = Event.query.filter(Event.id == id).first_or_404()

        event.name = args.name
        event.description = args.description

        db.session.commit()

        return event

    @login_required
    @has_permission('delete_event')
    def delete(self, id):
        event = Event.query.filter(Event.id == id).first_or_404()

        db.session.delete(event)
        db.session.commit()

        return { 'delete': True }

class LocationResource(Resource):

    @login_required
    def get(self, id):
        pass

class TeamResource(Resource):

    @login_required
    def get(self, id):
        pass

def register_api(api):
    api.add_resource(EventListResource, '/api/events', endpoint='event_list')
    api.add_resource(EventResource, '/api/events/<int:id>', endpoint='event')

    api.add_resource(LocationResource, '/api/locations/<int:id>', endpoint='location')

    api.add_resource(TeamResource, '/api/teams/<int:id>', endpoint='team')
