from flask import Blueprint, render_template, request, redirect, session, url_for, json
from models.reservations import ReservationWeb
from models.payment_information.payment_service import PaymentService
from models.forms.forms import CreateReservationPage1Form, CreateReservationPage2Form, AddPaymentInformationForm, \
    DeleteReservation, ConfirmReservationForm, UpdateWhichReservation, UpdateReservationDates, UpdateConfirm, \
    ProvideFeedback, ViewFeedbackChooseLocation, ReviewReservationForm, DeletePaymentInformationForm
from application import login_manager
from flask_login import login_required
from flask_login import current_user
from datetime import datetime
from datetime import timedelta
from datetime import date
import uuid
from models.rooms import room_service

reservation_home_page_app = Blueprint('reservation_home_page_app', __name__)
reservationweb = ReservationWeb()
payment_service = PaymentService()
roomservice = room_service.RoomService()


@reservation_home_page_app.route('/create-reservation', methods=['GET', 'POST'])
@login_required
def create_reservation():
    form = CreateReservationPage1Form(request.form)
    error = None
    location_list = reservationweb.get_locations()
    form.location.choices = [(location, location) for location in location_list]
    if request.method == 'POST':
        location = request.form.get('location')
        start_date = request.form.get('stdt')
        end_date = request.form.get('enddt')
        if start_date == '' or end_date == '':
            error = "You cannot leave the date fields blank"
        else:
            start_date = str(start_date)
            end_date = str(end_date)
            session['loc'] = location
            session['s_date'] = start_date
            session['e_date'] = end_date
            available_reservations = reservationweb.check_for_rooms(start_date, end_date, location)
            # add serialization: session['available_rooms'] = available_reservations
            if not available_reservations:
                error = "There are no available rooms that match your criteria"
            elif datetime.strptime(start_date, "%Y-%m-%d").date() <= date.today():
                error = "You must choose a date in the future"
            elif datetime.strptime(start_date, "%Y-%m-%d").date() >= datetime.strptime(end_date, "%Y-%m-%d").date():
                error = "You must choose a checkout date after the check in date"
            else:
                return redirect('/create-reservation-2')
    return render_template('create_reservation/create_reservation_page1.html', form=form, error=error)


@reservation_home_page_app.route('/create-reservation-2', methods=['GET', 'POST'])
@login_required
def create_reservation_page2():
    error = None
    all_selected_rooms_list = []
    start_date = session['s_date']
    end_date = session['e_date']
    location = session['loc']
    available_rooms = reservationweb.check_for_rooms(start_date, end_date, location)
    # s_rooms = available_rooms.__dict__
    # print s_rooms
    size = len(available_rooms)
    form = CreateReservationPage2Form(request.form)
    i = 0
    if request.method == 'POST':
        # rooms_selected = request.form.get('customer_room')
        rooms_selected = request.form.getlist('check')
        if len(rooms_selected) == 0:
            error = "You must select at least one room"
        else:
            for rs in rooms_selected:
                for room in available_rooms:
                    if rs == str(room.room_num):
                        # room_categories_numbers = {"room_number": room.room_num, "room_category": room.category}
                        all_selected_rooms = {'room_number': room.get_room_num(), 'category': room.get_category(),
                                              'persons_allowed': room.get_num_people(), 'cost_per_day': room.get_cost(),
                                              'cost_extra_bed': room.get_cost_extra_bed(), 'extra_bed': 0}
                        all_selected_rooms_list.append(all_selected_rooms)
            session['rooms'] = all_selected_rooms_list
            session['reservation_id'] = uuid.uuid4()
            return redirect(url_for('reservation_home_page_app.confirm_reservation'))
    return render_template('create_reservation/create_reservation_page2.html', form=form,
                           available_rooms=available_rooms,
                           location=location, error=error)


@reservation_home_page_app.route('/confirm-reservation', methods=['GET', 'POST'])
@login_required
def confirm_reservation():
    rooms = session['rooms']
    extra_beds_room_numbers = []
    form = ConfirmReservationForm(request.form)
    if request.method == 'POST':
        extra_beds = request.form.getlist('check')
        for bed in extra_beds:
            extra_beds_room_numbers.append(int(bed))
        i = 0
        j = 0
        while i < len(extra_beds_room_numbers):
            if extra_beds_room_numbers[i] == rooms[j]['room_number']:
                rooms[j]['extra_bed'] = 1
                j = 0
                i += 1
            else:
                j += 1
        if len(extra_beds_room_numbers) > 0:
            session['rooms'] = rooms
        return redirect(url_for('reservation_home_page_app.review_reservation'))
    return render_template('create_reservation/confirm_reservation.html', form=form, rooms=rooms)


