from flask.ext.restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required
from sqlalchemy.sql.expression import asc, desc

from ..app import db
from ..utils import SafeUrlField
from ..user.decorators import has_permission

from models import Item, Action
from constants import STATUS_TYPES, STATUS_OPPOSITES, STATUS_CHECK_IN

class StatusField(fields.Raw):
    def format(self, value):
        return { 'code': value, 'name': STATUS_TYPES.get(value, None) }

item_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'status': StatusField,
    'tracking_number': fields.String,
    'owner': fields.Nested({ 'id': fields.String,
                             'name': fields.String,
                             'uri': SafeUrlField('team') }),
    'uri': SafeUrlField('item'),
}

action_fields = {
    'id': fields.String,
    'item': fields.Nested({ 'id': fields.String,
                            'name': fields.String,
                            'uri': SafeUrlField('item') }),
    'status': StatusField,
    'date': fields.DateTime(dt_format='rfc822'),
    'note': fields.String,
    'person': fields.Nested({ 'id': fields.String,
                              'given_name': fields.String,
                              'family_name': fields.String,
                              'uri': SafeUrlField('person') }),
    'event': fields.Nested({ 'id': fields.String,
                             'name': fields.String,
                             'uri': SafeUrlField('event') }),
    'location': fields.Nested({ 'id': fields.String,
                                'name': fields.String,
                                'uri': SafeUrlField('location') },
                               allow_null=True),
    'uri': SafeUrlField('action'),
}

class ItemListResource(Resource):

    @login_required
    @marshal_with(item_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=int)
        args = parser.parse_args()

        items_query = Item.query

        if args.status != None:
            items_query = items_query.filter(Item.status == args.status)

        return items_query.all()

    @login_required
    @has_permission('add_item')
    @marshal_with(item_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('tracking_number', type=str, required=True)
        args = parser.parse_args()

        item = Item(name=args.name, tracking_number=args.tracking_number, status=STATUS_CHECK_IN)

        db.session.add(item)
        db.session.commit()

        return item

class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('tracking_number', type=str, required=True)

    @login_required
    @marshal_with(item_fields)
    def get(self, id):
        return Item.query.filter(Item.id == id).first_or_404()

    @login_required
    @has_permission('edit_item')
    @marshal_with(item_fields)
    def put(self, id):
        args = self.parser.parse_args()

        item = Item.query.filter(Item.id == id).first_or_404()
        
        item.name = args.name
        item.tracking_number = args.tracking_number

        db.session.commit()

        return item

    @login_required
    @has_permission('delete_item')
    def delete(self, id):
        item = Item.query.filter(Item.id == id).first_or_404()

        db.session.delete(item);
        db.session.commit();

        return { 'delete': True }

class ActionListResource(Resource):

    @login_required
    @marshal_with(action_fields)
    def get(self):
        # These are seperate from post() so they are not all required
        # as they just define ways to search for items
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int)
        parser.add_argument('status', type=int)
        parser.add_argument('ascending', type=bool, default=False)
        args = parser.parse_args()
        
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

    @login_required
    @has_permission('perform_action')
    @marshal_with(action_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int, required=True)
        parser.add_argument('status', type=int, required=True)
        parser.add_argument('note', type=str)
        parser.add_argument('person_id', type=int, required=True)
        parser.add_argument('event_id', type=int, required=True)
        parser.add_argument('location_id', type=int)
        args = parser.parse_args()

        # Update status of item
        item = Item.query.filter(Item.id == args.item_id).first_or_404()
        item.status = args.status

        new_action = Action(item=item,
                status=args.status, note=args.note, 
                person_id=args.person_id, event_id=args.event_id,
                location_id=args.location_id)


        db.session.add(new_action)
        db.session.commit()

        return new_action

class ActionResource(Resource):

    @login_required
    @marshal_with(action_fields)
    def get(self, id):
        return Action.query.filter(Action.id == id).first_or_404()

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
