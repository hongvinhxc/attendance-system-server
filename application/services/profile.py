from application.models.profile import Profile

class ProfileService():
    def __init__(self):
        pass

    def get_profiles(self):
        profiles = Profile.objects()
        return profiles

    def add_profile(self, doc):
        profile = Profile()
        result = profile.save()
        return "Success"