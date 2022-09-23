from flask_restx import Resource, Namespace
from flask import request

from app.dao.model.user import users_schema, user_schema
from app.helpers.decorators import admin_required
from app.implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @admin_required
    def get(self):
        return users_schema.dump(user_service.get_all()), 200

    def post(self):
        upload_data = request.get_json()
        user_service.create(upload_data)
        return 201


@user_ns.route('/<int:uid>')
class UsersView(Resource):
    @admin_required
    def get(self, uid):
        return user_schema.dump(user_service.get_one(uid))

    @admin_required
    def put(self, uid):
        upload_data = request.get_json()
        if 'id' not in upload_data:
            upload_data['id'] = uid
        user_service.update(upload_data)
        return 201

    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return 204
