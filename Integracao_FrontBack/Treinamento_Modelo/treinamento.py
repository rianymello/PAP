import cv2
import numpy as np
import os
from PIL import Image

# Caminho para as imagens de treinamento (Agora apontando para 'Fotos-Melhoradas')
path = os.path.join(os.path.dirname(__file__), 'Fotos-Melhoradas')  # Caminho para a pasta 'Fotos-Melhoradas'

# Inicializando o reconhecedor LBPH e o detector de faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Função para obter as imagens e os IDs dos usuários
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # Pega todos os arquivos da pasta
    faceSamples = []
    ids = []
    photo_counts = {0: 0, 1: 0, 2: 0, 3: 0}  # Dicionário para contar fotos por pessoa

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
                photo_counts[id] += 1  # Incrementar a contagem de fotos da pessoa

    return faceSamples, ids, photo_counts

# Treinamento das faces
print("\n [INFO] Treinando faces. Isso pode levar alguns segundos. Aguarde...")
faces, ids, photo_counts = getImagesAndLabels(path)

# Exibindo o número de fotos para cada pessoa
print("\n[INFO] Quantidade de fotos para cada pessoa:")
for id, count in photo_counts.items():
    if id == 0:
        print(f"Riany: {count} fotos")
    elif id == 1:
        print(f"Bruno: {count} fotos")
    elif id == 2:
        print(f"Pedro: {count} fotos")
    elif id == 3:
        print(f"Diogo: {count} fotos")

# Treinamento do modelo
recognizer.train(faces, np.array(ids))

# Caminho para salvar o modelo treinado (somente dentro de 'Treiner', sem duplicação)
treiner_dir = os.path.join(os.path.dirname(__file__), 'Trainer')

# Não precisamos criar a pasta, pois ela já existe. Apenas garantir que ela seja acessada corretamente.
trainer_path = os.path.join(treiner_dir, 'trainer.yml')
recognizer.write(trainer_path)  # Salva o modelo treinado
print(f"\n [INFO] {len(np.unique(ids))} faces treinadas.")
print(f"\n [INFO] Modelo salvo em: {trainer_path}")
