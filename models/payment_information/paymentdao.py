from models.payment_information.payment_information import PaymentInformation
from application import db
from flask_login import current_user


class PaymentDao:
    def __init__(self):
        pass

    @classmethod
    def add_payment_information(cls, payment):
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute(
            "INSERT INTO PaymentInformation (name_on_card, card_number, expiration_date, cvv, user_name) "
            "VALUES (%s, %s, %s, %s, %s)",
            (payment.name, payment.card_number, payment.expiration_date, payment.cvv, current_user.username))
        cur.commit()
        cursor.close()
        return payment

    @classmethod
    def get_payment_information_by_username(cls, username):
        payment_information = set()
        cur = db.connection.cursor()
        cur.execute("SELECT name_on_card, card_number, expiration_date, cvv FROM PaymentInformation WHERE user_name='%s';" % username)
        location_instance = cur.fetchall()
        for val in location_instance:
            name_on_card = val[0]
            card_number = val[1]
            expiration_date = val[2]
            cvv = val[3]
            payment_information.add(PaymentInformation(name_on_card, expiration_date, cvv, card_number, username))
        cur.close()
        return payment_information
