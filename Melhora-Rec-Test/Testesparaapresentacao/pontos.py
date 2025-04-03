import cv2
import face_recognition
import numpy as np
import os
from PIL import Image

# Caminho absoluto da imagem
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "img2.jpeg")

# Verificar se o arquivo existe
if not os.path.exists(image_path):
    print(f"[ERRO] Arquivo '{image_path}' não encontrado. Verifique o caminho.")
    exit()

# Testar se a imagem pode ser aberta com PIL (para verificar formato)
try:
    with Image.open(image_path) as img:
        img.verify()  # Verifica se é uma imagem válida
except Exception as e:
    print(f"[ERRO] O arquivo não parece ser uma imagem válida. Detalhes: {e}")
    exit()

# Carregar a imagem com OpenCV
image = cv2.imread(image_path)
if image is None:
    print("[ERRO] OpenCV não conseguiu carregar a imagem. Possíveis causas:")
    print("1. O arquivo não é uma imagem compatível (JPEG, PNG, etc.)")
    print("2. O caminho do arquivo está incorreto")
    print("3. O arquivo pode estar corrompido")
    exit()

# Converter a imagem para RGB (face_recognition usa esse formato)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detectar rostos e pontos faciais
face_locations = face_recognition.face_locations(rgb_image, model="hog")
face_landmarks_list = face_recognition.face_landmarks(rgb_image, face_locations)

# Se nenhum rosto for detectado
if not face_landmarks_list:
    print("[ALERTA] Nenhum rosto detectado na imagem.")
    exit()

# Desenhar os pontos faciais na imagem
for face_landmarks in face_landmarks_list:
    for facial_feature in face_landmarks.keys():
        for point in face_landmarks[facial_feature]:
            cv2.circle(image, point, 1, (0, 0, 255), -1)  # Aumenta o tamanho dos pontos para melhor visibilidade

# Mostrar a imagem com os pontos faciais
title = "Pontos Faciais"
cv2.imshow(title, image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Opcional: salvar a imagem com os pontos desenhados
output_path = os.path.join(script_dir, "output.png")
cv2.imwrite(output_path, image)
print(f"[SUCESSO] Imagem processada salva em '{output_path}'")
