import os
import base64
import shutil
from application.services.profile import ProfileService
from application import config
from application.log_handlers import logger


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
        images = []
        if doc.get("images"):
            images = doc.get("images", [])
            del doc["images"]
        code, result = ProfileService().add_profile(doc)
        if code:
            self.write_image_to_folder(result["_id"], images)
        return code, result
   
    def update_profile(self, profile_id, doc):
        images = []
        if doc.get("images"):
            images = doc.get("images", [])
            del doc["images"]
        self.write_image_to_folder(profile_id, images)
        doc["trained"] = False
        return ProfileService().update_profile(profile_id, doc)
   
    def delete_profile(self, profile_id):
        return ProfileService().delete_profile(profile_id)

    def write_image_to_folder(self, profile_id, images):
        folder_path = os.path.join(config.PortalApi.IMAGES_FOLDER_PATH, profile_id)

        shutil.rmtree(folder_path, ignore_errors=True)
        os.mkdir(folder_path)
        for index, image in enumerate(images):
            image_path = os.path.join(folder_path, str(index) + ".png")
            with open(image_path, "wb") as file:
                imgdata = base64.b64decode(image.split(",")[1])
                bytes_image = bytearray(imgdata)
                file.write(bytes_image)

    def get_profile_images(self, profile_id):
        try:
            folder_path = os.path.join(config.PortalApi.IMAGES_FOLDER_PATH, profile_id)
            images = []
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    image_path = os.path.join(folder_path, filename)
                    with open(image_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        images.append("data:image/jpeg;base64," + encoded_string.decode("utf-8"))
            return True, images
        except Exception as error:
            logger.error(error)
            return False, "Internal Error"
        