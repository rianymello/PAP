from flask import Flask, render_template, Response, jsonify, send_file
import cv2
from flask_cors import CORS
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
from reconhecimento import reconhece_rosto

app = Flask(__name__)
CORS(app)

# Inicializar a captura de vídeo
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Definir largura do vídeo
cam.set(4, 480)  # Definir altura do vídeo

# Variáveis para armazenar logs
session_data = []  # Lista para armazenar os dados de entrada/saída

# Função para gerar frames de vídeo com reconhecimento facial
def gen_frames():
    while True:
        ret, frame = cam.read()  
        if not ret:
            break
        
        # Aqui você pode adicionar o código de reconhecimento facial
        frame = reconhece_rosto(frame)  # Chame a função para processar o frame
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Função para registrar o log
def log_recognition(event, name=None, confidence_value=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = ""
    
    if event == "entrou":
        log_message = f"{current_time} - {name} entrou"
    elif event == "saiu":
        log_message = f"{current_time} - {name} saiu. Confiança: {confidence_value}%"
        
        # Armazenando os dados no log
        session_data.append({
            'event': event,
            'name': name,
            'confidence_value': confidence_value,
            'timestamp': current_time
        })

    print(f"[LOG] {log_message}")

# Rota para exibir os logs
@app.route('/logs')
def get_logs():
    return jsonify(session_data)

# Função para converter o tempo de permanência para segundos
def time_to_seconds(time_str):
    if not time_str:  # Verifica se time_str é None ou string vazia
        return 0
    try:
        time_obj = datetime.strptime(time_str, '%H:%M:%S.%f')  # Considera milissegundos
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1_000_000
    except ValueError:
        print(f"Erro ao converter '{time_str}' para segundos. Definindo como 0.")
        return 0  # Caso haja erro na conversão, assume 0 segundos

# Carregar os dados do arquivo JSON (ajuste para o caminho correto)
arquivo_json = 'path/to/reconhecimento_log.json'

# Carregando os dados do arquivo JSON
with open(arquivo_json, 'r') as file:
    data = json.load(file)

# Preparando a lista para análise
people_data = []

# Processando os dados de cada pessoa
for person in data:
    total_time = sum(time_to_seconds(entry.get('time_inside')) for entry in person.get('entries', []))  # Verifica se existe 'entries'
    entry_count = len(person.get('entries', []))  # Contagem de saídas
    person['total_time_inside_seconds'] = total_time
    person['exit_count'] = entry_count
    people_data.append(person)

# Convertendo para DataFrame
import pandas as pd
df = pd.DataFrame(people_data)

# Calculando o tempo total de permanência em horas e adicionando ao DataFrame
df['total_time_inside_hours'] = df['total_time_inside_seconds'] / 3600

# Função para gerar o gráfico de Duração de Permanência
def generate_duration_plot():
    plt.figure(figsize=(8, 6))
    plt.gca().set_facecolor("black")  # Fundo preto dentro do gráfico
    sns.barplot(x='name', y='total_time_inside_hours', data=df, palette='Blues', hue='name', legend=False)
    plt.title('Duração Total de Permanência por Pessoa (Horas)', color='white')
    plt.xlabel('Nome', color='white')
    plt.ylabel('Tempo de Permanência (horas)', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plot_path = 'static/plots/duration_plot.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# Função para gerar o gráfico de Frequência de Saídas
def generate_exit_count_plot():
    plt.figure(figsize=(8, 6))
    plt.gca().set_facecolor("black")  # Fundo preto dentro do gráfico
    sns.barplot(x='name', y='exit_count', data=df, palette='Blues_r', hue='name', legend=False)
    plt.title('Frequência de Saídas por Pessoa', color='white')
    plt.xlabel('Nome', color='white')
    plt.ylabel('Número de Saídas', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plot_path = 'static/plots/exit_count_plot.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# Função para gerar o gráfico de Proporção de Tempo de Permanência
def generate_pie_chart():
    plt.figure(figsize=(8, 6))
    plt.gca().set_facecolor("black")  # Fundo preto dentro do gráfico
    plt.pie(df['total_time_inside_hours'], labels=df['name'], autopct='%1.1f%%', startangle=90, 
            colors=sns.color_palette("Blues", len(df)), textprops={'color': 'white'})
    plt.title('Proporção do Tempo de Permanência por Pessoa', color='white')
    pie_chart_path = 'static/plots/pie_chart.png'
    plt.savefig(pie_chart_path)
    plt.close()
    return pie_chart_path

# Rota para exibir os gráficos
@app.route('/graph/duration')
def get_duration_graph():
    plot_path = generate_duration_plot()
    return send_file(plot_path, mimetype='image/png')

@app.route('/graph/exit_count')
def get_exit_count_graph():
    plot_path = generate_exit_count_plot()
    return send_file(plot_path, mimetype='image/png')

@app.route('/graph/pie_chart')
def get_pie_chart():
    pie_chart_path = generate_pie_chart()
    return send_file(pie_chart_path, mimetype='image/png')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Criação do diretório para armazenar os gráficos, se necessário
    os.makedirs('static/plots', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
