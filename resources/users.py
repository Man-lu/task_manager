from flask_bcrypt import Bcrypt
from flask_restful import Resource, marshal_with, abort
from models.all_models import OwnerModel, db, app
from flask_jwt import jwt_required
from helpers import helpers

bcrypt = Bcrypt(app)


def find_by_id(user_id):
    user = OwnerModel.query.get(user_id)
    if user:
        return user
    else:
        return abort(404, message="User not available")


class Users(Resource):
    @marshal_with(helpers.resource_fields_user)
    def post(self):
        args = helpers.user_args.parse_args()
        user_exists = OwnerModel.query.all()

        for user in user_exists:
            if user.username == args['username'] or user.owner_name == args['owner_name'].title():
                return abort(404, message='user already exists')

        hashed_pass = bcrypt.generate_password_hash(args['password']).decode("utf-8")
        new_user = OwnerModel(owner_name=args["owner_name"].title(), username=args['username'],
                              password=hashed_pass)
        new_user.save_to_db()
        new_user.password = args['password']
        return new_user, 201

    @marshal_with(helpers.resource_fields_user)
    def get(self):
        owners = OwnerModel.query.all()
        return owners, 200


class User(Resource):
    @jwt_required()
    @marshal_with(helpers.resource_fields_user)
    def put(self, user_id):
        user_to_update = find_by_id(user_id)
        if user_to_update:
            args = helpers.user_args.parse_args()
            user_to_update.owner_name = args['owner_name']
            user_to_update.username = args['username']
            user_to_update.password = args['password']
            db.session.commit()
            return user_to_update, 200

    @marshal_with(helpers.resource_fields_user)
    def get(self, user_id):
        user = find_by_id(user_id)
        if user:
            return user, 200
