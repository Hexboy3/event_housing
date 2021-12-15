from flask import Blueprint, jsonify, abort, request
from ..models import Hotel, Room_Type, Room_Inventory, db, date_list, Attendee_Type, Reservation, attendee_rooms_table
from datetime import datetime, timedelta
import sqlalchemy

bp = Blueprint('attendees', __name__, url_prefix='/attendees')


@bp.route('blocked_rooms/<string:attendee_name>', methods=['GET'])
def attendee_rooms_by_name(attendee_name: str):
    """
    Returns various room types based on the rooms available to the attendee type name input by the user
    """
    # Make inserted attendee name lowercase
    attendee_name = attendee_name.lower()

    # Filter by attendee name to get the appropriate object
    a = Attendee_Type.query.filter_by(
        name=attendee_name).one()

    # Create a result list to add room_types to
    results = []
    # Loop through the room collection linked to the attendee
    for r in a.rooms:
        # Append room type to result list
        results.append(r.serialize_with_hotel())

    # Return reult list as a json object
    return jsonify(results)


@bp.route('blocked_rooms/<int:id>', methods=['GET'])
def attendee_rooms_by_id(id: int):
    """
    Returns various room types based on the rooms available to the attendee type id input by the user
    """

    # Filter by attendee name to get th appropriate row
    a = Attendee_Type.query.get_or_404(id)

    # Create a result list to add room_types to
    results = []
    # Loop through the room collection linked to the attendee
    for r in a.rooms:
        # Append room type to result list
        results.append(r.serialize_with_hotel())

    # Return reult list as a json object
    return jsonify(results)


@bp.route('attendee_inventory/<string:attendee_name>', methods=['GET'])
def attendee_inventory_by_name(attendee_name: str):

    '''
    Returns the inventory for each day and room type based on the attendee name entered
    '''
    # Make inserted attendee_name lowercase
    attendee_name = attendee_name.lower()

    # Filter for matching attendee row
    a = Attendee_Type.query.filter_by(
        name=attendee_name).one()

    # Create a result list to add room_types to
    results = []
    # Loop through the room collection linked to the attendee
    for r in a.rooms:
        # Lopp through the inventory for each room_type
        for inv in r.inventory.all():
            # Append inventory to result set
            results.append(inv.serialize())

    # Return reult list as a json object
    return jsonify(results)


@bp.route('attendee_inventory/<int:id>', methods=['GET'])
def attendee_inventory_by_id(id: int):

    '''
    Returns the inventory for each day and room type based on the attendee id entered
    '''

    # Filter for matching attendee row
    a = Attendee_Type.query.get_or_404(id)

    # Create a result list to add room_types to
    results = []
    # Loop through the room collection linked to the attendee
    for r in a.rooms:
        # Lopp through the inventory for each room_type
        for inv in r.inventory.all():
            # Append inventory to result set
            results.append(inv.serialize())

    # Return reult list as a json object
    return jsonify(results)


@bp.route('available/<string:attendee_name>', methods=['GET'])
def available_by_name(attendee_name: str):


    '''
    Returns the available rooms based on the check in and check out dates, number of rooms needed, and attendee name entered
    '''

    # Make inserted attendee name lowercase
    attendee_name = attendee_name.lower()

    # Check to see if dates are in request
    if 'check_in_date' not in request.json or 'check_out_date' not in request.json:
        return abort(400, description="Error: check_in_date or check_out_date not included in request")

    # check to see if the length of the strings is correct
    if len(request.json['check_in_date']) != 10 or len(request.json['check_out_date']) != 10:
        return abort(400, description="Error: Dates have to be in yyyy-mm-dd format")

    # NEED ERROR HANDLING
    a = Attendee_Type.query.filter_by(
        name=attendee_name).one()

    # check if acces code is correct
    if a.access_code != request.json['access_code']:
        return abort(400, description="Error: Incorrect access code")

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

    # Create a result list to add room_types to
    results = []
    # Loop through the room collection linked to the attendee
    for r in a.rooms:
        # filter for invnetory between the first night and last night that has the required inventory
        ri = r.inventory.filter(Room_Inventory.inventory >= number_of_rooms,
                                Room_Inventory.date >= first_night, Room_Inventory.date <= last_night)

        # Check to see if their is inventory for all nights required
        if len(ri.all()) == number_of_nights:
            # append to results set
            results.append(r.serialize_with_hotel())

    # return results as json object
    return jsonify(results)


