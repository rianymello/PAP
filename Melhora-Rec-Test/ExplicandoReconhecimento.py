import cv2
import face_recognition
import pickle
import numpy as np
import threading
import time
import json
from datetime import datetime, timedelta

# Carregar modelo treinado
with open("trainer.pkl", "rb") as file:
    data = pickle.load(file)

known_encodings = np.array(data["encodings"])
known_names = data["names"]

# Inicializar a câmera com DirectShow para melhor desempenho no Windows
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 160)  # Resolução mais baixa
cam.set(4, 120)  # Resolução mais baixa

print("[INFO] Iniciando reconhecimento facial... Pressione ESC para sair.")

# Variáveis para controle do processamento
process_frame = False  # Para processar um frame por vez
frame_lock = threading.Lock()
frame_to_process = None  # Guarda o frame a ser processado
running = True  # Controle do loop
frame_counter = 0  # Contador de frames para processar um a cada X capturas

# Dicionário para armazenar o tempo de entrada de cada pessoa
entry_times = {}
person_entries = {}

# Função para processar rostos de forma assíncrona
def process_faces():
    global frame_to_process, process_frame, running

    while running:
        if frame_to_process is not None:
            with frame_lock:
                small_frame = cv2.resize(frame_to_process, (0, 0), fx=0.5, fy=0.5)  # Reduzir o tamanho para ganho de desempenho
                rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # Converter para RGB

                frame_to_process = None  # Libera para o próximo processamento

            # Detectar rostos com o modelo "hog" (mais rápido e eficiente para hardware mais fraco)
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            face_landmarks_list = face_recognition.face_landmarks(rgb_frame, face_locations)

            recognized_faces = []
            for (top, right, bottom, left), face_encoding, face_landmarks in zip(face_locations, face_encodings, face_landmarks_list):
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match = np.argmin(distances)

                name = "Desconhecido"
                if distances[best_match] < 0.45:  # Ajuste de confiança para evitar erros
                    name = known_names[best_match]

                # Armazena as posições dos rostos reconhecidos
                recognized_faces.append((top * 2, right * 2, bottom * 2, left * 2, name, face_landmarks))

            # Atualiza os resultados para exibição no loop principal
            with frame_lock:
                global last_recognized_faces
                last_recognized_faces = recognized_faces

# Criar e iniciar a thread de reconhecimento facial
face_thread = threading.Thread(target=process_faces, daemon=True)
face_thread.start()

last_recognized_faces = []  # Últimos rostos reconhecidos
person_in_screen = set()  # Conjunto para controlar quem está na tela no momento

while True:
    ret, frame = cam.read()
    if not ret:
        print("[ERRO] Não foi possível acessar a câmera.")
        break

    # Espelhar a imagem (invertendo horizontalmente)
    frame = cv2.flip(frame, 1)

    # Processar um frame a cada 2 capturas (ajuste para reduzir carga)
    if frame_counter % 2 == 0:  # Processa a cada 2 frames
        with frame_lock:
            frame_to_process = frame.copy()
        process_frame = False
    else:
        process_frame = True

    frame_counter += 1

    # Desenhar os rostos reconhecidos e pontos faciais
    with frame_lock:
        for (top, right, bottom, left, name, face_landmarks) in last_recognized_faces:
            # Desenha um retângulo em torno do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Ajuste das coordenadas para compensar o redimensionamento
            height, width, _ = frame.shape
            scaling_factor = 0.5  # O fator de escala que foi usado para redimensionar a imagem

            # Desenhar pontos faciais diretamente sobre o rosto (ajustando para o tamanho original)
            for facial_feature in face_landmarks.keys():
                for point in face_landmarks[facial_feature]:
                    adjusted_point = (int(point[0] * (1 / scaling_factor)), int(point[1] * (1 / scaling_factor)))
                    cv2.circle(frame, adjusted_point, 1, (0, 0, 255), -1)

            # Verificar se a pessoa está entrando ou saindo da tela
            if name not in person_in_screen:
                if left < frame.shape[1] // 2:  # Entrando pela esquerda
                    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    entry_times[name] = time.time()
                    person_in_screen.add(name)
                    if name not in person_entries:
                        person_entries[name] = []
                    person_entries[name].append({
                        "entry_time": entry_time,
                        "exit_time": None,
                        "time_inside": None
                    })
                    print(f"[LOG] {name} entrou na tela.")
            else:
                if left > frame.shape[1] // 2:  # Saindo pela direita
                    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    duration = time.time() - entry_times[name]
                    # Atualiza a entrada da pessoa com o horário de saída e tempo dentro
                    for entry in person_entries[name]:
                        if entry["exit_time"] is None:
                            entry["exit_time"] = exit_time
                            entry["time_inside"] = str(timedelta(seconds=duration))
                            break
                    print(f"[LOG] {name} saiu da tela. Tempo dentro: {duration:.2f} segundos.")
                    person_in_screen.remove(name)

    # Mostrar o vídeo com o reconhecimento facial
    cv2.imshow("Reconhecimento Facial", frame)

    # Sair ao pressionar ESC
    if cv2.waitKey(10) & 0xFF == 27:
        running = False  # Encerra a thread de reconhecimento
        break

# Salvar os logs em um arquivo JSON
with open("logs.json", "w") as f:
    json.dump(person_entries, f, indent=4, default=str)

print("\n[INFO] Encerrando reconhecimento.")
cam.release()
cv2.destroyAllWindows()
