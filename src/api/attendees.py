from flask import Blueprint, jsonify, abort, request
from ..models import Hotel, Room_Type, Room_Inventory, db, date_list, Attendee_Type, Reservation, attendee_rooms_table
from datetime import datetime, timedelta
import sqlalchemy

bp = Blueprint('attendees', __name__, url_prefix='/attendees')


@bp.route('blocked_rooms/<attendee_name>', methods=['GET'])
def attendee_rooms(attendee_name: str):

    a = Attendee_Type.query.filter(Attendee_Type.name == attendee_name).first()

    result = []
    for r in a.rooms:
        result.append(r.serialize_with_hotel())

    return jsonify(result)


@bp.route('attendee_inventory/<attendee_name>', methods=['GET'])
def attendee_inventory(attendee_name: str):

    a = db.session.query(Attendee_Type).filter(
        Attendee_Type.name == attendee_name).first()

    result = []
    for r in a.rooms:
        for inv in r.inventory.all():
            result.append(inv.serialize())

    return jsonify(result)


@bp.route('available/<attendee_name>', methods=['GET'])
def available(attendee_name: str):

    # Check to see if dates are in request
    if 'check_in' not in request.json or 'check_out' not in request.json:
        return abort(400)

    # check to see if the length of the strings is correct
    if len(request.json['check_in']) != 10 or len(request.json['check_out']) != 10:
        return abort(400)

    # NEED ERROR HANDLING
    a = db.session.query(Attendee_Type).filter(
        Attendee_Type.name == attendee_name).first()

    if a.access_code != request.json['access_code']:
        return abort(400)

    # Check to see if the number of rooms is included in the request if not assume it is 1 room
    number_of_rooms = request.json['number_of_rooms'] if 'number_of_rooms' in request.json else 1

    # save check in date as first night
    first_night = request.json['check_in_date']

    # save the last_night as a datetime object
    last_night = datetime.strptime(request.json['check_out_date'], '%Y-%m-%d')

    # save first night as datetime object
    first_night_date = datetime.strptime(
        first_night, '%Y-%m-%d')

    # subtract the first_night_date from the last_night to get the number of nights needed to be used later
    number_of_nights = last_night.day - first_night_date.day

    # create a timedelta object to be used to get the night before the chekout
    subtract_day = timedelta(1)

    # subtract one day from the checkout to get the last_night needed
    last_night = last_night - subtract_day

    # checnge the last_night back to a string
    last_night = last_night.strftime('%Y-%m-%d')

    results = []
    for r in a.rooms:
        ri = r.inventory.filter(Room_Inventory.inventory >= number_of_rooms,
                                Room_Inventory.date >= first_night, Room_Inventory.date <= last_night)
        if len(ri.all()) == number_of_nights:
            results.append(r.serialize_with_hotel())

    return jsonify(results)


@bp.route('/reserve', methods=['POST'])
def reserve():

    required_fields = ['first_name', 'last_name', 'check_in_date', 'check_out_date',
                       'address', 'city', 'state_abr', 'zip_code', 'room_id']

    # looping throught to see if all required fields are in json request
    for field in required_fields:
        if field not in request.json:
            return abort(400)
        else:
            continue

    a = Attendee_Type.query.get_or_404(request.json['attendee_id'])

    # Check to see if attendee can reserve this room_type
    if not a.rooms.filter(id == request.json['room_id']):
        return abort(404)
    # if not a.rooms.has(id=request.json['room_id']):
    #     return abort(404)

    if a.access_code != request.json['access_code']:
        return "Error: Access code incorrect for attendee type"

    # Get
    r = Room_Type.query.get_or_404(request.json['room_id'])

    # Check to see if the number of rooms is included in the request if not assume it is 1 room
    number_of_rooms = request.json['number_of_rooms'] if 'number_of_rooms' in request.json else 1

    # save check in date as first night
    first_night = request.json['check_in_date']

    # save the last_night as a datetime object
    last_night = datetime.strptime(request.json['check_out_date'], '%Y-%m-%d')

    # save first night as datetime object
    first_night_date = datetime.strptime(
        first_night, '%Y-%m-%d')

    # subtract the first_night_date from the last_night to get the number of nights needed to be used later
    number_of_nights = last_night.day - first_night_date.day

    # create a timedelta object to be used to get the night before the chekout
    subtract_day = timedelta(1)

    # subtract one day from the checkout to get the last_night needed
    last_night = last_night - subtract_day

    # checnge the last_night back to a string
    last_night = last_night.strftime('%Y-%m-%d')

    # Filter for the rows in room_inventory where the the number of rooms available is greater than the number of rooms requested
    # Also filter for rows where within the date range
    inventory = r.inventory.filter(Room_Inventory.inventory >= number_of_rooms,
                                   Room_Inventory.date >= first_night, Room_Inventory.date <= last_night)

    # check to see if all nights are included from the filtered inventory object if it is less than the number of nights it is aborted
    if len(inventory.all()) != number_of_nights:
        return abort(404, description="This Room type does not have enough inventory")
    else:
        # List to store the updated rows
        add_list = []
        # Loop through the inventory rows
        for ri in inventory:
            # decrease the inventory by the number of nights requested
            ri.inventory = ri.inventory - number_of_rooms
            # append the row the the add list
            add_list.append(ri)

        # Create the reservation to add to the commit list
        res = Reservation(request.json['first_name'], request.json['last_name'],
                          request.json['check_in_date'], request.json['check_out_date'],
                          request.json['address'], request.json['city'], request.json['state_abr'],
                          request.json['zip_code'], request.json['room_id'], request.json['attendee_id'], r.hotel_id)

        # add the reservation to the add list
        add_list.append(res)

        # add all of the rows to be commited
        db.session.add_all(add_list)

        # commit all of the rows
        db.session.commit()

        # return True (need to update to include all details of the reservation)
        return jsonify(True)
