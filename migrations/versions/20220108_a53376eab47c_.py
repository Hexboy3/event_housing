"""empty message

Revision ID: a53376eab47c
Revises: 
Create Date: 2022-01-08 16:04:14.535404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a53376eab47c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendee_types',
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('access_code', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_code'),
    sa.UniqueConstraint('name')
    )
    op.create_table('hotels',
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.Column('city', sa.String(length=128), nullable=False),
    sa.Column('state_abr', sa.String(length=2), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('room_types',
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('hotel_id', sa.SmallInteger(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('max_guests', sa.SmallInteger(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendee_rooms',
    sa.Column('room_id', sa.SmallInteger(), nullable=False),
    sa.Column('attendee_id', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['attendee_id'], ['attendee_types.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room_id'], ['room_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('room_id', 'attendee_id')
    )
    op.create_table('reservations',
    sa.Column('ack_num', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('check_in_date', sa.Date(), nullable=False),
    sa.Column('check_out_date', sa.Date(), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.Column('city', sa.String(length=128), nullable=False),
    sa.Column('state_abr', sa.String(length=2), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.SmallInteger(), nullable=False),
    sa.Column('attendee_id', sa.SmallInteger(), nullable=False),
    sa.Column('hotel_id', sa.SmallInteger(), nullable=False),
    sa.Column('price_per_night', sa.Float(), nullable=True),
    sa.Column('number_of_nights', sa.SmallInteger(), nullable=True),
    sa.Column('total_stay_price', sa.Float(), nullable=True),
    sa.Column('revervation_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['attendee_id'], ['attendee_types.id'], ),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['room_types.id'], ),
    sa.PrimaryKeyConstraint('ack_num')
    )
    op.create_table('room_inventories',
    sa.Column('room_id', sa.SmallInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('inventory', sa.SmallInteger(), nullable=False),
    sa.CheckConstraint('inventory >= 0'),
    sa.ForeignKeyConstraint(['room_id'], ['room_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('room_id', 'date')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_inventories')
    op.drop_table('reservations')
    op.drop_table('attendee_rooms')
    op.drop_table('room_types')
    op.drop_table('hotels')
    op.drop_table('attendee_types')
    # ### end Alembic commands ###