@bp.route('available/<int:id>', methods=['GET'])
def available_by_id(id: int):


    '''
    Returns the available rooms based on the check in and check out dates, number of rooms needed, and attendee id entered
    '''

    # Check to see if dates are in request
    if 'check_in_date' not in request.json or 'check_out_date' not in request.json:
        return abort(400, description="Error: check_in_date or check_out_date not included in request")

    # check to see if the length of the strings is correct
    if len(request.json['check_in_date']) != 10 or len(request.json['check_out_date']) != 10:
        return abort(400, description="Error: Dates have to be in yyyy-mm-dd format")

    # NEED ERROR HANDLING
    a = Attendee_Type.query.get_or_404(id)

    # check if acces code is correct
    if a.access_code != request.json['access_code']:
        return abort(400, description="Error: Incorrect access code")

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

    # Create a result list to add room_types to
    results = []
    # Loop through the room collection linked to the attendee
    for r in a.rooms:
        # filter for invnetory between the first night and last night that has the required inventory
        ri = r.inventory.filter(Room_Inventory.inventory >= number_of_rooms,
                                Room_Inventory.date >= first_night, Room_Inventory.date <= last_night)

        # Check to see if their is inventory for all nights required
        if len(ri.all()) == number_of_nights:
            # append to results set
            results.append(r.serialize_with_hotel())

    # return results as json object
    return jsonify(results)


@bp.route('/reserve', methods=['POST'])
def reserve():

    # List of required fields to loop through
    required_fields = ['first_name', 'last_name', 'check_in_date', 'check_out_date',
                       'address', 'city', 'state_abr', 'zip_code', 'room_id']

    # Looping through to see if all required fields are in json request
    for field in required_fields:
        if field not in request.json:
            return abort(400, description=f"Error: {field} not in request")
        else:
            continue

    a = Attendee_Type.query.get_or_404(request.json['attendee_id'])

    #  Check to see if access code is correct
    if a.access_code != request.json['access_code']:
        return abort(400, description="Error: Incorrect access code")

    # Check to see if attendee can reserve this room_type
    if a.rooms.filter_by(id=request.json['room_id']).scalar() is None:
        return abort(404, description="Room not available for your attendee type")

    # Get room_type
    r = Room_Type.query.get_or_404(request.json['room_id'])

    # Check to see if the number of rooms is included in the request if not assume it is 1 room
    number_of_rooms = request.json['number_of_rooms'] if 'number_of_rooms' in request.json else 1

    # Save check in date as first night
    first_night = request.json['check_in_date']

    # Save the last_night as a datetime object
    last_night = datetime.strptime(request.json['check_out_date'], '%Y-%m-%d')

    # Save first night as datetime object
    first_night_date = datetime.strptime(
        first_night, '%Y-%m-%d')

    # Subtract the first_night_date from the last_night to get the number of nights needed to be used later
    number_of_nights = last_night.day - first_night_date.day

    # Create a timedelta object to be used to get the night before the chekout
    subtract_day = timedelta(1)

    # Subtract one day from the checkout to get the last_night needed
    last_night = last_night - subtract_day

    # Convert the last_night back to a string
    last_night = last_night.strftime('%Y-%m-%d')

    # Filter for the rows in room_inventory where the the number of rooms available is greater than the number of rooms requested
    # Also filter for rows where within the date range
    inventory = r.inventory.filter(Room_Inventory.inventory >= number_of_rooms,
                                   Room_Inventory.date >= first_night, Room_Inventory.date <= last_night)

    # Check to see if all nights are included from the filtered inventory object if it is less than the number of nights it is aborted
    if len(inventory.all()) != number_of_nights:
        return abort(404, description="This Room type does not have enough inventory")
    else:
        # List to store the updated rows
        add_list = []
        # Loop through the inventory rows
        for ri in inventory:
            # Decrease the inventory by the number of nights requested
            ri.inventory = ri.inventory - number_of_rooms
            # Append the row the the add list
            add_list.append(ri)

        # Create the reservation to add to the commit list
        res = Reservation(request.json['first_name'], request.json['last_name'],
                          request.json['check_in_date'], request.json['check_out_date'],
                          request.json['address'], request.json['city'], request.json['state_abr'],
                          request.json['zip_code'], request.json['room_id'], request.json['attendee_id'], r.hotel_id)

        # Add the reservation to the add list
        add_list.append(res)

        # Add all of the rows to be commited
        db.session.add_all(add_list)

        # Commit all of the rows
        db.session.commit()

        # Return True (need to update to include all details of the reservation)
        return jsonify(True)
