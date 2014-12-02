from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required
from sqlalchemy.sql.expression import asc, desc

from ..user.decorators import can_edit_items, can_perform_action

from models import Item, Action
from constants import STATUS_TYPES, STATUS_OPPOSITES

from ..person.api import person_fields

item_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'status': fields.String,
    'tracking_number': fields.String,
    #'owner': fields.Nested({ 'name': fields.String,
    #                         'uri': fields.Url('team') }),
    'uri': fields.Url('item'),
}

class StatusItem(fields.Raw):
    def format(self, value):
        return { 'code': value, 'name': STATUS_TYPES.get(value, None) }

action_fields = {
    'id': fields.String,
    'item': fields.Nested({ 'name': fields.String,
                            'uri': fields.Url('item') }),
    'status': StatusItem,
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
    parser.add_argument('status', type=int)

    @login_required
    @marshal_with(item_fields)
    def get(self):
        args = self.parser.parse_args()

        items_query = Item.query

        if args.status != None:
            items_query = items_query.filter(Item.status == args.status)

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
    parser = reqparse.RequestParser()
    parser.add_argument('item_id', type=int)
    parser.add_argument('status', type=int)
    parser.add_argument('ascending', type=bool, default=False)

    @login_required
    @marshal_with(action_fields)
    def get(self):
        args = self.parser.parse_args()
        
        actions_query = Action.query

        # By default newest items are returned first
        if args.ascending:
            actions_query = actions_query.order_by(asc(Action.date))
        else:
            actions_query = actions_query.order_by(desc(Action.date))

        if args.item_id != None:
            actions_query = actions_query.filter(Action.item_id == args.item_id)

        if args.status != None:
            actions_query = actions_query.filter(Action.status == args.status)

        return actions_query.all()

class ActionResource(Resource):

    @login_required
    def get(self, id):
        pass

    @login_required
    @can_perform_action
    def post(self):
        pass

class StatusDefResource(Resource):

    @login_required
    def get(self):
        return { 'types': STATUS_TYPES, 'opposites': STATUS_OPPOSITES }

def register_api(api):
    api.add_resource(ItemListResource, '/api/items', endpoint='items_list')
    api.add_resource(ItemResource, '/api/items/<int:id>', endpoint='item')
    api.add_resource(ActionListResource, '/api/actions', endpoint='actions_list')
    api.add_resource(ActionResource, '/api/actions/<int:id>', endpoint='action')
    api.add_resource(StatusDefResource, '/api/status_def', endpoint='status_def')
