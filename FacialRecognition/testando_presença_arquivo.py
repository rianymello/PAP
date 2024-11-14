import os

# Verifique o diretório atual
print("Diretório atual:", os.getcwd())

# Verifique se o arquivo está presente no diretório
if os.path.exists('haarcascade_frontalface_default.xml'):
    print("Arquivo encontrado!")
else:
    print("Arquivo não encontrado. Verifique o caminho.")
