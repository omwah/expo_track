from flask.ext.restful import Resource, fields, marshal_with
from flask.ext.login import login_required

from ..user.decorators import can_edit_items, can_perform_action

from models import Item, Action
from constants import ACTION_TYPES

item_fields = {
    'name': fields.String,
    'description': fields.String,
    'tracking_number': fields.Fixed,
    'owner': fields.Nested({ 'name': fields.String,
                             'uri': fields.Url('team') }),
    'uri': fields.Url('item')
}

class ActionTypeItem(fields.Raw):
    def format(self, value):
        return { 'code': value, 'name': ACTION_TYPES.get(value, None) }

action_fields = {
    'item': fields.Nested({ 'name': fields.String,
                            'uri': fields.Url('item') }),
    'type': ActionTypeItem,
    'date': fields.DateTime(dt_format='rfc822'),
    'note': fields.String,
    'person': fields.Nested({ 'given_name': fields.String,
                              'family_name': fields.String,
                              'uri': fields.Url('person') }),
    'event': fields.Nested({ 'name': fields.String,
                             'uri': fields.Url('event') }),
    #'location': fields.Nested({ 'name': fields.String,
    #                            'uri': fields.Url('location') }),
    'uri': fields.Url('action'),
}

class ItemListResource(Resource):

    @login_required
    def get(self):
        pass

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

def register_api(api):
    api.add_resource(ItemListResource, '/api/items', endpoint='item_list')
    api.add_resource(ItemResource, '/api/items/<int:id>', endpoint='item')
    api.add_resource(ActionListResource, '/api/actions', endpoint='action_list')
    api.add_resource(ActionResource, '/api/actions/<int:id>', endpoint='action')
