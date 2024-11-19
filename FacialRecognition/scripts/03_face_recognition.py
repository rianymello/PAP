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

# Dicionário para armazenar rostos já reconhecidos
recognized_faces = {}
# Lista de logs para exibir no painel lateral
logs = []
max_logs = 10  # Limite máximo de mensagens no painel

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

    # Criar um painel preto para o lado direito
    height, width, _ = img.shape
    black_panel = np.zeros((height, 200, 3), dtype=np.uint8)  # 200 de largura, cor preta

    # Para cada face detectada
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar um retângulo ao redor da face

        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])  # Predizer a face

        # Verificar se a confiança é inferior a 100 (quanto menor a confiança, mais precisa a previsão)
        if confidence < 100:
            id_name = names[id]  # Nome associado ao ID
            confidence = "  {0}%".format(round(100 - confidence))  # Exibir a confiança como uma porcentagem
        else:
            id_name = "Desconhecido"
            confidence = "  {0}%".format(round(100 - confidence))

        # Colocar o nome e a confiança na imagem
        cv2.putText(img, str(id_name), (x + 5, y - 5), font, 1, (0, 0, 0), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

        # Verificar se é a primeira vez que o rosto foi reconhecido
        if id_name != "Desconhecido" and id_name not in recognized_faces:
            recognized_faces[id_name] = True  # Marcar como reconhecido
            message = f"Rosto de {id_name} reconhecido"
            logs.append(message)  # Adicionar ao log

            # Garantir que o log não ultrapasse o limite máximo
            if len(logs) > max_logs:
                logs.pop(0)  # Remover a mensagem mais antiga

    # Exibir as mensagens no painel
    y_offset = 20
    for log in logs:
        cv2.putText(black_panel, log, (10, y_offset), font, 0.5, (255, 255, 255), 1)
        y_offset += 30  # Incrementar a posição vertical para a próxima mensagem

    # Concatenar o painel preto com a imagem da câmera
    combined_image = np.hstack((img, black_panel))

    # Exibir a imagem combinada
    cv2.imshow('camera', combined_image)

    # Pressione 'ESC' para sair do vídeo
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Finalizar
print("\n [INFO] Saindo do programa e limpando os recursos")
cam.release()
cv2.destroyAllWindows()
