# --- Script 1: preparar_dataset.py ---
# Missão: Ler as imagens das pastas, padronizar o tamanho e salvar
# tudo em um único arquivo para facilitar o treinamento.

import os
from PIL import Image
import numpy as np

# --- Configurações ---
# Caminho para a pasta com as imagens que você organizou
DIRETORIO_DATASET = 'dataset_kinshasa' 
# Tamanho padrão para todas as imagens (largura, altura)
TAMANHO_IMAGEM = (128, 128)

print("Iniciando o pré-processamento das imagens...")

# Listas para guardar as imagens processadas e seus rótulos
imagens_processadas = []
rotulos = []

# Mapeia o nome da pasta para um número (nosso rótulo)
# 0 para 'seca', 1 para 'alagada'
mapa_rotulos = {'seca': 0, 'alagada': 1}

# Loop através das subpastas ('seca', 'alagada')
for nome_classe, rotulo_numerico in mapa_rotulos.items():
    
    caminho_pasta_classe = os.path.join(DIRETORIO_DATASET, nome_classe)
    print(f"Processando imagens da pasta: {nome_classe}")
    
    # Loop através de cada imagem na pasta
    for nome_arquivo in os.listdir(caminho_pasta_classe):
        try:
            # Caminho completo para a imagem
            caminho_imagem = os.path.join(caminho_pasta_classe, nome_arquivo)
            
            # Abre a imagem usando a biblioteca Pillow
            img = Image.open(caminho_imagem).convert('RGB') # Converte para RGB para garantir 3 canais de cor
            
            # Redimensiona a imagem para o tamanho padrão
            img_redimensionada = img.resize(TAMANHO_IMAGEM)
            
            # Converte a imagem para um array numpy (uma matriz de números)
            array_imagem = np.array(img_redimensionada)
            
            # Adiciona a imagem processada e seu rótulo às nossas listas
            imagens_processadas.append(array_imagem)
            rotulos.append(rotulo_numerico)

        except Exception as e:
            print(f"Erro ao processar a imagem {nome_arquivo}: {e}")

# Converte as listas para arrays numpy, que é o formato que o TensorFlow usa
imagens_processadas = np.array(imagens_processadas)
rotulos = np.array(rotulos)

# Normaliza os pixels da imagem (transforma valores de 0-255 para 0-1)
# Isso ajuda o modelo a aprender mais rápido e melhor
imagens_processadas = imagens_processadas / 255.0

print("\nPré-processamento concluído!")
print(f"Total de imagens processadas: {len(imagens_processadas)}")
print(f"Formato do array de imagens: {imagens_processadas.shape}")

# Salva os arrays processados em um único arquivo comprimido.
# Este será o nosso dataset "limpo e pronto" para o próximo script.
np.savez('dataset_processado.npz', imagens=imagens_processadas, rotulos=rotulos)

print("\nDataset salvo com sucesso no arquivo 'dataset_processado.npz'!")