import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

date_list = ['2022-03-01', '2022-03-02', '2022-03-03', '2022-03-04']


class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    state_abr = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    rooms = db.relationship('Room_Type', backref='hotel',
                            lazy='dynamic')

    def __init__(self, name: str, address: str, city: str, state_abr: str, zip_code: int):
        self.name = name
        self.address = address
        self.city = city
        self.state_abr = state_abr
        self.zip_code = zip_code

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state_abr': self.state_abr,
            'zip_code': self.zip_code
        }


attendee_rooms_table = db.Table(
    'attendee_rooms',
    db.Column(
        'room_id', db.SmallInteger,
        db.ForeignKey('room_types.id', ondelete='CASCADE'),
        primary_key=True
    ),

    db.Column(
        'attendee_id', db.SmallInteger,
        db.ForeignKey('attendee_types.id', ondelete='CASCADE'),
        primary_key=True
    )
)


class Room_Type(db.Model):
    __tablename__ = 'room_types'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    hotel_id = db.Column(db.SmallInteger, db.ForeignKey(
        'hotels.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    max_guests = db.Column(db.SmallInteger, nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.relationship(
        'Room_Inventory', backref='Room', lazy='dynamic')

    def __init__(self, hotel_id: int, name: str, max_guests: int, price: float):
        self.hotel_id = hotel_id
        self.name = name
        self.max_guests = max_guests
        self.price = price

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'max_guests': self.max_guests
        }

    def serialize_with_hotel(self):
        return{
            'id': self.id,
            'hotel': self.hotel.name,
            'name': self.name,
            'max_guests': self.max_guests
        }


class Attendee_Type(db.Model):
    __tablename__ = 'attendee_types'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    access_code = db.Column(db.String(128), unique=True)
    rooms = db.relationship(
        'Room_Type', secondary=attendee_rooms_table, lazy='dynamic', backref=db.backref('attendees', lazy='dynamic'))

    def __init__(self, name: int, access_code: str):
        self.name = name
        self.access_code = access_code

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name
        }


class Room_Inventory(db.Model):
    __tablename__ = 'room_inventories'
    __table_args__ = (db.CheckConstraint("inventory >= 0"),)
    room_id = db.Column(db.SmallInteger, db.ForeignKey(
        'room_types.id', ondelete="CASCADE"), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    inventory = db.Column(db.SmallInteger, nullable=False, default=0)
    non_negative = db.CheckConstraint("inventory >= 0")

    def __init__(self, room_id: int, date, inventory):
        self.room_id = room_id
        self.date = date
        self.inventory = inventory

    def serialize(self):
        return{
            'hotel': self.Room.hotel.name,
            'room': self.Room.name,
            'room_id': self.room_id,
            'date': self.date.isoformat(),
            'inventory': self.inventory
        }


class Reservation(db.Model):
    def calc_num_nights(context):
        check_in_date = datetime.datetime.strptime(
            context.get_current_parameters()['check_in_date'], '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(
            context.get_current_parameters()['check_out_date'], '%Y-%m-%d')
        num_of_days = check_out_date - check_in_date
        return num_of_days.days

    def get_price(context):
        room_id = context.get_current_parameters()['room_id']
        r = Room_Type.query.get_or_404(room_id)
        return r.price

    def calc_total_price(context):
        check_in_date = datetime.datetime.strptime(
            context.get_current_parameters()['check_in_date'], '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(
            context.get_current_parameters()['check_out_date'], '%Y-%m-%d')
        num_of_days = check_out_date - check_in_date
        room_id = context.get_current_parameters()['room_id']
        r = Room_Type.query.get_or_404(room_id)

        return num_of_days.days * r.price

    __tablename__ = 'reservations'
    ack_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    state_abr = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.SmallInteger, db.ForeignKey(
        'room_types.id'), nullable=False)
    attendee_id = db.Column(db.SmallInteger, db.ForeignKey(
        'attendee_types.id'), nullable=False)
    hotel_id = db.Column(db.SmallInteger, db.ForeignKey(
        'hotels.id'), nullable=False)
    price_per_night = db.Column(
        db.Float, default=get_price, onupdate=get_price)
    number_of_nights = db.Column(
        db.SmallInteger, default=calc_num_nights, onupdate=calc_num_nights)
    total_stay_price = db.Column(
        db.Float, default=calc_total_price, onupdate=calc_total_price)
    revervation_created = db.Column(
        db.DateTime, default=datetime.datetime.now())

    def __init__(self, first_name: str, last_name: str, check_in_date,
                 check_out_date, address: str, city: str, state_abr: str,
                 zip_code: int, room_id: int, attendee_id: int, hotel_id: int):
        self.first_name = first_name
        self.last_name = last_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.address = address
        self.city = city
        self.state_abr = state_abr
        self.zip_code = zip_code
        self.room_id = room_id
        self.attendee_id = attendee_id
        self.hotel_id = hotel_id

    def serialize(self):
        return{
            "Ackowledgement Number": self.ack_num,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Check In Date": self.check_in_date.isoformat(),
            "Check Out Date": self.check_out_date.isoformat(),
            "Address": self.address,
            "City": self.city,
            "Hotel": Hotel.query.get_or_404(self.hotel_id).name,
            "Room Type": Room_Type.query.get_or_404(self.room_id).name,
            "Price Per Night": self.price_per_night,
            "Number of Nights": self.number_of_nights,
            "Total": self.total_stay_price,
            "Date Created": self.revervation_created
        }
