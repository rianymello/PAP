from flask import Flask, jsonify, request
import cv2
import numpy as np
import os
import base64

app = Flask(__name__)

# Carregar o reconhecedor e o classificador de faces
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Caminho para o arquivo do modelo treinado
trainer_path = 'trainer.yml'
recognizer.read(trainer_path)

# Carregar o classificador Haar
cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# Lista de nomes associados aos IDs (ajustar conforme seu modelo)
names = ['Riany', 'Bruno', 'Pedro', 'Diogo']  # IDs: 0 = Riany, 1 = Bruno, etc.

@app.route('/reconhecer', methods=['POST'])
def reconhecer():
    try:
        # Verificar se o JSON contém o campo 'image'
        if 'image' not in request.json:
            return jsonify({'error': 'Imagem não encontrada na requisição'}), 400

        # Receber a imagem
        img_data = base64.b64decode(request.json['image'])
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Erro ao decodificar imagem'}), 400

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

        results = []
        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 100:
                name = names[id_]
                confidence_text = f"Confidence: {round(100 - confidence)}%"
            else:
                name = "Desconhecido"
                confidence_text = "Confidence: Desconhecido"
            
            results.append({
                'name': name,
                'confidence': confidence_text,
                'coordinates': {'x': x, 'y': y, 'w': w, 'h': h}
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
