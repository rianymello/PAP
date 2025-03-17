from flask import Flask, render_template, Response
import cv2
from flask_cors import CORS
import sys
import os

# Importar as funções de detecção e reconhecimento facial
from deteccao import detectar_faces
from reconhecimento import reconhece_rosto

app = Flask(__name__)
CORS(app)

# Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Carregar o modelo treinado de reconhecimento facial
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../trainer/trainer.yml')  # Carregar o modelo treinado

# Função para gerar frames de vídeo com detecção e reconhecimento facial
def gen_frames():
    while True:
        ret, frame = cam.read()  # Ler o frame da câmera
        if not ret:
            break
        
        # Detecção facial
        frame = detectar_faces(frame)  # Detectar rostos
        
        # Reconhecimento facial
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Reconhecimento do rosto detectado
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence >= 45 and confidence <= 85:  # Confiança do reconhecimento (ajustar conforme necessário)
                cv2.putText(frame, f"ID: {id_}, Confiança: {round(100 - confidence)}%", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Desconhecido", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Desenhar um quadrado em volta do rosto detectado
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Converter o frame processado para JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Enviar o frame para o navegador
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para capturar vídeo em tempo real com detecção e reconhecimento de faces
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Executar o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
