from reservationservice import ReservationService

reservationService = ReservationService()


class ReservationWeb:
    def __init__(self):
        pass

    @classmethod
    def check_for_rooms(cls, start_date, end_date, location):
        rooms = reservationService.check_for_rooms(start_date, end_date, location)
        return rooms

    @classmethod
    def create(cls, reservation_id, current_user, location, start_date, end_date, cc_number, rooms):
        return reservationService.create_reservation(reservation_id, current_user, location, start_date, end_date, cc_number, rooms)

    @classmethod
    def delete(cls, reservation_id):
        return reservationService.delete_reservation(reservation_id)

    @classmethod
    def get_reservations_by_username(cls, user_inst):
        return reservationService.get_reservations_by_username(str(user_inst.username))

    @classmethod
    def get_future_reservations(cls, user_inst):
        return reservationService.get_future_reservations(str(user_inst.username))

    @classmethod
    def get_reservation_by_reservation_id(cls, reservation_id):
        return reservationService.get_reservation_by_reservation_id(str(reservation_id))

    @classmethod
    def get_locations(cls):
        return reservationService.get_locations()

    @classmethod
    def get_total_cost(cls, rooms, start_date, end_date):
        return reservationService.get_total_cost(rooms, start_date, end_date)

    @classmethod
    def update_reservation_dates(cls, reservation_id, new_start_date, new_end_date, total_cost):
        return reservationService.update_reservation_dates(reservation_id, new_start_date, new_end_date, total_cost)

    @classmethod
    def search_rooms_with_new_dates(cls, start_date, end_date, location, reservation_id):
        return reservationService.search_rooms_with_new_dates(start_date, end_date, location, reservation_id)

    @classmethod
    def add_credit_card(cls, name, card_number, expiration_date, cvv, current_user):
        return reservationService.add_credit_card(name, card_number, expiration_date, cvv, current_user)

    @classmethod
    def add_review(cls, location, rating, comment, current_user):
        return reservationService.add_review(location, rating, comment, current_user)

    @classmethod
    def get_all_reviews_by_location(cls, location):
        return reservationService.get_all_reviews_by_location(location)

    @classmethod
    def get_total_cost(cls, rooms, start_date, end_date):
        return reservationService.get_total_cost(rooms, start_date, end_date)

    @classmethod
    def delete_credit_card(cls, card_number):
        return reservationService.delete_credit_card(card_number)

    @classmethod
    def get_future_and_present_reservations(cls, current_user):
        return reservationService.get_future_and_present_reservations(str(current_user.username))

    @classmethod
    def check_credit_card(cls, card_number):
        return reservationService.check_credit_card(card_number)

    @classmethod
    def check_to_delete_credit_card(cls, card_number):
        return reservationService.check_to_delete_credit_card(card_number)

