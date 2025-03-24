import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Estilo escuro para fundo preto
plt.style.use("dark_background")

# Verificando o diretório de trabalho atual
print("Diretório atual:", os.getcwd())

# Defina o caminho para o arquivo JSON no mesmo diretório
arquivo_json = os.path.join(os.getcwd(), 'Integracao_FrontBack', 'Treinamento_Modelo', 'reconhecimento_log.json')

# Carregando os dados do arquivo JSON
with open(arquivo_json, 'r') as file:
    data = json.load(file)

# Função para converter o tempo de permanência para segundos
def time_to_seconds(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

# Preparando a lista para análise
people_data = []

# Processando os dados de cada pessoa
for person in data:
    total_time = sum(time_to_seconds(entry['time_inside']) for entry in person['entries'])
    entry_count = len(person['entries'])
    person['total_time_inside_seconds'] = total_time
    person['exit_count'] = entry_count
    people_data.append(person)

# Convertendo para DataFrame
df = pd.DataFrame(people_data)

# Calculando o tempo total de permanência em horas e adicionando ao DataFrame
df['total_time_inside_hours'] = df['total_time_inside_seconds'] / 3600

# Exibindo a tabela com os dados processados de forma legível
table = df[['name', 'total_time_inside_hours', 'exit_count']]
table = table.rename(columns={'total_time_inside_hours': 'Tempo Total de Permanência (Horas)', 'exit_count': 'Quantidade de Saídas'})

# Criando a figura para os gráficos e a tabela
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('black')  # Define o fundo da janela como preto

# Ajustando a cor do texto para branco e melhorando contraste
ax.axis('tight')
ax.axis('off')

# Corrigindo as cores da tabela para garantir que o texto seja visível
table_obj = ax.table(cellText=table.values, colLabels=table.columns, loc='center',
         cellLoc='center', colColours=["#1f1f1f"] * len(table.columns),  # Fundo das colunas
         cellColours=[['#1f1f1f']*len(table.columns)]*len(table),  # Fundo das células
         rowLoc='center', colLoc='center')  # Garantir que o texto e a célula estejam centralizados

# Ajustando o texto da tabela para branco
for (i, j), cell in table_obj.get_celld().items():
    if i == 0:  # Cor para as colunas
        cell.set_text_props(color='white')
    else:  # Cor para as células
        cell.set_text_props(color='white')

plt.show()

# 1. Gráfico de Duração de Permanência (Bar Chart)
plt.figure(figsize=(8, 6))
plt.gca().set_facecolor("black")  # Fundo preto dentro do gráfico
sns.barplot(x='name', y='total_time_inside_hours', data=df, palette='Blues', hue='name', legend=False)
plt.title('Duração Total de Permanência por Pessoa (Horas)', color='white')
plt.xlabel('Nome', color='white')
plt.ylabel('Tempo de Permanência (horas)', color='white')
plt.xticks(color='white')
plt.yticks(color='white')
plt.show()

# 2. Gráfico de Frequência de Saídas (Número de Saídas)
plt.figure(figsize=(8, 6))
plt.gca().set_facecolor("black")  # Fundo preto dentro do gráfico
sns.barplot(x='name', y='exit_count', data=df, palette='Blues_r', hue='name', legend=False)
plt.title('Frequência de Saídas por Pessoa', color='white')
plt.xlabel('Nome', color='white')
plt.ylabel('Número de Saídas', color='white')
plt.xticks(color='white')
plt.yticks(color='white')
plt.show()

# 3. Gráfico de Pizza de Proporção de Tempo de Permanência
plt.figure(figsize=(8, 6))
plt.gca().set_facecolor("black")  # Fundo preto dentro do gráfico
plt.pie(df['total_time_inside_hours'], labels=df['name'], autopct='%1.1f%%', startangle=90, 
        colors=sns.color_palette("Blues", len(df)), textprops={'color': 'white'})
plt.title('Proporção do Tempo de Permanência por Pessoa', color='white')
plt.show()
