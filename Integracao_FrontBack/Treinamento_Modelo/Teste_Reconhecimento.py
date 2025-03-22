import cv2
import numpy as np
import os
import datetime

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

# 🔹 Função para registrar o log de reconhecimento (apenas eventos importantes)
def log_recognition(event, name=None, confidence_value=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = ""
    
    if event == "entrou":
        log_message = f"{current_time} - {name} entrou"
    elif event == "saiu":
        log_message = f"{current_time} - {name} saiu"
    
    with open("reconhecimento_log.txt", "a") as log_file:
        log_file.write(log_message + "\n")
    print(f"[LOG] {log_message}")

# 🔹 Variáveis de controle de tempo de log
last_log_time = datetime.datetime.now()
recognized_last_time = None

# Posições anteriores para movimento (direita / esquerda)
last_position_x = None

while True:
    ret, img = cam.read()  # Ler o frame da câmera
    img = cv2.flip(img, 1)  # Espelhar a imagem da câmera
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza

    # 🔹 Ajuste na detecção de faces para melhor reconhecimento de rostos distantes
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # Reduzido para detectar rostos menores
        minNeighbors=5,  # Mantém precisão sem falsos positivos excessivos
        minSize=(int(minW), int(minH)),
    )

    recognized_this_frame = False  # Flag para saber se algum rosto foi reconhecido neste frame

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar um retângulo na face

        # 🔹 Predição do modelo
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # 🔹 Ajuste da confiança para exibição
        confidence_value = round(100 - confidence)  # Converter em porcentagem

        # 🔹 Verificação da confiabilidade do reconhecimento
        if confidence_value >= 40:  # Ajuste para reconhecer apenas com confiança suficiente
            id = names[id]  # Pegar nome correspondente
            recognized_this_frame = True  # Rosto reconhecido neste frame
        else:
            id = "Desconhecido"

        # 🔹 Exibir nome e confiança na tela
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, f"{confidence_value}%", (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # 🔹 Se Riany foi reconhecida
        if id == "Riany":
            center_x = x + w // 2  # Posição centralizada do rosto (x)
            if last_position_x is None:
                last_position_x = center_x  # Inicializa a posição anterior

            # Detecta movimento de esquerda para direita
            if center_x > last_position_x + 200: 
                if recognized_last_time != "Riany":
                    log_recognition("entrou", "Riany", confidence_value)
                    recognized_last_time = "Riany"
                last_position_x = center_x

            # Detecta movimento de direita para esquerda
            elif center_x < last_position_x - 200:
                if recognized_last_time == "Riany":
                    log_recognition("saiu", "Riany", confidence_value)
                    recognized_last_time = None
                last_position_x = center_x

    # 🔹 Se nenhum rosto foi reconhecido no frame atual
    if not recognized_this_frame and recognized_last_time is not None:
        recognized_last_time = None  # Riany foi desconectada ou está fora da tela

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
