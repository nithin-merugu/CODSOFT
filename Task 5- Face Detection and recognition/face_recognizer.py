import cv2
import numpy as np
import os
import pickle

class FaceRecognizer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_faces = {}
        self.current_id = 0
        self.is_model_trained = False
        self.load_trained_data()

    def add_face(self, image, name):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            return False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            if name not in self.known_faces:
                self.known_faces[name] = self.current_id
                self.current_id += 1
            
            self.recognizer.update([roi_gray], np.array([self.known_faces[name]]))
        
        self.is_model_trained = True
        self.save_trained_data()
        return True

    def recognize_faces(self, image):
        if not self.is_model_trained:
            return [], []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        face_names = []
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id_, confidence = self.recognizer.predict(roi_gray)
            
            if confidence >= 100:
                name = "Unknown"
            else:
                name = [name for name, id_value in self.known_faces.items() if id_value == id_][0]
            
            face_names.append(name)
        
        return faces, face_names

    def draw_faces(self, image, faces, face_names):
        for ((x, y, w, h), name) in zip(faces, face_names):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return image

    def save_trained_data(self):
        self.recognizer.save("trained_model.yml")
        with open("known_faces.pkl", "wb") as f:
            pickle.dump(self.known_faces, f)
        with open("current_id.pkl", "wb") as f:
            pickle.dump(self.current_id, f)
        with open("is_model_trained.pkl", "wb") as f:
            pickle.dump(self.is_model_trained, f)

    def load_trained_data(self):
        if os.path.exists("trained_model.yml"):
            self.recognizer.read("trained_model.yml")
        if os.path.exists("known_faces.pkl"):
            with open("known_faces.pkl", "rb") as f:
                self.known_faces = pickle.load(f)
        if os.path.exists("current_id.pkl"):
            with open("current_id.pkl", "rb") as f:
                self.current_id = pickle.load(f)
        if os.path.exists("is_model_trained.pkl"):
            with open("is_model_trained.pkl", "rb") as f:
                self.is_model_trained = pickle.load(f)