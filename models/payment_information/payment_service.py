from paymentdao import PaymentDao
from models.payment_information.payment_information import PaymentInformation
from flask_login import current_user

paymentDao = PaymentDao()


class PaymentService:
    def __init__(self):
        pass

    @classmethod
    def add_payment_information(cls, name, expiration_date, cvv, card_number):
        payment_information = PaymentInformation(name, expiration_date, cvv, card_number, current_user)
        return paymentDao.add_payment_information(payment_information)

    @classmethod
    def get_payment_information_by_username(cls, user):
        return paymentDao.get_payment_information_by_username(user.username)
