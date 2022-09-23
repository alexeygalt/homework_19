from flask_restx import Resource, Namespace
from flask import request

from app.dao.model.director import DirectorSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        director_d = request.get_json()
        director_service.create(director_d)
        return 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        upload_data = request.get_json()
        if not 'id' in upload_data:
            upload_data['id'] = rid
        director_service.update(upload_data)
        return 204

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return 204

