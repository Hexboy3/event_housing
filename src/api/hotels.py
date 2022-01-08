from flask import Blueprint, jsonify, abort, request
from ..models import Hotel, Room_Type, Room_Inventory, db, date_list, Attendee_Type
import sqlalchemy

bp = Blueprint('hotels', __name__, url_prefix='/hotels')


@bp.route('', methods=['POST'])
def create():

    # Create list of required fields needed in json request
    required_fields = ['name', 'address', 'city', 'state_abr', 'zip_code']

    # Looping through to see if all required fields are in json request
    for field in required_fields:
        if field not in request.json:
            return abort(404, description=f"Error: {field} not in request")
        else:
            continue

    # Create hotel objects from details in request
    h = Hotel(request.json['name'], request.json['address'], request.json['city'],
              state_abr=request.json['state_abr'], zip_code=request.json['zip_code'])

    # Add to hotel object to session
    db.session.add(h)

    # Commit hotel object
    db.session.commit()

    # Return json object with inputted details
    return jsonify(h.serialize())


@bp.route('/<int:id>', methods=['POST'])
def add_room_type(id: int):

    # Get hotel object
    Hotel.query.get_or_404(id)

    # Create list of required fields needed from json request
    required_fields = ['name', 'max_guests', 'price']

    # Loop through required_fields list and check if they are in json request
    for field in required_fields:
        if field not in request.json:
            return abort(404)
        else:
            continue
    # Create Room_Type object using fields in json request
    r = Room_Type(id, request.json['name'], request.json['max_guests'],
                  request.json['price'])

    # add Room_Type object r to session
    db.session.add(r)

    # Commit Room_Type object
    db.session.commit()

    # Check to see if inventory is in json request if not make it zero
    inventory = request.json['inventory'] if 'inventory' in request.json else 0

    # Create list to store Room_Invneotry objects
    room_inventories = []

    # Loop through the date_list to create a row for each date and append it to room_inventories list
    for date in date_list:
        ri = Room_Inventory(r.id, date, inventory)
        room_inventories.append(ri)

    # Add room_inventories list to session to be added
    db.session.add_all(room_inventories)

    # Commit changes to the database
    db.session.commit()

    # return json object to show inventory for each date
    return jsonify(r.serialize())


@bp.route('/<int:id>', methods=['PATCH'])
def inventory_update(id: int):

    # check to see if number_adjustment is in json request abort if not
    if 'number_adjustment' not in request.json:
        abort(404, description="Error: number_ajustment not in request")

    # Update Invnetory rows by number_adjustment
    Room_Inventory.query.filter_by(room_id=id).update(
        {'inventory': Room_Inventory.inventory + request.json['number_adjustment']})

    # Commit changes
    db.session.commit()

    # Get inventory rows
    ri = Room_Inventory.query.filter_by(room_id=id)

    # Create results list
    results = []

    # Loop through invnetory rows and append serialized data to results
    for row in ri:
        results.append(row.serialize())

    # Convert results into json object and return it
    return jsonify(results)


@bp.route('/<int:id>', methods=['GET'])
def see_attendees(id: int):

    # get room_type object
    r = Room_Type.query.get_or_404(id)

    # Create results list
    results = []

    # Loop through attendees for the room type and append to results list in serialized form
    for a in r.attendees:
        results.append(a.serialize())

    # Convert results into json object and return it
    return jsonify(results)


@bp.route('/remove/hotel/<int:id>', methods=['DELETE'])
def delete_hotel(id: int):
    """
    Delete hotel from event
    """
    try:
        Hotel.query.filter_by(id=id).delete()

        db.session.commit()
        return jsonify(True)

    except:
        return jsonify(False)


@bp.route('/remove/room_type/<int:id>', methods=['DELETE'])
def delete_room_type(id: int):
    """
    Delete room type from event
    """
    try:
        Room_Type.query.filter_by(id=id).delete()

        db.session.commit()

        return jsonify(True)
    except:
        return jsonify(False)
