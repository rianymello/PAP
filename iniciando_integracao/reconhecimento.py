import cv2
import numpy as np
import os

# Carregar o reconhecedor e o classificador de faces
recognizer = cv2.face.LBPHFaceRecognizer_create()

trainer_path = os.path.join(os.path.dirname(__file__), "trainer", "trainer.yml")
recognizer.read(trainer_path)


cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# Lista de nomes associados aos IDs
names = ['Riany', 'Bruno', 'Pedro', 'Diogo']  # IDs: 0 = Riany, 1 = Bruno, etc.


# Função exportada
def reconhece_rosto(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])  # Predizer rosto

        if confidence < 100:
            nome = names[id_]  # Nome associado ao ID
            conf_texto = f"Confiança: {round(100 - confidence)}%"
        else:
            nome = "Desconhecido"
            conf_texto = "Confiança: Desconhecido"

        cv2.putText(frame, nome, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, conf_texto, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame  # Retorna o frame processado
