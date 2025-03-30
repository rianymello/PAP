import os
from PIL import Image, ImageEnhance, ImageFilter
import random

# Função para aplicar o aumento de flip
def flip_image(image, filename, output_folder):
    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_image = flipped_image.convert("RGB")  # Garantir que está no formato RGB
    flipped_image.save(os.path.join(output_folder, f'{filename}_flip.jpg'))

# Função para aplicar o aumento de blur
def blur_image(image, filename, output_folder):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 3)))
    blurred_image = blurred_image.convert("RGB")  # Garantir que está no formato RGB
    blurred_image.save(os.path.join(output_folder, f'{filename}_blur.jpg'))

# Função para aplicar o aumento de rotação
def rotate_image(image, filename, output_folder):
    angle = random.uniform(-30, 30)
    rotated_image = image.rotate(angle)
    rotated_image = rotated_image.convert("RGB")  # Garantir que está no formato RGB
    rotated_image.save(os.path.join(output_folder, f'{filename}_rotate.jpg'))

# Função para aplicar o aumento de brilho
def brightness_image(image, filename, output_folder):
    enhancer = ImageEnhance.Brightness(image)
    factor = random.uniform(0.8, 1.2)
    brightened_image = enhancer.enhance(factor)
    brightened_image = brightened_image.convert("RGB")  # Garantir que está no formato RGB
    brightened_image.save(os.path.join(output_folder, f'{filename}_brightness.jpg'))

# Função para aplicar o aumento de ruído
def noise_image(image, filename, output_folder):
    width, height = image.size
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            r, g, b = image.getpixel((i, j))[:3]  # Ignorar canal alpha
            noise = random.randint(-20, 20)
            r = min(255, max(0, r + noise))
            g = min(255, max(0, g + noise))
            b = min(255, max(0, b + noise))
            pixels[i, j] = (r, g, b)
    image = image.convert("RGB")  # Garantir que está no formato RGB
    image.save(os.path.join(output_folder, f'{filename}_noise.jpg'))

# Função para carregar as imagens de treinamento
def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('jpg', 'jpeg', 'png')):
            img_path = os.path.join(folder, filename)
            img = Image.open(img_path)
            images.append(img)
            filenames.append(filename)
    return images, filenames

# Caminhos absolutos para as pastas
input_folder = r'C:\Users\mello\Desktop\PAP\Melhora-Rec-Test\Fotos'  # Pasta com fotos originais
output_folder = r'C:\Users\mello\Desktop\PAP\Melhora-Rec-Test\FotosMelhoradas'  # Pasta para salvar fotos aumentadas

# Verificar se a pasta de saída existe, caso contrário, criar
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Carregar as imagens da pasta 'Fotos'
images, filenames = load_images_from_folder(input_folder)

# Para cada imagem, aplicar as transformações
for idx, img in enumerate(images):
    filename = filenames[idx].split('.')[0]  # Remover a extensão do nome do arquivo
    flip_image(img, filename, output_folder)
    blur_image(img, filename, output_folder)
    rotate_image(img, filename, output_folder)
    brightness_image(img, filename, output_folder)
    noise_image(img, filename, output_folder)

print("Imagens aumentadas foram salvas com sucesso em 'FotosMelhoradas'!")