@reservation_home_page_app.route('/review_reservation', methods=['GET', 'POST'])
@login_required
def review_reservation():
    error = None
    start_date = session['s_date']
    end_date = session['e_date']
    location = session['loc']
    rooms = session['rooms']
    reservation_id = session['reservation_id']
    credit_cards = payment_service.get_payment_information_by_username(current_user)
    form = ReviewReservationForm(request.form)
    form.credit_card.choices = [(cc.get_card_number(), cc.get_card_number()) for cc in credit_cards]
    total_cost = reservationweb.get_total_cost(rooms, start_date, end_date)
    print rooms
    if request.method == 'POST':
        credit_card_to_use = request.form.get('credit_card')
        if credit_card_to_use is None:
            error = "You must select or add a credit card"
        else:
            reservationweb.create(reservation_id, current_user, location, start_date, end_date, credit_card_to_use, rooms)
            return redirect('/')
    return render_template('create_reservation/review_reservation.html', form=form, reservation_id=reservation_id,
                           start_date=start_date, end_date=end_date, location=location, total_cost=total_cost,
                           rooms=rooms, error=error)


@reservation_home_page_app.route('/add-credit-card', methods=['GET', 'POST'])
@login_required
def add_credit_card():
    error = None
    form = AddPaymentInformationForm(request.form)
    if request.method == 'POST':
        card_number = request.form.get('card_number')
        card_exists = reservationweb.check_credit_card(card_number)
        name = request.form.get('name')
        expiration_date = request.form.get('expiration_date')
        cvv = request.form.get('cvv')
        if card_number == '' or name == '' or expiration_date == '' or cvv == '':
            error = "All fields must be completed"
        else:
            if card_exists is True:
                error = "The card number you have entered already exists."
            else:
                reservationweb.add_credit_card(name, card_number, expiration_date, cvv, current_user)
                return redirect(url_for('reservation_home_page_app.review_reservation'))
    return render_template('user/add_credit_card.html', form=form, error=error)


@reservation_home_page_app.route('/delete-credit-card', methods=['GET', 'POST'])
@login_required
def delete_credit_card():
    error = None
    form = DeletePaymentInformationForm(request.form)
    credit_cards = payment_service.get_payment_information_by_username(current_user)
    form.credit_card.choices = [(cc.get_card_number(), cc.get_card_number()) for cc in credit_cards]
    if request.method == 'POST':
        card_number = request.form.get('credit_card')
        can_delete = reservationweb.check_to_delete_credit_card(card_number)
        if can_delete is True:
            reservationweb.delete_credit_card(card_number)
            return redirect(url_for('reservation_home_page_app.review_reservation'))
        else:
            error = "You cannot delete a card that is being used by a reservation"
    return render_template('user/delete_credit_card.html', form=form, error=error)


@reservation_home_page_app.route('/customerreservationhome')
@login_required
def customer_home():
    reservations = reservationweb.get_reservations_by_username(current_user)
    return render_template('view_reservation/view_reservation.html', reservation_list=reservations)


