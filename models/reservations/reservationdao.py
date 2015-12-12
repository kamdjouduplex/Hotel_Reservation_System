from models.reservations.reservation import Reservation
from models.rooms.room import Room
from application import db
from flask_login import current_user


class ReservationDao:
    def __init__(self):
        pass

    @classmethod
    def check_for_rooms(cls, start_date, end_date, location):
        room_list = set()
        cur = db.connection.cursor()
        cur.execute(
            "SELECT Rooms.room_category, Rooms.number_people, Rooms.cost, Rooms.cost_extra_bed, Rooms.room_location, Rooms.room_number "
            "FROM (SELECT Room.room_category, RoomType.number_people, RoomType.cost, RoomType.cost_extra_bed, Room.room_location, Room.room_number "
            "FROM Room INNER JOIN RoomType ON Room.room_category = RoomType.room_category WHERE ( Room.room_location ='%s') ) AS Rooms "
            "WHERE room_number NOT IN (SELECT ReservationHasRooms.room_number FROM ReservationHasRooms WHERE ReservationHasRooms.reservation_id IN "
            "(SELECT Reservation.reservation_id FROM Reservation WHERE (ReservationHasRooms.room_location='%s' AND Reservation.is_cancelled='0' "
            "AND Date('%s') < Date(Reservation.end_date) AND Date('%s') >= Date(Reservation.start_date))));" % (
            location, location, start_date, end_date)
        )
        room_instance = cur.fetchall()
        for val in room_instance:
            room_category = val[0]
            num_people = val[1]
            cost = val[2]
            cost_extra_bed = val[3]
            room_location = val[4]
            room_num = val[5]
            room_list.add(Room(num_people, room_category, cost, cost_extra_bed, room_num, room_location))
        cur.close()
        return room_list

    @classmethod
    def get_all_reservations(cls):
        reservation_list = set()
        cur = db.connect().cursor()
        cur.execute(
            "SELECT DISTINCT reservation_id, start_date, end_date, user_name, is_cancelled, card_number, total_cost FROM Reservation WHERE is_cancelled='0';")
        reservation_instance = cur.fetchall()
        for val in reservation_instance:
            reservation_id = val[0]
            start_date = val[1]
            end_date = val[2]
            user_name = val[3]
            hotel_loc = val[4]
            is_cancelled = val[5]
            card_num = val[6]
            total_cost = val[7]
            reservation_list.add(
                Reservation(reservation_id, user_name, hotel_loc, start_date, end_date, is_cancelled,
                            card_num, total_cost))
        cur.close()
        return reservation_list

    @classmethod
    def get_reservations_by_username(cls, username):
        reservation_list = []
        cur = db.connection.cursor()
        # cur.execute("SELECT reservation_id, start_date, end_date, user_name, is_cancelled, card_number FROM Reservation WHERE user_name='%s' AND is_cancelled='0';" % username)
        cur.execute(
            "SELECT DISTINCT R.reservation_id, R.start_date, R.end_date, RhR.room_location, R.total_cost FROM Reservation AS R "
            "NATURAL JOIN ReservationHasRooms AS RhR WHERE (R.user_name='%s' AND R.is_cancelled='0');" % username
        )
        reservation_instance = cur.fetchall()
        for val in reservation_instance:
            reservation_dict = {'reservation_id': val[0], 'start_date': val[1], 'end_date': val[2], 'location': val[3],
                                'total_cost': val[4]}
            reservation_list.append(reservation_dict)
        cur.close()
        return reservation_list

    @classmethod
    def get_reservation_by_reservation_id(cls, reservation_id):
        reservation = None
        cur = db.connection.cursor()
        # cur.execute("SELECT reservation_id, start_date, end_date, user_name, is_cancelled, card_number FROM Reservation WHERE reservation_id='%s' AND is_cancelled='0';" % reservation_id)
        cur.execute(
            "SELECT DISTINCT R.reservation_id, R.start_date, R.end_date, R.user_name, RhR.room_location, R.is_cancelled, "
            "R.card_number, R.total_cost FROM Reservation AS R INNER JOIN ReservationHasRooms AS RhR ON RhR.reservation_id=R.reservation_id"
            " WHERE (R.reservation_id='%s' AND R.is_cancelled='0');" % reservation_id
        )
        reservation_instance = cur.fetchall()
        for val in reservation_instance:
            reservation_id = val[0]
            start_date = val[1]
            end_date = val[2]
            user_name = val[3]
            hotel_loc = val[4]
            is_cancelled = val[5]
            card_num = val[6]
            total_cost = val[7]
            reservation = Reservation(reservation_id, user_name, hotel_loc, str(start_date), str(end_date),
                                      is_cancelled, card_num, total_cost)
        cur.close()
        return reservation

    @classmethod
    def add_reservation(cls, reservation):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute(
            "INSERT INTO Reservation (reservation_id, start_date, end_date, user_name, is_cancelled, card_number, total_cost) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (reservation.reservation_id, reservation.start_date, reservation.end_date, current_user.username,
             reservation.is_cancelled, reservation.payment_information, reservation.total_cost))
        cur.commit()
        cursor.close()
        return reservation

    @classmethod
    def delete_reservation(cls, reservation_id, total_cost, number_of_rooms):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute("UPDATE Reservation SET is_cancelled='1', total_cost='%s' WHERE reservation_id='%s';" % (str(total_cost), str(reservation_id)))
        cursor.execute("SET foreign_key_checks = 0;")
        i = 0
        while i < number_of_rooms:
            cursor.execute("UPDATE ReservationHasRooms SET room_number='%s'  WHERE reservation_id='%s' ORDER BY room_number DESC LIMIT 1;" % (i, str(reservation_id)))
            i += 1
        cursor.execute("SET foreign_key_checks = 1;")
        cur.commit()
        cursor.close()

    @classmethod
    def get_locations(cls):
        locations = set()
        cur = db.connection.cursor()
        cur.execute("SELECT room_location FROM Location;")
        location_instance = cur.fetchall()
        for val in location_instance:
            location = val[0]
            locations.add(location)
        cur.close()
        return locations

    @classmethod
    def search_rooms_with_new_dates(cls, start_date, end_date, location, rooms):
        room_list = set()
        cur = db.connection.cursor()
        cur.execute(
            "SELECT Rooms.room_category, Rooms.number_people, Rooms.cost, Rooms.cost_extra_bed, Rooms.room_location, Rooms.room_number "
            "FROM (SELECT Room.room_category, RoomType.number_people, RoomType.cost, RoomType.cost_extra_bed, Room.room_location, Room.room_number "
            "FROM Room INNER JOIN RoomType ON Room.room_category = RoomType.room_category WHERE ( Room.room_location ='%s')) "
            "AS Rooms WHERE (room_number NOT IN (SELECT ReservationHasRooms.room_number FROM ReservationHasRooms "
            "WHERE ReservationHasRooms.reservation_id IN (SELECT Reservation.reservation_id FROM Reservation "
            "WHERE (ReservationHasRooms.room_location='%s' AND Reservation.is_cancelled='0' AND Date('%s') <= Date(Reservation.end_date) "
            "AND Date('%s') >= Date(Reservation.start_date)))) AND Rooms.room_number IN (%s));" % (
            location, location, start_date, end_date, rooms)
        )
        room_instance = cur.fetchall()
        for val in room_instance:
            room_category = val[0]
            num_people = val[1]
            cost = val[2]
            cost_extra_bed = val[3]
            room_location = val[4]
            room_num = val[5]
            room_list.add(Room(num_people, room_category, cost, cost_extra_bed, room_num, room_location))
        cur.close()
        return room_list

    @classmethod
    def update_reservation_dates(cls, reservation_id, new_start_date, new_end_date, total_cost):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute("UPDATE Reservation SET start_date='%s', end_date='%s', total_cost='%s' WHERE reservation_id='%s';" % (new_start_date, new_end_date, total_cost, str(reservation_id)))
        cur.commit()
        cursor.close()

    @classmethod
    def get_reservation_rooms(cls, reservation_id):
        cur = db.connection.cursor()
        cur.execute(
            "SELECT ReservationHasRooms.room_number FROM ReservationHasRooms WHERE ReservationHasRooms.reservation_id='%s';" % reservation_id
        )
        rooms = cur.fetchall()
        cur.close()
        return rooms

    @classmethod
    def add_credit_card(cls, name, card_number, expiration_date, cvv, user):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute(
            "INSERT INTO PaymentInformation (name_on_card, card_number, expiration_date, cvv, user_name) VALUES (%s, %s, %s, %s, %s)",
            (name, card_number, expiration_date, cvv, user)
        )
        cur.commit()
        cursor.close()

    @classmethod
    def add_review(cls, location, rating, comment, review_id, user):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute(
            "INSERT INTO HotelReview (review_number, location, rating, comment, user_name) VALUES (%s, %s, %s, %s, %s)",
            (str(review_id), location, rating, comment, user)
        )
        cur.commit()
        cursor.close()

    @classmethod
    def get_all_reviews_by_location(cls, location):
        all_reviews = []
        cur = db.connection.cursor()
        cur.execute(
            "SELECT HotelReview.rating, HotelReview.comment FROM HotelReview WHERE HotelReview.location='%s';" % location
        )
        reviews = cur.fetchall()
        for review in reviews:
            review_dict = {'rating': review[0], 'comment': review[1]}
            all_reviews.append(review_dict)
        cur.close()
        return all_reviews

    @classmethod
    def get_room_count(cls, reservation_id):
        cur = db.connection.cursor()
        cur.execute(
            "SELECT reservation_id, COUNT(*) AS count FROM ReservationHasRooms WHERE reservation_id='%s';" % reservation_id
        )
        rooms = cur.fetchall()
        num_rooms = rooms[0][1]
        cur.close()
        return num_rooms

    @classmethod
    def get_future_reservations(cls, username, today):
        reservation_list = set()
        cur = db.connection.cursor()
        # cur.execute("SELECT reservation_id, start_date, end_date, user_name, is_cancelled, card_number FROM Reservation WHERE user_name='%s' AND is_cancelled='0';" % username)
        cur.execute(
            "SELECT DISTINCT R.reservation_id, R.start_date, R.end_date, R.user_name, RhR.room_location, R.is_cancelled, "
            "R.card_number, R.total_cost FROM Reservation AS R, ReservationHasRooms AS RhR WHERE (R.start_date >= '%s' AND R.user_name='%s' "
            "AND R.is_cancelled='0' "
            "AND RhR.reservation_id=R.reservation_id);" % (today, username)
        )
        reservation_instance = cur.fetchall()
        for val in reservation_instance:
            reservation_id = val[0]
            start_date = val[1]
            end_date = val[2]
            user_name = val[3]
            hotel_loc = val[4]
            is_cancelled = val[5]
            card_num = val[6]
            total_cost = val[7]
            reservation_list.add(
                Reservation(reservation_id, user_name, hotel_loc, start_date, end_date, is_cancelled,
                            card_num, total_cost))
        cur.close()
        return reservation_list

    @classmethod
    def get_future_and_present_reservations(cls, username, today):
        reservation_list = set()
        cur = db.connection.cursor()
        # cur.execute("SELECT reservation_id, start_date, end_date, user_name, is_cancelled, card_number FROM Reservation WHERE user_name='%s' AND is_cancelled='0';" % username)
        cur.execute(
            "SELECT DISTINCT R.reservation_id, R.start_date, R.end_date, R.user_name, RhR.room_location, R.is_cancelled, "
            "R.card_number, R.total_cost FROM Reservation AS R, ReservationHasRooms AS RhR WHERE (R.end_date >= '%s' AND R.user_name='%s' "
            "AND R.is_cancelled='0' "
            "AND RhR.reservation_id=R.reservation_id);" % (today, username)
        )
        reservation_instance = cur.fetchall()
        for val in reservation_instance:
            reservation_id = val[0]
            start_date = val[1]
            end_date = val[2]
            user_name = val[3]
            hotel_loc = val[4]
            is_cancelled = val[5]
            card_num = val[6]
            total_cost = val[7]
            reservation_list.add(
                Reservation(reservation_id, user_name, hotel_loc, start_date, end_date, is_cancelled,
                            card_num, total_cost))
        cur.close()
        return reservation_list

    @classmethod
    def delete_credit_card(cls, card_number):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute("DELETE FROM PaymentInformation WHERE card_number='%s';" % card_number)
        cur.commit()
        cursor.close()

    @classmethod
    def check_credit_card(cls, card_number):
        credit_cards = []
        cur = db.connection.cursor()
        cur.execute(
            "SELECT card_number FROM PaymentInformation WHERE card_number='%s';" % card_number
        )
        cards = cur.fetchall()
        for val in cards:
            card = val[0]
            credit_cards.append(card)
        cur.close()
        return credit_cards

    @classmethod
    def check_to_delete_credit_card(cls, card_number):
        credit_cards = []
        cur = db.connection.cursor()
        cur.execute(
            "SELECT card_number FROM Reservation WHERE card_number='%s';" % card_number
        )
        cards = cur.fetchall()
        for val in cards:
            card = val[0]
            credit_cards.append(card)
        cur.close()
        return credit_cards
