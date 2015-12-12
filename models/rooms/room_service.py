from room_dao import RoomDao
from models.rooms.room import Room

roomDao = RoomDao()


class RoomService:
    def __init__(self):
        pass

    @classmethod
    def add_room_to_reservation(cls, rooms, reservation_id, room_location):
        # room_type = roomDao.get_room_type(str(room_category))
        """
        # room = Room(room_type.num_people, room_type.category, room_type.cost, room_type.cost_extra_bed, room_number, room_location)
        room = Room(room_type.num_people, room_type.category, room_type.cost, room_type.cost_extra_bed, room_number, room_location)
        print("category is ..............", room.category)
        print("num people is ..............", room.num_people)
        print("cost is ..............", room.cost)
        print("cost extra bed is ..............", room.cost_extra_bed)
        print("room number is ..............", room.room_num)
        print("location......................", room.location)
        """
        for room in rooms:
            roomDao.add_room_to_reservation(str(reservation_id), room_location, room['room_number'], room['extra_bed'])
        return True

    @classmethod
    def get_rooms_from_reservation_id(cls, reservation_id):
        rooms = roomDao.get_rooms_from_reservation_id(reservation_id)
        if len(rooms) == 0:
            return "Something terrible has happened"
        return rooms

    @classmethod
    def get_room_numbers_array(cls, rooms):
        room_numbers_list = []
        for room in rooms:
            room_numbers_list.append(room['room_number'])
        return room_numbers_list
