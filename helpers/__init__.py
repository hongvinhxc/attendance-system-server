import json
import random
import string
from datetime import date, datetime

from bson import ObjectId
from flask import jsonify


def random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y/%m/%d, %H:%M:%S")

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