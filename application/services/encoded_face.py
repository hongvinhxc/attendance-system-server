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