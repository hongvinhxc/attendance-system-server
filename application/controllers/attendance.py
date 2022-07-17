from datetime import datetime
from dateutil import relativedelta
from application.services.attendance import AttendanceService
from application.log_handlers import logger
from application.services.profile import ProfileService
from helpers import get_working_days_in_range, get_working_days_of_month


class AttendanceController():


    def get_attendances(self, query):
        month = query["month"]
        del query["month"]
        size = query.pop('size')
        page = query.pop('page')
        limit = size
        offset = size * (page - 1)
        total = ProfileService().count_profiles(query)
        result = ProfileService().get_profiles(limit, offset, query)
        working_days_in_month = get_working_days_of_month(month)
        for item in result:
            creation_date = datetime.strptime(item["creation_date"], "%Y-%m-%d %H:%M:%S") \
                .replace(hour=0, minute=0, second=0, microsecond=0)
            if creation_date.month > month.month:
                break
            if creation_date.month == month.month:
                working_days_in_month = [day for day in working_days_in_month if day > creation_date.day]
            status, attendances = AttendanceService().get_profile_attendances_by_month(item["_id"], month)
            if not status:
                break
            working_days = [day for day in attendances if day.creation_date.day in working_days_in_month]
            day_working = len(working_days)
            not_checkin = len([day for day in working_days if day.attendance_times[0].hour > 12])
            not_checkout = len([day for day in working_days if day.attendance_times[-1].hour < 13])
            day_arrive_late = len([day for day in working_days if day.attendance_times[0].hour in range(8, 13)])
            day_leave_early = len([day for day in working_days if day.attendance_times[-1].hour in range(13, 18)])
            item["absence"] = len(working_days_in_month) - day_working
            item["late"] = day_arrive_late
            item["early"] = day_leave_early
            item["not_checkin"] = not_checkin
            item["not_checkout"] = not_checkout
        return {
            "rows": result,
            "total": total,
            "page": page,
            "size": size
        }

    def get_profile_attendances_by_month(self, id, month):
        status, profile =  ProfileService().get_profile(id)
        if not status:
            return status, profile
        
        creation_month = datetime.strptime(profile["creation_date"], "%Y-%m-%d %H:%M:%S") \
            .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if creation_month > month:
            profile["calendar"] = {}
            return True, profile

        status, result = AttendanceService().get_profile_attendances_by_month_for_calendar(id, month)
        if not status:
            return status, result

        working_days_in_month = get_working_days_of_month(month)
        working_days = {}

        for day in result:
            if day.creation_date.day not in working_days_in_month:
                break
            day["is_late"] = day.attendance_times[0].hour in range(8, 13)
            day["is_early"] = day.attendance_times[-1].hour in range(13, 18)
            day["is_not_checkin"] = day.attendance_times[0].hour > 12
            day["is_not_checkout"] = day.attendance_times[-1].hour < 3
        
        for day in result:
            working_days[day.creation_date.strftime("%Y-%m-%d")] = AttendanceService().to_dict(day)

        day_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        creation_date = datetime.strptime(profile["creation_date"], "%Y-%m-%d %H:%M:%S") \
            .replace(hour=0, minute=0, second=0, microsecond=0)
        if creation_date > day_start:
            day_start = creation_date
        else:
            day_start = day_start - relativedelta.relativedelta(days=(day_start.weekday() + 1) % 7)
        
        full_days = {}
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        working_days_in_range = get_working_days_in_range(day_start, 42)
        for delta in range(42):
            current_day = day_start + relativedelta.relativedelta(days=delta)
            current_day_str = current_day.strftime("%Y-%m-%d")
            if current_day > today:
                break
            if current_day_str in working_days:
                full_days[current_day_str] = working_days[current_day_str]
            else:
                full_days[current_day_str] = { "is_absence": True } if current_day_str in working_days_in_range else {}

        profile["calendar"] = full_days
        return status, profile

    def export_attendances(self, query):
        size = query.pop('size')
        page = query.pop('page')
        limit = size
        offset = size * (page - 1)
    
        return False, ""