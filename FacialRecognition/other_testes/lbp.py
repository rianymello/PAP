import cv2
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o LBP
def local_binary_pattern(image, radius, points):
    height, width = image.shape
    lbp_image = np.zeros_like(image)

    for i in range(radius, height - radius):
        for j in range(radius, width - radius):
            center = image[i, j]
            binary_pattern = 0

            for p in range(points):
                angle = 2 * np.pi * p / points
                x_offset = int(radius * np.cos(angle))
                y_offset = int(radius * np.sin(angle))

                # Pixel vizinho
                neighbor = image[i + y_offset, j + x_offset]
                binary_pattern |= (neighbor >= center) << p

            lbp_image[i, j] = binary_pattern

    return lbp_image

# Configuração do LBP
RADIUS = 1  # Raio ao redor de cada pixel
POINTS = 8 * RADIUS  # Número de vizinhos ao redor de cada pixel

# Carregar a imagem em escala de cinza
image = cv2.imread('data/fotos/bruno1.jpg', cv2.IMREAD_GRAYSCALE)

# Verificar se a imagem foi carregada corretamente
if image is None:
    print("Erro ao carregar a imagem. Verifique o caminho.")
else:
    # Aplicar o LBP usando a função customizada
    lbp = local_binary_pattern(image, RADIUS, POINTS)

    # Calcular o histograma do LBP
    (hist, _) = np.histogram(lbp.ravel(),
                             bins=np.arange(0, POINTS + 3),
                             range=(0, POINTS + 2))

    # Normalizar o histograma
    hist = hist.astype("float")
    hist /= hist.sum()

    # Visualizar os resultados
    plt.figure(figsize=(12, 8))

    # Imagem original
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagem Original')
    plt.axis('off')

    # Imagem com LBP aplicado
    plt.subplot(1, 3, 2)
    plt.imshow(lbp, cmap='gray')
    plt.title('Padrão LBP')
    plt.axis('off')

    # Histograma LBP
    plt.subplot(1, 3, 3)
    plt.bar(range(0, len(hist)), hist, width=0.5, color='blue')
    plt.title('Histograma LBP')
    plt.xlabel('Padrões Binários')
    plt.ylabel('Frequência')

    plt.tight_layout()
    plt.show()