@reservation_home_page_app.route('/delete-reservation', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_reservation():
    error = None
    message = None
    reservation_list = reservationweb.get_future_reservations(current_user)
    form = DeleteReservation(request.form)
    if request.method == 'POST':
        reservation_to_delete = request.form.getlist('reservation')
        if len(reservation_to_delete) > 1:
            error = "You can only select one reservation to delete"
        elif len(reservation_to_delete) == 0:
            error = "You must select a reservation to delete. If none are displayed, you do not have any reservations."
        elif len(reservation_to_delete) == 1:
            reservation_to_delete = reservation_to_delete[0]
            reservation = reservationweb.get_reservation_by_reservation_id(str(reservation_to_delete))
            if datetime.strptime(reservation.start_date, "%Y-%m-%d").date() <= date.today() + timedelta(days=1):
                message = "You have successfully deleted your reservation and will receive a 0% refund of $0"
            elif datetime.strptime(reservation.start_date, "%Y-%m-%d").date() <= date.today() + timedelta(days=3):
                message = "You have successfully deleted your reservation and will receive an 80% refund of: $" + str(
                    reservation.get_total_cost() * .8)
            else:
                message = "You have successfully deleted your reservation and will receive a 100% refund of: $" + str(
                    reservation.get_total_cost())
            reservationweb.delete(reservation)
            return redirect(url_for("reservation_home_page_app.display_success_message", message=message))
    return render_template('create_reservation/cancel_reservation.html', form=form, reservation_list=reservation_list,
                           error=error)


@reservation_home_page_app.route('/view_reservation/<reservation_id>', methods=['GET', 'POST'])
@login_required
def view_reservation(reservation_id):
    reservation = reservationweb.get_reservation_by_reservation_id(reservation_id)
    return render_template('view_reservation/view_reservation.html', reservation=reservation)


@reservation_home_page_app.route('/update_reservation', methods=['GET', 'POST'])
@login_required
def update_reservation():
    error = None
    reservation_list = reservationweb.get_future_reservations(current_user)
    form = UpdateWhichReservation(request.form)
    if request.method == 'POST':
        # reservation_id = request.form.get('reservation')
        reservation_id = request.form.getlist('reservation')
        if len(reservation_id) > 1:
            error = "You can only select one reservation to update"
        else:
            reservation_id = reservation_id[0]
            reservation = reservationweb.get_reservation_by_reservation_id(str(reservation_id))
            if reservation_id is None:
                error = "You must select a reservation to delete. If none are displayed, you do not have any reservations to update."
            elif datetime.strptime(reservation.start_date, "%Y-%m-%d").date() <= date.today() + timedelta(days=3):
                error = "You cannot update reservations within 3 days of the check in date"
            else:
                return redirect(
                    url_for('reservation_home_page_app.update_reservation_check_rooms', reservation_id=reservation_id))
    return render_template('update_reservation/update_reservation.html', form=form, reservation_list=reservation_list,
                           error=error)


@reservation_home_page_app.route('/update_reservation_check_rooms/<reservation_id>', methods=['GET', 'POST'])
@login_required
def update_reservation_check_rooms(reservation_id):
    error = None
    form = UpdateReservationDates(request.form)
    reservation = reservationweb.get_reservation_by_reservation_id(reservation_id)
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        session['update_start_date'] = start_date
        session['update_end_date'] = end_date
        session['reservation_location'] = reservation.hotel_location
        session['reservation_id'] = str(reservation_id)
        if start_date == '' or end_date == '':
            error = "You cannot leave the date fields blank"
        elif datetime.strptime(start_date, "%Y-%m-%d").date() < date.today():
            error = "You must choose a date that is either today or in the future"
        elif datetime.strptime(start_date, "%Y-%m-%d").date() >= datetime.strptime(end_date, "%Y-%m-%d").date():
            error = "You must choose a checkout date after the check in date"
        else:
            # serialize this:
            available_rooms = reservationweb.search_rooms_with_new_dates(start_date, end_date,
                                                                         reservation.hotel_location,
                                                                         str(reservation_id))
            if not available_rooms:
                error = "There are no available rooms during the requested dates"
            else:
                current_rooms = roomservice.get_rooms_from_reservation_id(str(reservation_id))
                session['rooms'] = current_rooms
                return redirect(url_for('reservation_home_page_app.update_reservation_confirm_new_dates'))
    return render_template('update_reservation/update_reservation_change_dates.html', reservation=reservation,
                           form=form, error=error)


@reservation_home_page_app.route('/update_reservation_confirm_new_dates', methods=['GET', 'POST'])
@login_required
def update_reservation_confirm_new_dates():
    error = None
    form = UpdateConfirm(request.form)
    new_start_date = session['update_start_date']
    new_end_date = session['update_end_date']
    location = session['reservation_location']
    reservation_id = session['reservation_id']
    current_rooms = session['rooms']
    # available_rooms = reservationweb.search_rooms_with_new_dates(new_start_date, new_end_date, location, reservation_id)
    total_cost = reservationweb.get_total_cost(current_rooms, new_start_date, new_end_date)
    if request.method == 'POST':
        reservationweb.update_reservation_dates(reservation_id, new_start_date, new_end_date, total_cost)
        if not error:
            message = "You have successfully changed the dates of your reservation to " + new_start_date + " through " + new_end_date
            return redirect(url_for("reservation_home_page_app.display_success_message", message=message))
    return render_template('update_reservation/update_reservation_confirm_new_dates.html',
                           available_rooms=current_rooms, form=form, st_date=new_start_date, e_date=new_end_date,
                           total_cost=total_cost)


@reservation_home_page_app.route('/display_success_message/<message>', methods=['GET', 'POST'])
@login_required
def display_success_message(message):
    return render_template('index/success_page.html', message=message)


@reservation_home_page_app.route('/provide-feedback', methods=['GET', 'POST'])
@login_required
def provide_feedback():
    error = None
    form = ProvideFeedback(request.form)
    if request.method == 'POST':
        location = request.form.get('location')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        if location == '' or rating == '':
            error = "Location and/or Rating cannot be left blank"
        else:
            reservationweb.add_review(location, rating, comment, current_user)
            message = "Thank you for your feedback!"
            return redirect(url_for("reservation_home_page_app.display_success_message", message=message))
    return render_template('feedback/provide_feedback.html', form=form, error=error)


@reservation_home_page_app.route('/view-review-choose-location', methods=['GET', 'POST'])
@login_required
def view_reviews_choose_location():
    error = None
    reviews = None
    location = None
    form = ViewFeedbackChooseLocation(request.form)
    if request.method == 'POST':
        location = request.form.get('location')
        reviews = reservationweb.get_all_reviews_by_location(location)
        if location == '':
            error = "Location cannot be left blank"
        elif reviews is None:
            error = "There are no reviews for this location"
        else:
            session['reviews'] = reviews
            session['location'] = location
            # return redirect(url_for('reservation_home_page_app.view_reviews', location=location))
    return render_template('feedback/view_review_choose_location.html', form=form, error=error, reviews=reviews,
                           location=location)
