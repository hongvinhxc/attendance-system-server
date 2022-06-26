from application.services.profile import ProfileService


class ProfileController():

    def get_profiles(self):
        return ProfileService().get_profiles()

    def add_profile(self, doc):
        return ProfileService().add_profile(doc)
