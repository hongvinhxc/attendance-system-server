from mongoengine import DynamicDocument
from helpers import serialize_bson_respone

class BaseService():

    def __init__(self):
        """
        constructor service
        """
        raise NotImplementedError()
      
    def to_dict(self, obj: DynamicDocument):
        if type(obj) is list:
            obj = [item.to_mongo() for item in obj]
        else:
            obj = obj.to_mongo()
        return serialize_bson_respone(obj)

    def build_regex(self, filter: dict):
        regex_filter = {}
        for field, value in filter.items():
            key = field + "__iregex"
            regex_filter[key] = value
        return regex_filter