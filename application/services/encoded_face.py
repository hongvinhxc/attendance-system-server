from mongoengine import NotUniqueError, DoesNotExist, ValidationError

from application.log_handlers import logger
from application.models.encoded_face import EncodedFace
from application.services import BaseService


class EncodedFaceService(BaseService):
    def __init__(self):
        pass

    def save_encoded_face(self, id, doc):
        """
        save endcoded face
        """
        try:
            encoded_face = EncodedFace.objects(id=id)
            encoded_face.update(upsert=True, **doc)
            return True
        except Exception as error:
            logger.error(error)
        return False

    def get_encoded_faces(self):
        """
        get endcoded faces
        """
        try:
            encoded_face = EncodedFace.objects(data__not__size=0)
            return self.to_dict(list(encoded_face))
        except Exception as error:
            logger.error(error)
        return []

    def delete_encoded_face(self, encoded_face_id):
        """
        delete a endcoded faces by id
        """
        try:
            encoded_face = EncodedFace.objects.get(id=encoded_face_id)
            encoded_face.delete()
            return True, "Delete encoded face successful"
        except DoesNotExist as error:
            error_message = "An encoded face with this id does not exist"
            logger.error(error)
        except Exception as error:
            error_message = str(error)
            logger.error(error)
        return False, error_message