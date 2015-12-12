from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, SelectField, validators, IntegerField, \
    SelectMultipleField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import DateField
from datetime import datetime, date
from wtforms.validators import DataRequired
from models.reservations.city import City
import re
from models.user import User
from application import db


class LoginForm(Form):
    username = StringField(u'Username Must Begin With the Letter C', [validators.DataRequired()])
    password = PasswordField(u'Password', validators=[validators.input_required()])
    remember_me = BooleanField(u'Remember Me', default=False)
    sign_in = SubmitField("Sign In")


class SignUpForm(Form):
    username = StringField(u'Username Must Begin With the Letter C', validators=[validators.DataRequired()])
    email = EmailField(u'Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField(u'Password', validators=[validators.input_required()])
    password_verify = PasswordField(u'Repeat Password', validators=[validators.input_required()])
    sign_up = SubmitField("Sign Up")


class CreateReservationPage1Form(Form):
    location = SelectField(label="City")
    stdt = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
    enddt = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
    search = SubmitField("Search")


class CreateReservationPage2Form(Form):
    check = BooleanField()
    # customer_room = SelectMultipleField(label="Rooms")
    submit = SubmitField("Submit")


class AddPaymentInformationForm(Form):
    name = StringField('Name on Card', [validators.DataRequired()])
    card_number = IntegerField('Card Number', [validators.required()])
    expiration_date = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
    cvv = IntegerField('CVV', [validators.required()])
    save = SubmitField("Save")


class DeletePaymentInformationForm(Form):
    credit_card = SelectField(label="Select Credit Card")
    delete_card = SubmitField("Delete Credit Card")


class ConfirmReservationForm(Form):
    check = BooleanField("check")
    next_page = SubmitField("Next")


class ReviewReservationForm(Form):
    credit_card = SelectField(label="Select Credit Card")
    create_reservation = SubmitField("Create Reservation")


class DeleteReservation(Form):
    reservation = BooleanField("reservation")
    submit = SubmitField("Delete")


class UpdateWhichReservation(Form):
    reservation = BooleanField("reservation")
    next_page = SubmitField("Next")


class UpdateReservationDates(Form):
    start_date = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
    search = SubmitField("Search")


class UpdateConfirm(Form):
    confirm = SubmitField("Confirm")


class ProvideFeedback(Form):
    location = SelectField("Location",
                           choices=[('', ''), ('Atlanta', 'Atlanta'), ('Savannah', 'Savannah'), ('Miami', 'Miami'),
                                    ('Orlando', 'Orlando'), ('Charlotte', 'Charlotte')],
                           validators=[validators.DataRequired()])
    rating = SelectField("Rating",
                         choices=[('', ''), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Neutral', 'Neutral'),
                                  ('Bad', 'Bad'), ('Very Bad', 'Very Bad')],
                         validators=[validators.DataRequired()])
    comment = TextAreaField("Comment")
    submit = SubmitField("Submit")


class ViewFeedbackChooseLocation(Form):
    location = SelectField("Location",
                           choices=[('', ''), ('Atlanta', 'Atlanta'), ('Savannah', 'Savannah'), ('Miami', 'Miami'),
                                    ('Orlando', 'Orlando'), ('Charlotte', 'Charlotte')],
                           validators=[validators.DataRequired()])
    search = SubmitField("Search")
