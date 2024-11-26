import cv2
import os

# Caminhos das pastas
INPUT_FOLDER = 'data/fotos'
OUTPUT_FOLDER = 'data/teste'

# Criar a pasta de saída, se não existir
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Carregar o classificador Haar Cascade
cascade_path = 'haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# Verificar se o Haar Cascade foi carregado corretamente
if face_cascade.empty():
    raise IOError("Falha ao carregar o arquivo Haar Cascade em: " + cascade_path)

# Iterar por cada arquivo na pasta de entrada
for filename in os.listdir(INPUT_FOLDER):
    input_path = os.path.join(INPUT_FOLDER, filename)
    
    # Verificar se é um arquivo de imagem
    if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.png') or filename.lower().endswith('.jpeg')):
        continue
    
    # Ler a imagem
    image = cv2.imread(input_path)
    if image is None:
        print(f"Erro ao carregar a imagem: {input_path}")
        continue
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostos
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Desenhar retângulos ao redor dos rostos detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Caminho de saída
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    
    # Salvar a imagem com os rostos detectados
    cv2.imwrite(output_path, image)
    print(f"Rostos detectados e imagem salva em: {output_path}")

print("Processamento concluído.")
