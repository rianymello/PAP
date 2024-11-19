import cv2
import os
import numpy as np

# Diretório de entrada (imagens processadas)
INPUT_DIR = 'data/teste'

# Nome do arquivo de saída
OUTPUT_FILE = 'data/teste_mosaico.jpg'

# Configurações do mosaico
GRID_SIZE = (3, 5)  # Número de linhas e colunas na grade (ajustar conforme o número de imagens)
CELL_SIZE = (200, 200)  # Tamanho de cada célula do mosaico (largura, altura)

# Obter a lista de arquivos processados na pasta de entrada
file_names = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# Ordenar os arquivos por nome
file_names.sort()

# Certificar-se de que há imagens suficientes para preencher a grade
if len(file_names) == 0:
    print("[ERRO] Nenhuma imagem encontrada na pasta de teste.")
    exit()

# Criar uma lista de imagens ajustadas para o mosaico
images = []
for file_name in file_names:
    img_path = os.path.join(INPUT_DIR, file_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"[WARN] Não foi possível carregar a imagem: {file_name}")
        continue

    # Obter as dimensões da imagem
    h, w, _ = img.shape
    scale = min(CELL_SIZE[0] / w, CELL_SIZE[1] / h)  # Calcular o fator de escala para manter a proporção
    new_w, new_h = int(w * scale), int(h * scale)

    # Redimensionar a imagem com proporção mantida
    resized_img = cv2.resize(img, (new_w, new_h))

    # Criar uma célula em branco e centralizar a imagem redimensionada
    cell = np.ones((CELL_SIZE[1], CELL_SIZE[0], 3), dtype=np.uint8) * 255  # Fundo branco
    y_offset = (CELL_SIZE[1] - new_h) // 2
    x_offset = (CELL_SIZE[0] - new_w) // 2
    cell[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized_img

    images.append(cell)

# Calcular o número total de imagens necessárias para preencher a grade
total_cells = GRID_SIZE[0] * GRID_SIZE[1]

# Preencher com células brancas se não houver imagens suficientes
if len(images) < total_cells:
    blank_cell = np.ones((CELL_SIZE[1], CELL_SIZE[0], 3), dtype=np.uint8) * 255  # Célula em branco
    images.extend([blank_cell] * (total_cells - len(images)))

# Organizar as imagens na grade
grid_images = []
for i in range(GRID_SIZE[0]):  # Para cada linha
    row_images = images[i * GRID_SIZE[1]:(i + 1) * GRID_SIZE[1]]  # Obter as imagens da linha
    grid_images.append(np.hstack(row_images))  # Concatenar horizontalmente

# Concatenar todas as linhas verticalmente
mosaic = np.vstack(grid_images)

# Salvar o mosaico em um arquivo
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
cv2.imwrite(OUTPUT_FILE, mosaic)

print(f"[INFO] Mosaico criado e salvo em: {OUTPUT_FILE}")
