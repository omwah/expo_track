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
    'event': fields.Nested({ 'id': fields.String,
                             'name': fields.String,
                             'uri': SafeUrlField('event') }),
    'uri': SafeUrlField('location'),
}

team_fields = {
    'id': fields.String,
    'name': fields.String,
    'members': fields.Nested({ 'id': fields.String,
                               'given_name': fields.String,
                               'family_name': fields.String,
                               'uri': SafeUrlField('person') },
                             allow_null=True),
    'primary_location': fields.Nested({ 'id': fields.String,
                                        'name': fields.String,
                                        'uri': SafeUrlField('location') }),
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

def location_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('event_id', type=int, required=True)
    return parser

class LocationListResource(Resource):

    @login_required
    @marshal_with(location_fields)
    def get(self):
        locations = Location.query.all()
        return locations

    @login_required
    @has_permission('add_location')
    @marshal_with(location_fields)
    def post(self):
        args = location_parser().parse_args()

        location = Location(name=args.name, event_id=args.event_id)

        db.session.add(location)
        db.session.commit()

        return location

class LocationResource(Resource):

    @login_required
    @marshal_with(location_fields)
    def get(self, id):
        return Location.query.filter(Location.id == id).first_or_404()

    @login_required
    @has_permission('edit_location')
    @marshal_with(location_fields)
    def put(self, id):
        args = location_parser().parse_args()
        
        location = Location.query.filter(Location.id == id).first_or_404()

        location.name = args.name
        location.event_id = args.event_id

        db.session.commit()

        return location

    @login_required
    @has_permission('delete_location')
    def delete(self, id):
        location = Location.query.filter(Location.id == id).first_or_404()

        db.session.delete(location)
        db.session.commit()

        return { 'delete': True }

def team_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('primary_location_id', type=int, required=True)
    return parser

class TeamListResource(Resource):

    @login_required
    @marshal_with(team_fields)
    def get(self):
        teams = Team.query.all()
        return teams

    @login_required
    @has_permission('add_team')
    @marshal_with(team_fields)
    def post(self):
        args = team_parser().parse_args()

        team = Team(name=args.name, primary_location_id=args.primary_location_id)

        db.session.add(team)
        db.session.commit()

        return team

class TeamResource(Resource):

    @login_required
    @marshal_with(team_fields)
    def get(self, id):
        return Team.query.filter(Team.id == id).first_or_404()

    @login_required
    @has_permission('edit_team')
    @marshal_with(team_fields)
    def put(self, id):
        args = team_parser().parse_args()
        
        team = Team.query.filter(Team.id == id).first_or_404()

        team.name = args.name
        team.primary_location_id = args.primary_location_id

        db.session.commit()
        db.session.refresh(team)

        return team

    @login_required
    @has_permission('delete_team')
    def delete(self, id):
        team = Team.query.filter(Team.id == id).first_or_404()

        db.session.delete(team)
        db.session.commit()

        return { 'delete': True }

def register_api(api):
    api.add_resource(EventListResource, '/api/events', endpoint='event_list')
    api.add_resource(EventResource, '/api/events/<int:id>', endpoint='event')

    api.add_resource(LocationListResource, '/api/locations', endpoint='location_list')
    api.add_resource(LocationResource, '/api/locations/<int:id>', endpoint='location')

    api.add_resource(TeamListResource, '/api/teams', endpoint='team_list')
    api.add_resource(TeamResource, '/api/teams/<int:id>', endpoint='team')
