import cv2
import numpy as np
import os
from PIL import Image

# Caminho para as imagens de treinamento
path = 'Fotos'  # A pasta onde as fotos de treinamento (riany1,2,3,4 e bruno1,2,3) estão armazenadas

# Inicializando o reconhecedor LBPH e o detector de faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Função para obter as imagens e os IDs dos usuários
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # Pega todos os arquivos da pasta
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        # Abrir a imagem e converter para escala de cinza
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        # Extrair o ID do nome do arquivo (assumindo que o nome do arquivo contém "riany" ou "bruno")
        id = -1  # Valor inicial inválido
        if "riany" in imagePath.lower():
            id = 0
        elif "bruno" in imagePath.lower():
            id = 1

        if id != -1:  # Certificar-se de que a imagem tem um ID válido
            # Detectar as faces na imagem
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

    return faceSamples, ids

# Função para salvar as imagens com o quadrado verde ao redor dos rostos
def saveFacesWithRectangle(path, faces, ids):
    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    for imagePath, id in zip(imagePaths, ids):
        # Abrir a imagem
        PIL_img = Image.open(imagePath)
        img_numpy = np.array(PIL_img)

        # Detectar faces na imagem
        faces_detected = detector.detectMultiScale(img_numpy)
        
        # Desenhar o retângulo verde ao redor de cada rosto
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(img_numpy, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Salvar a imagem com os quadrados verdes
        filename = os.path.join("resultados", os.path.basename(imagePath))
        cv2.imwrite(filename, img_numpy)

# Treinamento das faces
print("\n [INFO] Treinando faces. Isso pode levar alguns segundos. Aguarde...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Salvar o modelo treinado na pasta trainer/
recognizer.write('trainer/trainer.yml')  # Salva o modelo treinado
print("\n [INFO] {0} faces treinadas.".format(len(np.unique(ids))))

# Salvar as imagens com o quadrado verde ao redor das faces
saveFacesWithRectangle(path, faces, ids)

print("\n [INFO] Imagens com quadrados verdes salvas na pasta 'resultados'.")
