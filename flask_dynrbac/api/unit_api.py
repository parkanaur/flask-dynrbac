from flask_restful import Resource, abort
from flask import current_app

from flask_dynrbac.exc import DynRBACNotFoundException
from flask_dynrbac.api.argparsers import unit_update_parser, unit_create_parser


def _logic():
    return current_app.rbac.unit_logic


class UnitApi(Resource):
    def _get_or_abort(self, id):
        try:
            return _logic().get_by_id(id)
        except DynRBACNotFoundException:
            return abort(404)

    def get(self, id):
        return self._get_or_abort(id).to_dict()

    def put(self, id):
        kw = unit_update_parser.parse_args(strict=True)
        unit = self._get_or_abort(id)

        _logic().update_unit(unit, **kw)

        return '', 204

    def delete(self, id):
        unit = self._get_or_abort(id)
        _logic().delete(unit)

        return '', 204


class UnitListApi(Resource):
    def get(self):
        return [unit.to_dict() for unit in _logic().get_all()]

    def post(self):
        kw = unit_create_parser.parse_args(strict=True)
        unit = _logic().create_unit(**kw)
        return unit.to_dict()
