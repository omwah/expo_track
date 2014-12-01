from flask.ext.restful import Resource, fields, marshal_with
from flask.ext.login import login_required

from ..user.decorators import can_edit_people

from models import Person, Address, Phone, Email

person_fields = {
    'id': fields.String,
    'given_name': fields.String,
    'family_name': fields.String,
    'uri': fields.Url('person'),
}

class PeopleListResource(Resource):

    @login_required
    @marshal_with(person_fields)
    def get(self):
        people = Person.query.all()
        return people

class PersonResource(Resource):

    @login_required
    def get(self, id):
        pass

def register_api(api):
    api.add_resource(PeopleListResource, '/api/people', endpoint='people_list')
    api.add_resource(PersonResource, '/api/people/<int:id>', endpoint='person')
