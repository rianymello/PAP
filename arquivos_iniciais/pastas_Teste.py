import os

def mostrar_estrutura_pastas(caminho):
    for root, dirs, files in os.walk(caminho):
        # Ignorar o diretório node_modules
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        # Excluir arquivos de imagem
        files = [f for f in files if not (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.img'))]

        # Imprimir o diretório atual
        print(f'Diretório: {root}')

        # Imprimir arquivos
        for file in files:
            print(f'  {file}')


# Substitua 'caminho/para/seu/diretorio' pelo caminho do diretório que deseja analisar
mostrar_estrutura_pastas('C:\\Users\\mello\\Desktop\\PAP')
