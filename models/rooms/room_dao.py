from models.rooms.RoomType import RoomType
from models.rooms.room import Room
from application import db
from flask_login import current_user


class RoomDao:
    def __init__(self):
        pass

    @classmethod
    def add_room_to_reservation(cls, reservation_id, room_location, room_number, extra_bed):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute(
            "INSERT INTO ReservationHasRooms (reservation_id, room_location, room_number, has_extra_bed)"
            "VALUES (%s, %s, %s, %s)",
            (reservation_id, room_location, room_number, extra_bed))
        cur.commit()
        cursor.close()
        return True

    @classmethod
    def get_rooms_from_reservation_id(cls, reservation_id):
        rooms = []
        cur = db.connection.cursor()
        cur.execute(
            "SELECT Rooms.room_number, Rooms.room_category, Rooms.number_people, Rooms.cost, Rooms.cost_extra_bed,  RhR.has_extra_bed "
            "FROM (SELECT R.room_number, R.room_location, RT.room_category, RT.cost, RT.cost_extra_bed, RT.number_people "
            "FROM RoomType AS RT NATURAL JOIN  Room AS R) AS Rooms "
            "NATURAL JOIN ReservationHasRooms AS RhR WHERE reservation_id='%s';" % reservation_id)
        reservation_instance = cur.fetchall()
        for val in reservation_instance:
            room_dict = {'room_number': val[0], 'room_category': val[1], 'number_people': val[2], 'cost_per_day': val[3],
                         'cost_extra_bed': val[4], 'extra_bed': val[5]}
            rooms.append(room_dict)
        cur.close()
        return rooms
