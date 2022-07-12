import sys
import os
import time
sys.path = [os.path.dirname(sys.path[0])] + sys.path
from application import create_app_without_api
from application.log_handlers import logger
from application.controllers.detect_face import DetectFaceController

def thread_train_new_face():
    """
    thread train new face
    """
    app = create_app_without_api()
    with app.app_context():
        while True:
            try:
                DetectFaceController().auto_encode_new_face()
            except Exception as error:
                logger.error(error)
            time.sleep(5)
           

if __name__ == "__main__":
    thread_train_new_face()