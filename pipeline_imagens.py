# --- Script Principal: pipeline_imagens.py ---
# Missão: Orquestrar a previsão em novas imagens e registrar os resultados.

import numpy as np
import tensorflow as tf
from PIL import Image
import os
import csv
from datetime import datetime

# --- Carregamento e Configurações ---
print("Carregando o modelo treinado 'modelo_classificador_enchentes.h5'...")
try:
    modelo = tf.keras.models.load_model('modelo_classificador_enchentes.h5')
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"ERRO: Não foi possível carregar o modelo. Verifique se o arquivo existe. Detalhes: {e}")
    exit()

DB_FILE = "alert_log.csv"
TAMANHO_IMAGEM = (128, 128) # Deve ser o mesmo tamanho usado no treino.

# --- Funções Auxiliares (preparar imagem e salvar log) ---

def setup_database():
    """Cria o arquivo CSV com cabeçalho se ele não existir."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Imagem_Analisada", "Status_Previsto", "Confianca_Alagada"])
    print(f"Log de eventos configurado para salvar em '{DB_FILE}'")

def save_log(caminho_imagem, status, confianca):
    """Salva uma nova entrada no log CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nome_arquivo = os.path.basename(caminho_imagem)
    with open(DB_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, nome_arquivo, status, f"{confianca:.2%}"])
        
def preparar_imagem_unica(caminho_imagem):
    """Carrega, redimensiona e normaliza uma única imagem para o modelo."""
    try:
        img = Image.open(caminho_imagem).convert('RGB')
        img_redimensionada = img.resize(TAMANHO_IMAGEM)
        array_imagem = np.array(img_redimensionada) / 255.0
        return np.expand_dims(array_imagem, axis=0)
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em '{caminho_imagem}'")
        return None

# --- Loop Principal de Execução ---

setup_database() # Garante que o arquivo de log existe

while True:
    print("\n" + "="*50)
    caminho_imagem = input("Digite o caminho da imagem de satélite para analisar (ou 'sair'): ")

    if caminho_imagem.lower() == 'sair':
        break

    imagem_para_prever = preparar_imagem_unica(caminho_imagem)

    if imagem_para_prever is not None:
        # Faz a previsão
        previsao = modelo.predict(imagem_para_prever)
        confianca_alagada = previsao[0][0]

        # Interpreta o resultado
        if confianca_alagada > 0.5:
            status = "Área Alagada"
        else:
            status = "Área Seca"

        print(f"\n--- Resultado da Análise ---")
        print(f"Imagem: {os.path.basename(caminho_imagem)}")
        print(f"Status Previsto: {status}")
        print(f"Confiança (de ser alagada): {confianca_alagada:.2%}")
        
        # Salva o resultado no log
        save_log(caminho_imagem, status, confianca_alagada)
        print("Resultado salvo no log.")

print("\nAnálise encerrada.")