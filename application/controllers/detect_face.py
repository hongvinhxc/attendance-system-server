import base64
from datetime import datetime
import math
import pickle
import cv2
import numpy as np
import io
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn import neighbors

from application import config
from application.log_handlers import logger
from application.services.attendance import AttendanceService
from application.services.encoded_face import EncodedFaceService
from application.services.profile import ProfileService


detector = cv2.dnn.readNetFromCaffe(config.PortalApi.PROTOTXT_PATH, config.PortalApi.CAFFEMODEL_PATH)  # load model


class DetectFaceController():

    def auto_encode_new_face(self):
        """
        auto train new face
        """
        ids = ProfileService().get_untrain_profile_ids()
        if len(ids) == 0:
            return
        
        logger.info("New profile updated, start training new model")
        for id in ids:
            data_trained = self.encode_face_by_id(id)
            self.save_encode_face(id, data_trained)
            ProfileService().update_profile(id, {"trained": True})
            
        classify_data = self.classify_faces()
        self.save_model_to_file(classify_data)
            
    def encode_face_by_id(self, id):
        image_folder_path = os.path.join(config.PortalApi.IMAGES_FOLDER_PATH, id)
        if not os.path.isdir(image_folder_path):
            return []
        data = []
        for img_path in image_files_in_folder(image_folder_path):
            image = face_recognition.load_image_file(img_path)
            # sử dụng phần 1 nhận diện khuôn mặt hàm return_box_faces trả về khuôn mặt
            face_bounding_boxes = self.return_box_faces(image=image)
            if len(face_bounding_boxes) != 1:
                # nếu có nhiều hơn 1 khuôn mặt thì bỏ qua ảnh đó
                logger.debug("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
                    face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # thêm mã hóa của khuôn mặt vào mảng của dữ liệu để chuẩn bị huấn luyện
                data.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0].tolist())
        return data

    def return_box_faces(self, image):
        list_box = self.return_box(image)
        try:
            box_faces = [(box[1], box[2], box[3], box[0]) for box in list_box.astype("int")]
        except:
            box_faces = []
        # trả về danh sách các khuôn mặt detect đc dạng list tuple điểm, 1 tuple là 1 khuôn mat
        # tuple dạng (y0,x1,y1,x0)
        return box_faces

    def return_box(self, image):
        (h, w) = image.shape[:2]
        # prepares image for entrance on the model
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        # put image on model
        detector.setInput(blob)
        # propagates image through model
        detections = detector.forward()
        # check confidance of 200 predictions
        list_box = []
        for i in range(0, detections.shape[2]):
            # box --> array[x0,y0,x1,y1]
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            # confidence range --> [0-1]
            confidence = detections[0, 0, i, 2]

            if confidence >= config.PortalApi.CONFIDENCE:
                if list_box == []:
                    list_box = np.expand_dims(box, axis=0)
                else:
                    list_box = np.vstack((list_box, box))

        return list_box # trả về list các dự đoán 

    def save_encode_face(self, id, data):
        EncodedFaceService().save_encoded_face(id, {"data": data})

    def classify_faces(self):
        encoded_data = []
        labels = []

        data = EncodedFaceService().get_encoded_faces()
        for item in data:
            for encode_face in item["data"]:
                encoded_data.append(np.fromiter(encode_face, dtype=float))
                labels.append(item["_id"])

        # xác định số cụm knn hay số người cần nhận diện
        n_neighbors = int(round(math.sqrt(len(encoded_data))))
        # tạo và train
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm="ball_tree", weights='distance')
        knn_clf.fit(encoded_data, labels)

        return knn_clf

    def save_model_to_file(self, knn_clf):
        model_save_path = config.PortalApi.MODEL_TRAINED_PATH
        if model_save_path is not None:
            with open(model_save_path, 'wb') as f:
                pickle.dump(knn_clf, f)
                logger.info("Trained new model: %s", knn_clf)

    def predict_face(self, image): 
        if "," in image:
            image = image.split(",")[1]
        list_face_id = self.detect_face_id(image)
        if not list_face_id:
            return False, "No known people can be found"

        attended_ids = []
        for id in list_face_id:
            if self.update_attendance_info(id):
                attended_ids.append(id)
        
        return ProfileService().get_profiles_ids(list_face_id)

    def detect_face_id(self, image):
        """
        detect face
        """
        try:
            
            with open(config.PortalApi.MODEL_TRAINED_PATH, 'rb') as f:
                knn_clf = pickle.load(f)
            # tải ảnh và tìm kiếm khuôn mặt
            X_img = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image)))
            X_face_locations = self.return_box_faces(X_img)

            # nếu ko có khuôn mặt trả về mảng rỗng
            if len(X_face_locations) == 0:
                return None

            # chuyển khuôn mặt về dữ liệu mã hóa
            faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

            # sử dụng KNN để dự đoán và trả về kết quả
            closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
            are_matches = [closest_distances[0][i][0] <= config.PortalApi.DISTANCE_THRESHOLD for i in range(len(X_face_locations))]

            # Xóa những người có kết quả dưới ngưỡng
            return [pred for pred, rec in zip(knn_clf.predict(faces_encodings), are_matches) if rec]
        except Exception as error:
            logger.error(error)
            return None

    def update_attendance_info(self, id):
        """
        update user attandance info
        """
        now = datetime.now()
        status, attendance_info = AttendanceService().get_profile_attendance_by_day(id, now)
        if not status:
            return False
        if not attendance_info:
            doc = {
                "profile_id": id,
                "attendance_times": [now]
            }
            status, result = AttendanceService().add_attendance(doc)
            return status

        last_time = attendance_info.attendance_times[-1]
        if (now - last_time).seconds > 10:
            doc = {
                "push__attendance_times": now
            }
            status, result = AttendanceService().update_attendance(attendance_info.id, doc)
            return status
        return False