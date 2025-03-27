from flask import Flask, render_template, Response, jsonify
import cv2
from flask_cors import CORS
import datetime
from reconhecimento import reconhece_rosto

app = Flask(__name__)
CORS(app)

# Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Variáveis para armazenar logs
session_data = []  # Lista para armazenar os dados de entrada/saída

# Função para gerar frames de vídeo com reconhecimento facial
def gen_frames():
    while True:
        ret, frame = cam.read()  
        if not ret:
            break
        
        # Aqui você pode adicionar o código de reconhecimento facial
        frame = reconhece_rosto(frame)  # Chame a função para processar o frame
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Função para registrar o log
def log_recognition(event, name=None, confidence_value=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = ""
    
    if event == "entrou":
        log_message = f"{current_time} - {name} entrou"
    elif event == "saiu":
        log_message = f"{current_time} - {name} saiu. Confiança: {confidence_value}%"
        
        # Armazenando os dados no log
        session_data.append({
            'event': event,
            'name': name,
            'confidence_value': confidence_value,
            'timestamp': current_time
        })

    print(f"[LOG] {log_message}")

# Rota para exibir os logs
@app.route('/logs')
def get_logs():
    return jsonify(session_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
