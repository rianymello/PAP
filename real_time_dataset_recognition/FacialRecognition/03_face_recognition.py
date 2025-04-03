import cv2
import numpy as np
import os

# Carrega o modelo treinado
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Carrega o classificador Haarcascade
cascade_path = "C:/Users/mello/Desktop/real_time_dataset_recognition/FacialRecognition/haarcascade_frontalface_default.xml"
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {cascade_path}")
face_cascade = cv2.CascadeClassifier(cascade_path)

# Define a fonte para exibição
font = cv2.FONT_HERSHEY_SIMPLEX

# Lista de nomes associados aos IDs
names = ['None', 'riany', 'Tom holand', 'pedro'] 

# Inicializa a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Largura
cam.set(4, 480)  # Altura

# Define o tamanho mínimo da janela para ser reconhecida como rosto
min_w = int(0.1 * cam.get(3))
min_h = int(0.1 * cam.get(4))

while True:
    ret, img = cam.read()
    if not ret:
        print("[ERRO] Falha ao capturar imagem.")
        break
    
    img = cv2.flip(img, 1)  # Espelha a imagem para visualização natural
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(min_w, min_h)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        
        if id < len(names):  # Evita erro se o ID for maior que a lista de nomes
            name = names[id]
        else:
            name = "Desconhecido"
        
        confidence_text = f"{100 - confidence:.2f}%" if confidence < 100 else "Desconhecido"
        
        # Criar retângulo abaixo do rosto para o nome
        rect_height = 30  # Altura do retângulo para o nome
        cv2.rectangle(img, (x, y + h), (x + w, y + h + rect_height), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x + 5, y + h + 20), font, 0.7, (255, 255, 255), 2)
        cv2.putText(img, confidence_text, (x + 5, y + h - 5), font, 0.7, (255, 255, 0), 1)
    
    cv2.imshow('Reconhecimento Facial', img)
    
    if cv2.waitKey(10) & 0xFF == 27:  # Pressione 'ESC' para sair
        break

# Libera os recursos
print("\n[INFO] Encerrando programa e liberando recursos.")
cam.release()
cv2.destroyAllWindows()
