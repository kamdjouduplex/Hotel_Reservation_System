from flask import Blueprint, render_template, redirect
from flask_login import login_required
from models.admin.admin_service import AdminService
from flask_login import current_user


admin_app = Blueprint('admin_app', __name__)
admin_service = AdminService()


@admin_app.route('/view_reservation_report', methods=['GET', 'POST'])
@login_required
def view_reservation_report():
    error = None
    months = ['August', 'September']
    report = admin_service.get_reservation_report(months)
    if not report:
        error = "There is not any data to generate a reservation report"
    return render_template('admin/view_reservation_report.html', report=report, error=error)


@admin_app.route('/view_revenue_report', methods=['GET', 'POST'])
@login_required
def view_revenue_report():
    error = None
    months = ['August', 'September']
    report = admin_service.get_revenue_reports(months)
    if not report:
        error = "There is not any data to generate a revenue report"
    return render_template('admin/view_revenue_report.html', report=report, error=error)


@admin_app.route('/view_popular_category_report', methods=['GET', 'POST'])
@login_required
def view_popular_category_report():
    error = None
    report = admin_service.get_popular_room_category_reports()
    if not report:
        error = "There is not any data to generate a revenue report"
    return render_template('admin/view_popular_category_report.html', report=report, error=error)