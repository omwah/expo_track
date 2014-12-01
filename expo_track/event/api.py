from flask.ext.restful import Resource, fields, marshal_with
from flask.ext.login import login_required

from ..user.decorators import can_edit_events

from models import Event, Location, Team

class EventResource(Resource):

    @login_required
    def get(self, id):
        pass

class LocationResource(Resource):

    @login_required
    def get(self, id):
        pass

class TeamResource(Resource):

    @login_required
    def get(self, id):
        pass

def register_api(api):
    api.add_resource(EventResource, '/api/events/<int:id>', endpoint='event')
    api.add_resource(LocationResource, '/api/locations/<int:id>', endpoint='location')
    api.add_resource(TeamResource, '/api/teams/<int:id>', endpoint='team')
