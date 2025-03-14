from flask import Flask, render_template, Response
import cv2
from flask_cors import CORS

from deteccao import detectar_faces


app = Flask(__name__)
CORS(app)

# Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Função para gerar frames de vídeo com detecção facial
def gen_frames():
    while True:
        ret, frame = cam.read()  # Ler o frame da câmera
        if not ret:
            break

        frame = detectar_faces(frame)  # Aplicar o algoritmo de detecção de rostos
        
        # Converter o frame processado para JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para capturar vídeo em tempo real com detecção de faces
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Executar o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
