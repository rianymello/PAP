import cv2
import numpy as np
import os
import datetime

# Carregar o reconhecedor e o classificador de faces
recognizer = cv2.face.LBPHFaceRecognizer_create()

trainer_path = r"C:\Users\mello\Desktop\PAP\Integracao_FrontBack\Treinamento_Modelo\Trainer\trainer.yml"
recognizer.read(trainer_path)

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# Lista de nomes associados aos IDs
names = ['Riany', 'Bruno', 'Pedro', 'Diogo']  # IDs: 0 = Riany, 1 = Bruno, etc.

# Variáveis para controlar entrada/saída
last_position_x = {}  # Para armazenar a última posição do rosto
recognized_last_time = {}  # Para saber se a pessoa já foi registrada como 'entrou' ou 'saiu'

# Função de log
def log_recognition(event, name=None, confidence_value=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = ""
    
    if event == "entrou":
        log_message = f"{current_time} - {name} entrou"
    elif event == "saiu":
        log_message = f"{current_time} - {name} saiu. Confiança: {confidence_value}%"
        
    print(f"[LOG] {log_message}")
    return log_message

# Função exportada para reconhecimento facial e detecção de entrada/saída
def reconhece_rosto(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])  # Predizer rosto

        if confidence < 100:
            nome = names[id_]  # Nome associado ao ID
            conf_texto = f"Confidence: {round(100 - confidence)}%"
        else:
            nome = "Desconhecido"
            conf_texto = "Confidence: Desconhecido"

        # Se a pessoa foi reconhecida e não é "Desconhecido"
        if nome != "Desconhecido":
            center_x = x + w // 2  # Posição central do rosto no eixo X

            # Se a pessoa não está no dicionário de posições, adicione
            if nome not in last_position_x:
                last_position_x[nome] = center_x
                recognized_last_time[nome] = None

            # Detectar se a pessoa entrou ou saiu
            if center_x > last_position_x[nome] + 100 and recognized_last_time[nome] != nome:
                log_recognition("entrou", nome, round(100 - confidence))
                recognized_last_time[nome] = nome
                last_position_x[nome] = center_x

            elif center_x < last_position_x[nome] - 100 and recognized_last_time[nome] == nome:
                log_recognition("saiu", nome, round(100 - confidence))
                recognized_last_time[nome] = None
                last_position_x[nome] = center_x

        # Exibindo nome e confiança na imagem
        cv2.putText(frame, nome, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, conf_texto, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame  # Retorna o frame processado
