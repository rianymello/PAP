import os

def list_files(startpath, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = ['node_modules', 'venv', '.git']
    
    with open("test.txt", "w") as f:
        for root, dirs, files in os.walk(startpath):
            # Remover as pastas a serem ignoradas da lista de diretórios
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            f.write(f"Pasta: {root}\n")
            for file in files:
                f.write(f"  Arquivo: {os.path.join(root, file)}\n")

# Defina o diretório de início para a busca
start_directory = r"C:\Users\mello\Desktop\ReconhecimentoFacial"

# Chama a função para listar os arquivos e salvar no arquivo
list_files(start_directory)
