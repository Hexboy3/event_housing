from flask import Blueprint, jsonify, abort, request
from ..models import Attendee_Type, attendee_rooms_table, Hotel, Room_Type, Room_Inventory, db, date_list
import sqlalchemy
bp = Blueprint('manager', __name__, url_prefix='/manager')


@bp.route('', methods=['POST'])
def add_attendee():

    if 'name' not in request.json or 'access_code' not in request.json:
        return abort(400)

    at = Attendee_Type(request.json['name'], request.json['access_code'])
    db.session.add(at)
    db.session.commit()

    if 'rooms' in request.json:
        stmt = sqlalchemy.insert(attendee_rooms_table).values(
            room_id=request.json['rooms'], attendee_id=at.id)
        db.session.execute(stmt)
        db.session.commit()

    return jsonify(at.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete_attendee(id: int):
    """
    Delete Attendee Type from records
    """

    try:
        Attendee_Type.query.filter_by(id=id).delete()

        db.session.commit()

        return jsonify(True)

    except:
        return jsonify(False)
