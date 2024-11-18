import cv2
import numpy as np
import os

# Carregar o reconhecedor e o classificador de faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('models/trainer.yml')  # Caminho atualizado para o modelo treinado

cascadePath = "haarcascades/haarcascade_frontalface_default.xml"  # Caminho atualizado para o Haar Cascade
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# Lista de nomes associados aos IDs
names = ['Riany', 'Bruno', 'Pedro', 'Diogo']  # IDs: 0 = Riany, 1 = Bruno, 2 = Pedro, 3 = Diogo

# Iniciar captura de vídeo em tempo real
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Definir o tamanho mínimo da janela para ser reconhecida como uma face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()  # Ler o frame da câmera

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza

    # Detectar faces na imagem
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    # Para cada face detectada
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar um retângulo ao redor da face

        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])  # Predizer a face

        # Verificar se a confiança é inferior a 100 (quanto menor a confiança, mais precisa a previsão)
        if confidence < 100:
            id = names[id]  # Nome associado ao ID
            confidence = "  {0}%".format(round(100 - confidence))  # Exibir a confiança como uma porcentagem
        else:
            id = "Desconhecido"
            confidence = "  {0}%".format(round(100 - confidence))

        # Colocar o nome e a confiança na imagem
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (0, 0, 0), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

    # Exibir a imagem com a face detectada
    cv2.imshow('camera', img)

    # Pressione 'ESC' para sair do vídeo
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Finalizar
print("\n [INFO] Saindo do programa e limpando os recursos")
cam.release()
cv2.destroyAllWindows()
