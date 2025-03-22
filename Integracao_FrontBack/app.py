from flask import Flask, render_template, Response
import cv2
from flask_cors import CORS
from reconhecimento import reconhece_rosto  


app = Flask(__name__)
CORS(app)

# Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Função para gerar frames de vídeo com reconhecimento facial
def gen_frames():
    while True:
        ret, frame = cam.read()  
        if not ret:
            break
        
        frame = reconhece_rosto(frame)  # Agora chamamos a função importada

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
