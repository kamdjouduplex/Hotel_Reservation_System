import uuid
from models.payment_information.payment_service import PaymentService
from reservationdao import ReservationDao
from models.reservations.reservation import Reservation
from models.rooms.room_service import RoomService
from models.payment_information.payment_information import PaymentInformation
from datetime import datetime
from datetime import timedelta
from datetime import date


reservationDao = ReservationDao()
paymentService = PaymentService()
roomService = RoomService()


class ReservationService:
    def __init__(self):
        pass

    @classmethod
    def check_for_rooms(cls, start_date, end_date, location):
        rooms = reservationDao.check_for_rooms(start_date, end_date, location)
        return rooms

    @classmethod
    def create_reservation(cls, reservation_id, current_user, location, start_date, end_date, cc_number, rooms):
        # rooms = (rooms['room_number'], rooms['room_number']['room_category'], room_location)
        is_cancelled = False
        payment = True
        if payment is not None:
            total_cost = cls.get_total_cost(rooms, start_date, end_date)
            print rooms
            if total_cost > 0:
                new_reservation = Reservation(reservation_id, current_user, location, start_date, end_date, is_cancelled, str(cc_number), total_cost)
                reservationDao.add_reservation(new_reservation)
                cls.add_rooms_to_reservation(rooms, reservation_id, location)
                return "Success"
        return "Failed to Create Reservation"

    @classmethod
    def delete_reservation(cls, reservation):
        # if date is within 3 days of reservation do not allow deletion
        if reservation is not None:
            total_cost = None
            number_of_rooms = int(reservationDao.get_room_count(
                str(
                    reservation.get_reservation_id()
                )
            ))
            if datetime.strptime(reservation.start_date, "%Y-%m-%d").date() <= date.today() + timedelta(days=1):
                total_cost = reservation.get_total_cost()
            elif datetime.strptime(reservation.start_date, "%Y-%m-%d").date() <= date.today() + timedelta(days=3):
                total_cost = reservation.get_total_cost() * .2
            else:
                total_cost = 0
            return reservationDao.delete_reservation(reservation.get_reservation_id(), total_cost, number_of_rooms)
        else:
            return None

    @classmethod
    def get_reservations_by_username(cls, user):
        username = str(user.username)
        return reservationDao.get_reservations_by_username(username)

    @classmethod
    def get_reservation_by_reservation_id(cls, reservation_id):
        return reservationDao.get_reservation_by_reservation_id(str(reservation_id))

    @classmethod
    def get_locations(cls):
        return reservationDao.get_locations()

    @classmethod
    def get_total_cost(cls, rooms, start_date, end_date):
        # str_room_numbers = cls.get_room_numbers(rooms)
        # return reservationDao.get_total_cost(str_room_numbers, location)
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        number_of_nights = (end_date - start_date).days
        total_cost = 0
        for room in rooms:
            total_cost += room['cost_per_day']
            if room['extra_bed'] == 1:
                total_cost += room['cost_extra_bed']
        return number_of_nights * total_cost

    @classmethod
    def add_cc(cls, cc_name, cc_expiration_date, cc_cvv, cc_number):
        return paymentService.add_payment_information(cc_name, cc_expiration_date, cc_cvv, cc_number)

    @classmethod
    def add_rooms_to_reservation(cls, rooms, reservation_id, room_location):
        return roomService.add_room_to_reservation(rooms, reservation_id, room_location)

    @classmethod
    def search_rooms_with_new_dates(cls, start_date, end_date, location, reservation_id):
        rooms = reservationDao.get_reservation_rooms(str(reservation_id))
        str_rooms = ''
        for room in rooms:
            str_rooms = "'" + str(room[0]) + "'" + ", " + str_rooms
        str_rooms = str_rooms[:-2]
        available_rooms = reservationDao.search_rooms_with_new_dates(start_date, end_date, location, str_rooms)
        if len(available_rooms) != len(rooms):
            available_rooms = None
        return available_rooms

    @classmethod
    def update_reservation_dates(cls, reservation_id, new_start_date, new_end_date, total_cost):
        # total_cost = cls.get_total_cost()
        return reservationDao.update_reservation_dates(reservation_id, new_start_date, new_end_date, total_cost)

    @classmethod
    def add_credit_card(cls, name, card_number, expiration_date, cvv, current_user):
        current_user = current_user.username
        return reservationDao.add_credit_card(name, card_number, expiration_date, cvv, current_user)

    @classmethod
    def get_room_numbers(cls, rooms):
        str_room_numbers = ''
        for room in rooms:
            str_room_numbers = "'" + str(room['room_number']) + "'" + ", " + str_room_numbers
        str_room_numbers = str_room_numbers[:-2]
        return str_room_numbers

    @classmethod
    def add_review(cls, location, rating, comment, current_user):
        current_user = current_user.username
        review_id = uuid.uuid4()
        return reservationDao.add_review(location, rating, comment, review_id, current_user)

    @classmethod
    def get_all_reviews_by_location(cls, location):
        reviews = reservationDao.get_all_reviews_by_location(location)
        if len(reviews) == 0:
            reviews = None
        return reviews

    @classmethod
    def get_future_reservations(cls, current_user):
        today = str(date.today())
        reservations = reservationDao.get_future_reservations(current_user, today)
        return reservations

    @classmethod
    def get_future_and_present_reservations(cls, current_user):
        today = str(date.today())
        reservations = reservationDao.get_future_and_present_reservations(current_user, today)
        return reservations

    @classmethod
    def delete_credit_card(cls, card_number):
        return reservationDao.delete_credit_card(card_number)

    @classmethod
    def check_credit_card(cls, card_number):
        cards = reservationDao.check_credit_card(card_number)
        if len(cards) == 1:
            return True
        else:
            return False

    @classmethod
    def check_to_delete_credit_card(cls, card_number):
        cards = reservationDao.check_to_delete_credit_card(card_number)
        if len(cards) > 0:
            return False
        else:
            return True

