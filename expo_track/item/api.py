from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required

from ..user.decorators import can_edit_items, can_perform_action

from models import Item, Action
from constants import ACTION_TYPES

from ..person.api import person_fields

item_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'tracking_number': fields.Fixed,
    #'owner': fields.Nested({ 'name': fields.String,
    #                         'uri': fields.Url('team') }),
    'uri': fields.Url('item'),
}

class ActionTypeItem(fields.Raw):
    def format(self, value):
        return { 'code': value, 'name': ACTION_TYPES.get(value, None) }

action_fields = {
    'id': fields.String,
    'item': fields.Nested({ 'name': fields.String,
                            'uri': fields.Url('item') }),
    'type': ActionTypeItem,
    'date': fields.DateTime(dt_format='rfc822'),
    'note': fields.String,
    'person': fields.Nested(person_fields),
    'event': fields.Nested({ 'name': fields.String,
                             'uri': fields.Url('event') }),
    #'location': fields.Nested({ 'name': fields.String,
    #                            'uri': fields.Url('location') }),
    'uri': fields.Url('action'),
}

class ItemListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('action_type', type=int)

    @login_required
    @marshal_with(item_fields)
    def get(self):
        args = self.parser.parse_args()

        items_query = Item.query

        if args.action_type != None:
            items_query = items_query.join(Action).filter(Action.type == args.action_type)

        return items_query.all()

class ItemResource(Resource):

    @login_required
    def get(self, id):
        pass

    @login_required
    @can_edit_items
    def post(self):
        pass

    @login_required
    @can_edit_items
    def put(self, id):
        pass

    @login_required
    @can_edit_items
    def delete(self, id):
        pass

class ActionListResource(Resource):

    @login_required
    @marshal_with(action_fields)
    def get(self):
        actions = Action.query.all()
        return actions

class ActionResource(Resource):

    @login_required
    def get(self, id):
        pass

    @login_required
    @can_perform_action
    def post(self):
        pass

class ActionTypeResource(Resource):

    @login_required
    def get(self):
        return ACTION_TYPES

def register_api(api):
    api.add_resource(ItemListResource, '/api/items', endpoint='items_list')
    api.add_resource(ItemResource, '/api/items/<int:id>', endpoint='item')
    api.add_resource(ActionListResource, '/api/actions', endpoint='actions_list')
    api.add_resource(ActionResource, '/api/actions/<int:id>', endpoint='action')
    api.add_resource(ActionTypeResource, '/api/action_types', endpoint='action_types')

