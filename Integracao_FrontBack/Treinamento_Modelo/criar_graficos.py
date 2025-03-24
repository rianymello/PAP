import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Carregando os dados do arquivo JSON
with open('reconhecimento_log.json', 'r') as file:
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

# Tabela com os dados
ax.axis('tight')
ax.axis('off')
ax.table(cellText=table.values, colLabels=table.columns, loc='center', cellLoc='center', colColours=["#f5f5f5"] * len(table.columns))

# 1. Gráfico de Duração de Permanência (Bar Chart)
plt.figure(figsize=(8, 6))
sns.barplot(x='name', y='total_time_inside_hours', data=df, palette='viridis')
plt.title('Duração Total de Permanência por Pessoa (Horas)')
plt.xlabel('Nome')
plt.ylabel('Tempo de Permanência (horas)')
plt.show()

# 2. Gráfico de Frequência de Saídas (Número de Saídas)
plt.figure(figsize=(8, 6))
sns.barplot(x='name', y='exit_count', data=df, palette='Blues')
plt.title('Frequência de Saídas por Pessoa')
plt.xlabel('Nome')
plt.ylabel('Número de Saídas')
plt.show()

# 3. Gráfico de Pizza de Proporção de Tempo de Permanência
plt.figure(figsize=(8, 6))
plt.pie(df['total_time_inside_hours'], labels=df['name'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(df)))
plt.title('Proporção do Tempo de Permanência por Pessoa')
plt.show()
