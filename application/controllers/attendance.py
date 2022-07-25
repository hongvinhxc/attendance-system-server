from datetime import datetime, timedelta
from dateutil import relativedelta
from application.constants import DAY_IN_CALENDAR
from application.services.attendance import AttendanceService
from application.services.profile import ProfileService
from application.services.working_time import WorkingTimeService
from helpers import get_seconds_from_0h, get_working_days_in_range, get_working_days_of_month


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
        _, working_time = WorkingTimeService().get_working_time()
        working_days_in_month = get_working_days_of_month(month, working_time)
        working_days_in_month = [day.day for day in working_days_in_month]
        morning = [
            int(timedelta(hours=int(hour.split(":")[0]), minutes=int(hour.split(":")[1])).total_seconds())
            for hour in working_time["working_time"]["morning"]
        ]
        afternoon = [
            int(timedelta(hours=int(hour.split(":")[0]), minutes=int(hour.split(":")[1])).total_seconds())
            for hour in working_time["working_time"]["afternoon"]
        ]
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
            not_checkin = len([day for day in working_days if \
                get_seconds_from_0h(day.attendance_times[0]) > morning[1] and len(day.attendance_times) == 1])
            not_checkout = len([day for day in working_days if \
                get_seconds_from_0h(day.attendance_times[-1]) < afternoon[0] and len(day.attendance_times) == 1])
            day_arrive_late = len([day for day in working_days if get_seconds_from_0h(day.attendance_times[0]) > morning[0]])
            day_leave_early = len([day for day in working_days if get_seconds_from_0h(day.attendance_times[-1]) < afternoon[1]])
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

        status, working_time = WorkingTimeService().get_working_time()
        if not status:
            return status, working_time
        
        status, result = AttendanceService().get_profile_attendances_by_month_for_calendar(id, month)
        if not status:
            return status, result


        working_days_in_month = get_working_days_of_month(month, working_time)
        working_days_in_month = [day.day for day in working_days_in_month]
        working_days = {}

        morning = [
            int(timedelta(hours=int(hour.split(":")[0]), minutes=int(hour.split(":")[1])).total_seconds())
            for hour in working_time["working_time"]["morning"]
        ]
        afternoon = [
            int(timedelta(hours=int(hour.split(":")[0]), minutes=int(hour.split(":")[1])).total_seconds())
            for hour in working_time["working_time"]["afternoon"]
        ]

        for day in result:
            if day.creation_date.day not in working_days_in_month:
                continue
            day["is_late"] = get_seconds_from_0h(day.attendance_times[0]) > morning[0]
            day["is_early"] = get_seconds_from_0h(day.attendance_times[-1]) < afternoon[1]
            day["is_not_checkin"] = get_seconds_from_0h(day.attendance_times[0]) >= afternoon[0] and len(day.attendance_times) == 1
            day["is_not_checkout"] = get_seconds_from_0h(day.attendance_times[-1]) < afternoon[0] and len(day.attendance_times) == 1
        
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

        working_days_in_range = get_working_days_in_range(day_start, DAY_IN_CALENDAR, working_time)
        for delta in range(DAY_IN_CALENDAR):
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
