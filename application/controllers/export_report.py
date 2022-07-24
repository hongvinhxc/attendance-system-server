from calendar import monthrange
from datetime import datetime, timedelta
from dateutil import relativedelta
import os
import xlsxwriter
from application.services.attendance import AttendanceService
from application.services.export_report import ExportReportService
from application import config
from application.log_handlers import logger
from application.services.profile import ProfileService
from application.services.working_time import WorkingTimeService
from helpers import get_seconds_from_0h, get_working_days_of_month


class ExportReportController():

    def get_reports(self, query):
        """
        get reports
        """
        size = query.pop('size')
        page = query.pop('page')
        limit = size
        offset = size * (page - 1)
        total = ExportReportService().count_export_reports(query)
        result = ExportReportService().get_export_reports(limit, offset, query)
        return {
            "rows": result,
            "total": total,
            "page": page,
            "size": size
        }

    def export_report(self, query):
        """
        export report
        """
        month = query["month"]
        status, data = self.get_attendances(query)
        time_export = datetime.now().strftime("%Y%m%d%H%M%S")
        month_export = month.strftime("%Y-%B")
        report_name = "Attendance_{month_export}_{time_export}.xlsx".format(month_export=month_export, time_export=time_export)
        report_path = os.path.join(config.PortalApi.REPORTS_FOLDER_PATH, report_name)
        workbook = xlsxwriter.Workbook(report_path)
        merge_row_format = workbook.add_format({ 'valign':   'vcenter', "num_format": "@" })
        header_row_format = workbook.add_format({ 'valign':   'vcenter','bold': True, "align": "center" })
        header_center_row_format = workbook.add_format({ 'valign':   'vcenter','bold': True, "align": "center" })
        center_row_format = workbook.add_format({ 'valign':   'vcenter', "align": "center" })
        worksheet = workbook.add_worksheet()
        worksheet.freeze_panes(3, 4)
        worksheet.write(0, 0,  "Thông tin điểm danh Tháng " + month.strftime("%m/%Y"))

        start_col = 0
        start_row = 2
        no = 1
        for row_index, item in enumerate(data):
            row = start_row + row_index * 2 + 1
            no = no + 1
            if row_index == 0:
                worksheet.set_column(start_col, start_col, 5)
                worksheet.set_column(start_col + 1, start_col + 3, 25)
                worksheet.write(start_row, start_col,  "STT", header_row_format)
                worksheet.write(start_row, start_col + 1,  "Họ và tên", header_row_format)
                worksheet.write(start_row, start_col + 2,  "Mã nhân viên", header_row_format)
                worksheet.write(start_row, start_col + 3,  "Vị trí", header_row_format)
            worksheet.merge_range(row, start_col, row + 1, start_col, no, header_center_row_format)
            worksheet.merge_range(row, start_col + 1, row + 1, start_col + 1, item["name"], merge_row_format)
            worksheet.merge_range(row, start_col + 2, row + 1, start_col + 2, item["code"], header_center_row_format)
            worksheet.merge_range(row, start_col + 3, row + 1, start_col + 3, item["position"], merge_row_format)
            col = start_col + 4
            for day, day_data in item["calendar"].items():
                if row_index == 0:
                    day = datetime.strptime(day, "%Y-%m-%d").strftime("%d/%m")
                    worksheet.write(start_row, col, day, header_center_row_format)
                field_data = ["", ""]
                if bool(day_data):
                    if day_data.get("is_absence"):
                        field_data = ["X", "X"]
                    else:
                        field_data = [datetime.strptime(day_data["attendance_times"][0], "%Y-%m-%d %H:%M:%S").strftime("%H:%M"),
                            datetime.strptime(day_data["attendance_times"][-1], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")]
                worksheet.write(row, col, field_data[0], center_row_format)
                worksheet.write(row + 1, col, field_data[1], center_row_format)
                col = col + 1
        workbook.close()

        ExportReportService().save_export_report({
            "filename": report_name,
            "report_month": month
        })
        
        return True, report_name

    def get_attendances(self, query):
        status, working_time = WorkingTimeService().get_working_time()
        if not status:
            return status, working_time

        month = query["month"]
        profiles = ProfileService().get_all_profiles()

        working_days_in_month = get_working_days_of_month(month, working_time)
        working_days_in_month_str = [day.strftime("%Y-%m-%d") for day in working_days_in_month]
        working_days_in_month = [day.day for day in working_days_in_month]
        now = datetime.now()
        monthday = monthrange(month.year, month.month)[1]
        if now.month == month.month and now.year == month.year:
            monthday = monthrange(now.year, now.month)[1]
        for profile in profiles:
            creation_month = datetime.strptime(profile["creation_date"], "%Y-%m-%d %H:%M:%S") \
                .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if creation_month > month:
                profile["calendar"] = {}
                continue
            
            _, result = AttendanceService().get_profile_attendances_by_month(profile["_id"], month)


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
                    break

                day["is_late"] = get_seconds_from_0h(day.attendance_times[0]) > morning[0]
                day["is_early"] = get_seconds_from_0h(day.attendance_times[-1]) < afternoon[1]
                day["is_not_checkin"] = get_seconds_from_0h(day.attendance_times[0]) >= afternoon[0] and len(day.attendance_times) == 1
                day["is_not_checkout"] = get_seconds_from_0h(day.attendance_times[-1]) < afternoon[0] and len(day.attendance_times) == 1
            
            for day in result:
                working_days[day.creation_date.strftime("%Y-%m-%d")] = AttendanceService().to_dict(day)

            day_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            creation_date = datetime.strptime(profile["creation_date"], "%Y-%m-%d %H:%M:%S") \
                .replace(hour=0, minute=0, second=0, microsecond=0)
         
            full_days = {}
            for delta in range(monthday):
                current_day = day_start + relativedelta.relativedelta(days=delta)
                current_day_str = current_day.strftime("%Y-%m-%d")
                if current_day < creation_date:
                    full_days[current_day_str] = {}
                    continue
                if current_day_str in working_days:
                    full_days[current_day_str] = working_days[current_day_str]
                else:
                    full_days[current_day_str] = { "is_absence": True } if current_day_str in working_days_in_month_str else {}

            profile["calendar"] = full_days

        return True, profiles

    def delete_export_report(self, profile_id):
        status, export_report = ExportReportService().get_export_report(profile_id)
        if not status:
            return status, result
        status, result = ExportReportService().delete_export_report(profile_id)
        if status:
            filename = export_report["filename"]
            file_path = os.path.join(config.PortalApi.REPORTS_FOLDER_PATH, filename)
            try:
                os.remove(file_path)
            except OSError:
                pass
        return status, result

    def download_export_report(self, profile_id):
        status, export_report = ExportReportService().get_export_report(profile_id)
        if not status:
            return status, export_report
        return status, export_report["filename"]