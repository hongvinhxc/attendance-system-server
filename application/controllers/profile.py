from itertools import count
from application.services.profile import ProfileService


class ProfileController():

    def get_profiles(self, query):
        size = query.pop('size')
        page = query.pop('page')
        limit = size
        offset = size * (page - 1)
        total = ProfileService().count_profiles(query)
        result = ProfileService().get_profiles(limit, offset, query)
        return {
            "rows": result,
            "total": total,
            "page": page,
            "size": size
        }

    def get_profile(self, profile_id):
        return ProfileService().get_profile(profile_id)

    def add_profile(self, doc):
        return ProfileService().add_profile(doc)
   
    def update_profile(self, profile_id, doc):
        return ProfileService().update_profile(profile_id, doc)
