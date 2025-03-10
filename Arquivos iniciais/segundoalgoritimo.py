import cv2
import face_recognition
import os
import numpy as np

# Carregar as imagens de referência e obter os encodings faciais
known_face_encodings = []
known_face_names = []

# Caminho da pasta onde estão as suas fotos
image_folder = "Fotos"

# Carregar e codificar cada imagem da pasta
for image_name in os.listdir(image_folder):
    # Carregar imagem e obter o encoding do rosto
    image_path = os.path.join(image_folder, image_name)
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    # Verificar se a imagem tem ao menos um rosto detectado
    if face_encodings:
        known_face_encodings.append(face_encodings[0])

        # Extrair o nome da imagem sem a extensão e adicionar a lista
        name = os.path.splitext(image_name)[0]  
        known_face_names.append(name)
                                                         
# Inicializar a câmera
cap = cv2.VideoCapture(0)

while True:
    # Ler um frame da câmera
    ret, frame = cap.read()
    if not ret:
        print("Erro ao acessar a câmera")
        break

    # Reduzir o tamanho do frame para processamento mais rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Substituindo a linha conforme solicitado
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])  # Converter BGR para RGB de forma contígua

    # Encontrar todos os rostos e seus encodings no frame atual
    face_locations = face_recognition.face_locations(rgb_small_frame)

    # Só tentar obter encodings se face_locations não estiver vazio
    face_encodings = []
    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        continue

    # Comparar os rostos detectados com o rosto conhecido
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Comparar rosto atual com os encodings conhecidos
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Desconhecido"

        # Usar o nome do primeiro rosto correspondente na lista
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]

        # Escalar as coordenadas do rosto de volta para o tamanho original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenhar o retângulo e o nome
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Exibir o frame com o reconhecimento facial
    cv2.imshow("Reconhecimento Facial", frame)

    # Pressione 's' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
2
# Liberar a câmera e fechar as janelas
cap.release()
cv2.destroyAllWindows()