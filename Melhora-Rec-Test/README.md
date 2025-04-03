
# Reconhecimento Facial

Este projeto implementa um sistema de **reconhecimento facial** utilizando a biblioteca `face_recognition` e `OpenCV`, projetado para identificar pessoas através de uma câmera conectada ao computador. O código utiliza **Python 3** e requer algumas dependências para funcionar corretamente.

## Requisitos

1. **Python 3.x** (preferencialmente Python 3.6 ou superior)
2. **Visual C++ Build Tools** (apenas no Windows, para compilar o `dlib` usado pelo `face_recognition`).
3. **Bibliotecas do Python** (instaláveis via terminal utilizando o arquivo `requirements.txt`):
   - `opencv-python`
   - `face-recognition`
   - `numpy`

## Passos para Configuração e Execução

### 1. Instalar o Python 3.x
Baixe e instale o Python 3 a partir do [site oficial](https://www.python.org/downloads/). Durante a instalação, **marque a opção "Add Python to PATH"** para facilitar o uso de comandos no terminal.

### 2. Instalar Ferramentas de Construção C++ (Windows apenas)
**Somente no Windows**: Para compilar o `dlib`, é necessário instalar o **Visual C++ Build Tools**.

- Baixe e instale o **Visual C++ Build Tools** [aqui](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
- Durante a instalação, selecione a opção **Desktop development with C++**.
- Isso é necessário para garantir que o pacote `dlib` (usado pela biblioteca `face_recognition`) seja compilado corretamente.

### 3. Instalar Dependências Python

Instalar as Bibliotecas do `requirements.txt`
Com o ambiente virtual ativado, instale as bibliotecas necessárias utilizando o arquivo `requirements.txt`. 

Para instalar todas as dependências listadas no arquivo, execute o comando:

pip install -r requirements.txt

Caso esteja utilizando Windows e tenha problemas ao instalar o pacote `dlib`, instale-o manualmente com o comando:

pip install dlib

### 4. Configuração do Projeto

#### Baixar ou Clonar o Repositório
Se você ainda não tem o código, baixe ou clone este repositório para a máquina local.

#### Câmera
O sistema precisa de uma câmera conectada ao computador. Verifique se a câmera está funcionando corretamente.

### 5. Executando o Projeto

Execute o código: Para rodar o projeto, basta executar o script Python principal:

Reconhecimento.py


#### Acessar a janela de vídeo
O código vai abrir uma janela mostrando a captura de vídeo ao vivo com a identificação de rostos. O programa irá reconhecer as pessoas cadastradas no arquivo `trainer.pkl` e exibir os resultados no vídeo.

### 6. Gerenciamento de Logs

O programa gerará um arquivo chamado `logs.json` com informações sobre as entradas e saídas das pessoas reconhecidas, incluindo o tempo dentro da área visível.

## Problemas Comuns

### Erro ao Instalar `dlib` (Windows)
Se você encontrar problemas ao instalar a biblioteca `dlib`, isso provavelmente está relacionado às ferramentas de compilação C++ que não estão instaladas corretamente. Certifique-se de que você instalou o **Visual C++ Build Tools** conforme indicado acima.

### Erro de Permissão para Acessar a Câmera
Certifique-se de que o dispositivo de câmera esteja conectado corretamente e que o sistema operacional tenha permissões para usá-la.

### Problema de Reconhecimento
Caso o reconhecimento facial não funcione corretamente:
- Verifique se o arquivo `trainer.pkl` está presente.
- Certifique-se de que as faces estejam bem visíveis.
