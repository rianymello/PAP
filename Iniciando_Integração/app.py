from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições do React

# Carregar classificador de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/detect', methods=['POST'])
def detect_faces():
    try:
        data = request.json.get('image', '')

        # Remover o cabeçalho Base64
        if ',' in data:
            data = data.split(",")[1]

        # Corrigir padding do Base64
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)

        # Converter Base64 para imagem OpenCV
        image_data = base64.b64decode(data)
        image_np = np.frombuffer(image_data, dtype=np.uint8)
        frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Converter para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostos
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Criar lista com coordenadas dos rostos
        faces_list = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in faces]

        return jsonify({"faces": faces_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
