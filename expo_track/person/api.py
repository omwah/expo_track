from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required

from ..app import db
from ..utils import SafeUrlField
from ..user.decorators import has_permission

from models import Person, Contact

contact_fields = {
    'id': fields.String,
    'type': fields.String,
    'address': fields.String,
    'phone_number': fields.String,
    'email_address': fields.String,
}

person_fields = {
    'id': fields.String,
    'given_name': fields.String,
    'family_name': fields.String,
    'contacts': fields.Nested(contact_fields, allow_null=True),
    'uri': SafeUrlField('person'),
}

def person_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('given_name', type=str, required=True)
    parser.add_argument('family_name', type=str, required=True)
    parser.add_argument('contacts', type=dict, action='append')
    return parser

def contact_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=int, default=0)
    parser.add_argument('address', type=str)
    parser.add_argument('phone_number', type=str)
    parser.add_argument('email_address', type=str)
    return parser

def modify_contacts(person, contacts_dict):
    "Modifies the contacts from the client by overwriting contact items"

    parsed_contacts = []
    if contacts_dict != None:
        for contact in contacts_dict:
            parser = contact_parser()
            # Fake request object that RequestParser can pull items out of
            class ContactRequest(object):
                values = contact

            parsed_contacts.append(parser.parse_args(req=ContactRequest()))

    # Make number of items equal
    if len(parsed_contacts) < len(person.contacts):
        for count in range(len(person.contacts) - len(parsed_contacts)):
            person.contacts.pop()
    elif len(parsed_contacts) > len(person.contacts):
        for count in range(len(parsed_contacts) - len(person.contacts)):
            person.contacts.append(Contact(type=0))
 
    # Now copy from the parsed arguments into the Person object
    for db_contact, parsed_contact in zip(person.contacts, parsed_contacts):
        db_contact.type = parsed_contact.type
        db_contact.address = parsed_contact.address
        db_contact.phone_number = parsed_contact.phone_number
        db_contact.email_address = parsed_contact.email_address

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
        args = person_parser().parse_args()

        person = Person(given_name=args.given_name, 
                        family_name=args.family_name)

        modify_contacts(person, args.contacts)

        db.session.add(person)
        db.session.commit()

        return person


class PersonResource(Resource):

    @login_required
    @marshal_with(person_fields)
    def get(self, id):
        return Person.query.filter(Person.id == id).first_or_404()

    @login_required
    @has_permission('edit_person')
    @marshal_with(person_fields)
    def put(self, id):
        args = person_parser().parse_args()

        person = Person.query.filter(Person.id == id).first_or_404()

        person.family_name = args.family_name
        person.given_name = args.given_name

        modify_contacts(person, args.contacts)

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
