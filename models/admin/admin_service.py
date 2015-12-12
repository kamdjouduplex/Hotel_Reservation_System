from models.admin.admin_dao import AdminDao
import json

admin_dao = AdminDao()


class AdminService:
    def __init__(self):
        pass

    @classmethod
    def get_reservation_report(cls, months):
        reports = admin_dao.get_reservation_report(months)
        if len(reports) == 0:
            reports = None
        return reports

    @classmethod
    def get_revenue_reports(cls, months):
        reports = admin_dao.get_revenue_report(months)
        if len(reports) == 0:
            reports = None
        return reports

    @classmethod
    def get_popular_room_category_reports(cls):
        reports = admin_dao.get_popular_room_category_report()
        if len(reports) == 0:
            reports = None
        return reports
