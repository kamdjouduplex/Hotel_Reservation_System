from flask import Flask, json
from flask import current_app
from application import db
from models.rooms.room import Room


class Reservation:
    def __init__(self, reservation_id, username, hotel_location, start_date, end_date, is_cancelled,
                 payment_information, total_cost):
        self.reservation_id = reservation_id
        self.username = username
        self.hotel_location = hotel_location
        self.start_date = start_date
        self.end_date = end_date
        self.is_cancelled = is_cancelled
        self.payment_information = payment_information
        self.total_cost = total_cost

    def get_reservation_id(self):
        return self.reservation_id

    def get_user(self):
        return self.username

    def get_hotel_location(self):
        return self.hotel_location

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_is_cancelled(self):
        return self.is_cancelled

    def get_payment_information(self):
        return self.payment_information

    def get_total_cost(self):
        return self.total_cost
