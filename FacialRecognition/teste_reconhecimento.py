import cv2
import numpy as np

# Caminho para o modelo treinado
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')  # Carrega o modelo treinado

# Caminho para o classificador de face Haar
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Lista de nomes correspondentes aos IDs (ajustar conforme os IDs atribuídos durante o treinamento)
names = ['Riany', 'Bruno', 'Pedro', 'Diogo']  # IDs: 0 = Riany, 1 = Bruno, 2 = Pedro, 3 = Diogo

# Carregar a imagem de teste
imagePath = 'teste4.jpg'  # Troque pelo caminho da sua imagem de teste
img = cv2.imread(imagePath)

# Converter a imagem para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detectar faces na imagem
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# Verificar se alguma face foi detectada
if len(faces) == 0:
    print("Nenhuma face detectada.")
else:
    for (x, y, w, h) in faces:
        # Recortar a face detectada
        face_region = gray[y:y+h, x:x+w]

        # Fazer a predição (identificação da pessoa)
        id, confidence = recognizer.predict(face_region)

        # Definir a variável 'name' dependendo da confiança
        if confidence < 100:
            name = names[id]  # Nome da pessoa com base no ID
            confidence = round(100 - confidence)  # Confiança da predição
            print(f"Pessoa identificada: {name}, Confiança: {confidence}%")
        else:
            name = "Desconhecido"  # Caso a pessoa não seja reconhecida
            confidence = round(100 - confidence)  # Confiança da predição
            print(f"Pessoa desconhecida. Confiança: {confidence}%")

        # Desenhar um retângulo ao redor da face detectada
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, str(name), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Salvar a imagem com o nome e o retângulo desenhado ao redor da face
    output_image_path = "teste_identificado.jpg"
    cv2.imwrite(output_image_path, img)  # Salva a imagem com a identificação

    print(f"A imagem foi salva com o nome identificado em {output_image_path}.")
