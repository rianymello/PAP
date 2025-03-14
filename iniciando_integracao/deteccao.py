import cv2

# Carregar o classificador pré-treinado de detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detectar_faces(frame):
    """Aplica detecção de rostos em um frame e retorna a imagem com os rostos detectados."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Desenhar um quadrado verde em volta de cada rosto detectado
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame  # Retorna o frame com as detecções
