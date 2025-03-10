import cv2

# Carregar o classificador pré-treinado de detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Abrir a câmera 
cap = cv2.VideoCapture(0)  # 0 para usar a webcam padrão

while True:
    # Ler um frame da câmera
    ret, frame = cap.read()
    
    # Verificar se a câmera está funcionando corretamente
    if not ret:
        print("Erro ao acessar a câmera")
        break
    
    # Converter o quadro para tons de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostos na imagem
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Desenhar um quadrado verde em volta de cada rosto detectado
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Mostrar o frame com os quadrados ao redor dos rostos
    cv2.imshow('Rostos Detectados', frame)
    
    # Para sair da execução pressione a tecla 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

# Liberar a câmera e fechar as janelas
cap.release()
cv2.destroyAllWindows()