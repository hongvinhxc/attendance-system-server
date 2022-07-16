import json
import random
import string
from datetime import date, datetime
from dateutil import relativedelta

from bson import ObjectId
from flask import jsonify


def random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(obj, ObjectId):
        return str(obj)
        
    raise TypeError ("Type %s not serializable" % type(obj))


def serialize_bson_respone(obj):
    return json.loads(json.dumps(obj, default=json_serial))

def pack_result(status=True, data=None, message=None):
    """
    pack result for http response
    """
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return jsonify(response)

def get_working_days_of_month(now):
    holidays = {
        date(now.year, 4, 30),
        date(now.year, 5, 1),
        date(now.year, 9, 2),
        }
    businessdays = []
    for i in range(1, 32):
        try:
            thisdate = date(now.year, now.month, i)
        except(ValueError):
            break
        if thisdate.weekday() < 5 and thisdate not in holidays: # Monday == 0, Sunday == 6 
            businessdays.append(thisdate.day)
    return businessdays

def get_working_days_in_range(start, delta):
    year = start.year
    if start.month == 12:
        year += 1
    holidays = {
        date(year, 4, 30),
        date(year, 5, 1),
        date(year, 9, 2),
        }
    businessdays = []
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(delta):
        try:
            thisdate = start + relativedelta.relativedelta(days=i)
        except(ValueError):
            break
        if thisdate.weekday() < 5 and thisdate not in holidays: # Monday == 0, Sunday == 6 
            businessdays.append(thisdate.strftime("%Y-%m-%d"))
    return businessdays