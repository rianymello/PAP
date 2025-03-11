from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Função para gerar frames de vídeo para o Flask
def gen_frames():
    while True:
        ret, img = cam.read()  # Ler o frame da câmera
        if not ret:
            break
        
        # Convertendo a imagem para JPEG para enviar ao navegador
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para capturar vídeo em tempo real
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Executar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
