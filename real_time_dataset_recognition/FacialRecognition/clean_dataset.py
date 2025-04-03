import os

# Caminho da pasta 'dataset'
dataset_path = "dataset"

# Função para limpar a pasta
def clear_dataset():
    # Verifica se a pasta existe
    if os.path.exists(dataset_path):
        # Contador para verificar se algum arquivo foi removido
        files_removed = 0
        # Remove todos os arquivos dentro da pasta (sem remover subpastas)
        for filename in os.listdir(dataset_path):
            file_path = os.path.join(dataset_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove apenas arquivos, não diretórios
                    files_removed += 1  # Incrementa o contador
            except Exception as e:
                print(f"[ERRO] Não foi possível excluir {file_path}. Motivo: {e}")
        
        if files_removed > 0:
            print(f"\n[INFO] Limpeza concluída.")
        else:
            print("[INFO] Nenhum arquivo encontrado para remover.")

# Chama a função para limpar
clear_dataset()
