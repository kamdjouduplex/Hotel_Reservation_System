from application import db
from datetime import datetime
import json


class AdminDao:
    def __init__(self):
        pass

    @classmethod
    def get_reservation_report(cls, months):
        report_list = []
        cur = db.connection.cursor()
        for month in months:
            if month == 'August':
                cur.execute(
                    "SELECT Locations.room_location, COUNT(*) AS count FROM (SELECT DISTINCT RhR.reservation_id, RhR.room_location "
                    "FROM ReservationHasRooms AS RhR INNER JOIN Reservation AS R ON RhR.reservation_id = R.reservation_id "
                    "WHERE (R.start_date >= '2015-08-01' AND R.start_date <= '2015-08-31' AND R.is_cancelled='0')) AS Locations "
                    "GROUP BY Locations.room_location ORDER BY count DESC;"
                )
            elif month == 'September':
                cur.execute(
                    "SELECT Locations.room_location, COUNT(*) AS count FROM (SELECT DISTINCT RhR.reservation_id, RhR.room_location "
                    "FROM ReservationHasRooms AS RhR INNER JOIN Reservation AS R ON RhR.reservation_id = R.reservation_id "
                    "WHERE (R.start_date >= '2015-09-01' AND R.start_date <= '2015-09-30' AND R.is_cancelled='0')) AS Locations "
                    "GROUP BY Locations.room_location ORDER BY count DESC;"
                )
            reports = cur.fetchall()
            for val in reports:
                report_dict = {
                    'month': month,
                    'location': val[0],
                    'number_reservations': val[1]
                }
                report_list.append(report_dict)
        cur.close()
        return report_list

    @classmethod
    def get_revenue_report(cls, months):
        report_list = []
        cur = db.connection.cursor()
        for month in months:
            if month == 'August':
                cur.execute(
                    "SELECT Rooms.room_location, SUM(Rooms.total_cost) FROM (SELECT DISTINCT "
                    "Reservation.reservation_id, ReservationHasRooms.room_location, Reservation.total_cost "
                    "FROM Reservation INNER JOIN ReservationHasRooms ON ReservationHasRooms.reservation_id=Reservation.reservation_id "
                    "WHERE (Reservation.start_date >= '2015-08-01' AND Reservation.start_date <= '2015-08-31')"
                    " ORDER BY ReservationHasRooms.room_location) AS Rooms GROUP BY Rooms.room_location;"
                )
            elif month == 'September':
                cur.execute(
                    "SELECT Rooms.room_location, SUM(Rooms.total_cost) FROM (SELECT DISTINCT "
                    "Reservation.reservation_id, ReservationHasRooms.room_location, Reservation.total_cost "
                    "FROM Reservation INNER JOIN ReservationHasRooms ON ReservationHasRooms.reservation_id=Reservation.reservation_id "
                    "WHERE (Reservation.start_date >= '2015-09-01' AND Reservation.start_date <= '2015-09-30')"
                    " ORDER BY ReservationHasRooms.room_location) AS Rooms GROUP BY Rooms.room_location;"
                )
            reports = cur.fetchall()
            for val in reports:
                report_dict = {
                    'month': str(month),
                    'location': val[0],
                    'total_location_revenue': val[1]
                }
                report_list.append(report_dict)
        cur.close()
        return report_list

    @classmethod
    def get_popular_room_category_report(cls):
        report_list = []
        cur = db.connection.cursor()
        cur.execute(
            "CREATE VIEW ReservationRooms AS SELECT ReservationHasRooms.room_location, ReservationHasRooms.room_number FROM Reservation NATURAL JOIN ReservationHasRooms WHERE (Reservation.is_cancelled='0' AND Reservation.start_date >= '2015-08-01' AND Reservation.end_date <= '2015-08-31');"
        )
        cur.execute(
            "CREATE VIEW RoomsCategories AS SELECT ReservationRooms.room_location, Room.room_category, COUNT(*) as total FROM ReservationRooms NATURAL JOIN Room GROUP BY ReservationRooms.room_location, Room.room_category;"
        )
        cur.execute(
            "SELECT RoomsCategories.room_category, RoomsCategories.room_location, RoomsCategories.total FROM RoomsCategories "
            "INNER JOIN (SELECT MAX(total) total, room_location FROM RoomsCategories GROUP BY room_location) AS Rooms "
            "ON Rooms.room_location = RoomsCategories.room_location AND Rooms.total = RoomsCategories.total;"
        )
        reports = cur.fetchall()
        for val in reports:
            report_dict = {
                'month': 'August',
                'category': val[0],
                'location': val[1],
                'num_reservations': val[2]
            }
            report_list.append(report_dict)
        cur.execute(
            "DROP VIEW ReservationRooms;"
        )
        cur.execute(
            "DROP VIEW RoomsCategories;"
        )
        cur.close()
        return report_list
