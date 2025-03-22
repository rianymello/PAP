import cv2
import numpy as np
import os
from PIL import Image

# Caminho para as imagens de treinamento
path = os.path.join(os.path.dirname(__file__), 'Fotos')  # Caminho relativo à pasta FacialRecognition

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

        # Extrair o ID do nome do arquivo (assumindo que o nome do arquivo contém "riany", "bruno", "pedro" ou "diogo")
        id = -1  # Valor inicial inválido
        if "riany" in imagePath.lower():
            id = 0
        elif "bruno" in imagePath.lower():
            id = 1
        elif "pedro" in imagePath.lower():
            id = 2
        elif "diogo" in imagePath.lower():  # Novo ID para Diogo
            id = 3

        if id != -1:  # Certificar-se de que a imagem tem um ID válido
            # Detectar as faces na imagem
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

    return faceSamples, ids

# Treinamento das faces
print("\n [INFO] Treinando faces. Isso pode levar alguns segundos. Aguarde...")
faces, ids = getImagesAndLabels(path)

# Treinamento do modelo
recognizer.train(faces, np.array(ids))

# Caminho para salvar o modelo treinado
trainer_dir = os.path.join(os.path.dirname(__file__), '..', 'iniciando_integracao', 'trainer')

# Garantir que a pasta 'trainer' existe
if not os.path.exists(trainer_dir):
    os.makedirs(trainer_dir)

# Salvar o modelo treinado na pasta 'trainer/'
trainer_path = os.path.join(trainer_dir, 'trainer.yml')
recognizer.write(trainer_path)  # Salva o modelo treinado
print(f"\n [INFO] {len(np.unique(ids))} faces treinadas.")
print(f"\n [INFO] Modelo salvo em: {trainer_path}")
