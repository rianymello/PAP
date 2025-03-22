import cv2
import numpy as np
import os

# 🔹 Criando o reconhecedor LBPH com parâmetros ajustados
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=10, grid_x=8, grid_y=8)

# 🔹 Caminho do modelo treinado (certifique-se de re-treinar o modelo antes de testar!)
trainer_path = os.path.join(os.path.dirname(__file__), 'Treiner', 'trainer.yml')
recognizer.read(trainer_path)

# 🔹 Caminho correto para o Haarcascade
cascadePath = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascadePath)

# 🔹 Fonte para exibição do texto na imagem
font = cv2.FONT_HERSHEY_SIMPLEX

# 🔹 Lista de nomes associados aos IDs (ajuste conforme necessário)
names = ['Riany', 'Bruno', 'Pedro', 'Diogo']  # IDs: 0 = Riany, 1 = Bruno, 2 = Pedro, 3 = Diogo

# 🔹 Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Largura do vídeo
cam.set(4, 480)  # Altura do vídeo

# 🔹 Definir o tamanho mínimo para considerar um rosto
minW = 0.08 * cam.get(3)  # Ajustado para detecção de rostos menores
minH = 0.08 * cam.get(4)

while True:
    ret, img = cam.read()  # Ler o frame da câmera
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza

    # 🔹 Ajuste na detecção de faces para melhor reconhecimento de rostos distantes
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # Reduzido para detectar rostos menores
        minNeighbors=5,  # Mantém precisão sem falsos positivos excessivos
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar um retângulo na face

        # 🔹 Predição do modelo
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # 🔹 Ajuste da confiança para exibição
        confidence_value = round(100 - confidence)  # Converter em porcentagem

        # 🔹 Verificação da confiabilidade do reconhecimento
        if confidence_value >= 40: # Ajuste para reconhecer apenas com confiança suficiente
            id = names[id]  # Pegar nome correspondente
        else:
            id = "Desconhecido"

        # 🔹 Exibir nome e confiança na tela
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, f"{confidence_value}%", (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    # 🔹 Mostrar imagem com detecção
    cv2.imshow('camera', img)

    # 🔹 Pressione 'ESC' para sair do programa
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# 🔹 Encerrar a captura de vídeo
print("\n [INFO] Saindo do programa e limpando os recursos")
cam.release()
cv2.destroyAllWindows()
