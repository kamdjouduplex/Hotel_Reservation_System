class PaymentInformation:
    def __init__(self, name, expiration_date, cvv, card_number, user_name):
        self.name = name
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.card_number = card_number
        self.user_name = user_name

    def get_card_number(self):
        return self.card_number
