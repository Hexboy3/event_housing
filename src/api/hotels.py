from flask import Blueprint, jsonify, abort, request
from ..models import Hotel, Room_Type, Room_Inventory, db, date_list, Attendee_Type
import sqlalchemy

bp = Blueprint('hotels', __name__, url_prefix='/hotels')


@bp.route('', methods=['POST'])
def create():

    required_fields = ['name', 'address', 'city', 'state_abr', 'zip_code']

    for header in required_fields:
        if header not in request.json:
            return abort(404)
        else:
            continue

    name = request.json['name']
    address = request.json['address']
    city = request.json['city']
    state_abr = request.json['state_abr']
    zip_code = request.json['zip_code']

    h = Hotel(name, address, city, state_abr, zip_code)

    db.session.add(h)
    db.session.commit()

    return jsonify(h.serialize())


@bp.route('/<int:id>', methods=['POST'])
def add_room_type(id: int):

    Hotel.query.get_or_404(id)

    required_fields = ['name', 'max_guests', 'price']
    for header in required_fields:
        if header not in request.json:
            return abort(404)

    r = Room_Type(id, request.json['name'], request.json['max_guests'],
                  request.json['price'])

    db.session.add(r)
    db.session.commit()

    inventory = request.json['inventory'] if 'inventory' in request.json else 0
    room_inventories = []
    for date in date_list:
        ri = Room_Inventory(r.id, date, inventory)
        room_inventories.append(ri)

    db.session.add_all(room_inventories)
    db.session.commit()

    return jsonify(r.serialize())


@bp.route('/<int:id>', methods=['PATCH'])
def inventory_update(id: int):

    if 'number_adjustment' not in request.json:
        abort(404)

    Room_Inventory.query.filter_by(room_id=id).update(
        {'inventory': Room_Inventory.inventory + request.json['number_adjustment']})
    db.session.commit()
    ri = Room_Inventory.query.filter_by(room_id=id)
    result = []
    for row in ri:
        result.append(row.serialize())
    return jsonify(result)




@bp.route('/<int:id>', methods=['GET'])
def see_attendees(id: int):

    r = Room_Type.query.get_or_404(id)

    result = []
    for a in r.attendees:
        result.append(a.serialize())

    return jsonify(result)
