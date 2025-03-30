import os
import face_recognition
import pickle
import numpy as np

# Caminho da pasta de imagens
image_folder = r"c:\Users\mello\Desktop\PAP\Melhora-Rec-Test\Fotos"

# Nomes conhecidos
names = ["Riany", "Bruno", "Pedro", "Diogo"]

# Dicionário para armazenar os embeddings
encodings_dict = {}

for name in names:
    encodings_dict[name] = []

# Processar todas as imagens
for file in os.listdir(image_folder):
    if file.endswith((".jpg", ".jpeg", ".png")):
        for name in names:
            if name.lower() in file.lower():  # Verifica se o nome está na imagem
                image_path = os.path.join(image_folder, file)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    encodings_dict[name].append(face_encodings[0])
                    print(f"Processando: {file} - Nome: {name}")

# Criar um único vetor de reconhecimento por pessoa (média dos embeddings)
final_encodings = []
final_names = []

for name, encodings in encodings_dict.items():
    if encodings:  # Apenas se tiver imagens
        mean_encoding = np.mean(encodings, axis=0)  # Média dos vetores
        final_encodings.append(mean_encoding)
        final_names.append(name)

# Salvar os dados treinados
data = {"encodings": final_encodings, "names": final_names}
with open("trainer.pkl", "wb") as file:
    pickle.dump(data, file)

print("\n[INFO] Treinamento concluído! Modelo salvo em 'trainer.pkl'.")
