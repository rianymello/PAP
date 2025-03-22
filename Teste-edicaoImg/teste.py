import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

# Caminhos para as imagens originais e melhoradas
input_path = os.path.join(os.path.dirname(__file__), 'Fotos')
output_path = os.path.join(os.path.dirname(__file__), 'Fotos-Melhoradas')

# Limpar a pasta de saída (Fotos-Melhoradas) antes de salvar as novas imagens
if os.path.exists(output_path):
    for file in os.listdir(output_path):
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
else:
    os.makedirs(output_path)  # Criar a pasta se não existir

# Inicializando o detector de faces
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Contadores para rostos reconhecidos e não reconhecidos
total_rostos_reconhecidos = 0
total_rostos_nao_reconhecidos = 0

def melhorar_imagem(image_path):
    global total_rostos_reconhecidos, total_rostos_nao_reconhecidos
    
    try:
        # Abrir a imagem e converter para escala de cinza
        img = Image.open(image_path).convert('L')

        # Aumentar contraste
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)  # Aumenta o contraste em 50%

        # Converter para numpy array
        img_numpy = np.array(img, 'uint8')

        # Detectar rostos (ajustando parâmetros para detectar mais faces)
        faces = face_detector.detectMultiScale(img_numpy, scaleFactor=1.10, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print(f"Nenhum rosto detectado em {image_path}. Salvando imagem original melhorada.")
            output_file = os.path.join(output_path, os.path.basename(image_path))
            img.save(output_file)  # Salvar a imagem sem corte
            total_rostos_nao_reconhecidos += 1  # Incrementar rostos não reconhecidos
            return

        # Para cada rosto detectado, desenhar um quadrado verde e salvar
        for (x, y, w, h) in faces:
            # Desenhar quadrado verde ao redor do rosto
            cv2.rectangle(img_numpy, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Verde, espessura 2
            
            face = img_numpy[y:y+h, x:x+w]  # Recortar o rosto detectado

            # Suavizar e reduzir ruído
            face = cv2.GaussianBlur(face, (3, 3), 0)

            # Salvar imagem melhorada com o quadrado verde
            output_file = os.path.join(output_path, os.path.basename(image_path))
            cv2.imwrite(output_file, img_numpy)  # Salvar imagem com o quadrado verde
            print(f"Imagem melhorada salva em: {output_file}")

            total_rostos_reconhecidos += 1  # Incrementar rostos reconhecidos

    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")

# Processar todas as imagens na pasta de entrada
for filename in os.listdir(input_path):
    file_path = os.path.join(input_path, filename)
    if os.path.isfile(file_path):
        melhorar_imagem(file_path)

# Exibir resumo dos rostos reconhecidos e não reconhecidos
print("\n[INFO] Processamento concluído! As imagens melhoradas estão em 'Fotos-Melhoradas'.")
print(f"\nTotal de rostos reconhecidos: {total_rostos_reconhecidos}")
print(f"Total de rostos não reconhecidos: {total_rostos_nao_reconhecidos}")
