from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required

from ..app import db
from ..utils import SafeUrlField
from ..user.decorators import has_permission

from models import Person, Address, Phone, Email

person_fields = {
    'id': fields.String,
    'given_name': fields.String,
    'family_name': fields.String,
    'uri': SafeUrlField('person'),
}

class PeopleListResource(Resource):

    @login_required
    @marshal_with(person_fields)
    def get(self):
        people = Person.query.all()
        return people

    @login_required
    @has_permission('add_person')
    @marshal_with(person_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('given_name', type=str, required=True)
        parser.add_argument('family_name', type=str, required=True)
        args = parser.parse_args()

        person = Person(given_name=args.given_name, 
                        family_name=args.family_name)

        db.session.add(person)
        db.session.commit()

        return person


class PersonResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('given_name', type=str, required=True)
    parser.add_argument('family_name', type=str, required=True)

    @login_required
    def get(self, id):
        return Person.query.filter(Person.id == id).first_or_404()

    @login_required
    @has_permission('edit_person')
    @marshal_with(person_fields)
    def put(self, id):
        args = self.parser.parse_args()

        person = Person.query.filter(Person.id == id).first_or_404()

        person.family_name = args.family_name
        person.given_name = args.given_name

        db.session.commit()

        return person

    @login_required
    @has_permission('delete_person')
    def delete(self, id): 
        person = Person.query.filter(Person.id == id).first_or_404()

        db.session.delete(person);
        db.session.commit();

        return { 'delete': True }

def register_api(api):
    api.add_resource(PeopleListResource, '/api/people', endpoint='people_list')
    api.add_resource(PersonResource, '/api/people/<int:id>', endpoint='person')
