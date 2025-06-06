# --- Script 2: treinar_modelo.py ---
# Missão: Carregar o dataset pronto, construir uma Rede Neural Convolucional (CNN),
# treiná-la e salvar o modelo treinado para uso futuro.

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split

print("Carregando o dataset pré-processado...")
# Carrega os dados que salvamos no script anterior
dados = np.load('dataset_processado.npz')
imagens = dados['imagens']
rotulos = dados['rotulos']

print("Dataset carregado. Dividindo em conjuntos de treino e teste...")

# Divide os dados: 80% para treinar o modelo, 20% para testar sua performance
X_treino, X_teste, y_treino, y_teste = train_test_split(
    imagens, rotulos, test_size=0.2, random_state=42, stratify=rotulos
)

print(f"Dados de treino: {len(X_treino)} imagens")
print(f"Dados de teste: {len(X_teste)} imagens")

# --- Construção da Rede Neural Convolucional (CNN) ---
# Este é o nosso cérebro artificial, especializado em "ver" imagens.
modelo = Sequential([
    # 1ª Camada de Convolução: Encontra características básicas como bordas e cantos.
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D((2, 2)), # Reduz o tamanho da imagem, mantendo as características importantes.
    
    # 2ª Camada de Convolução: Encontra características mais complexas.
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # 3ª Camada de Convolução: Ainda mais complexidade.
    Conv2D(64, (3, 3), activation='relu'),
    
    # Achata a matriz 2D da imagem em um vetor 1D para a rede neural.
    Flatten(),
    
    # Camada Densa: A parte "inteligente" que toma a decisão.
    Dense(64, activation='relu'),
    Dropout(0.5), # Técnica para evitar que o modelo "decore" os dados (overfitting).
    
    # Camada de Saída: Uma única saída com 'sigmoid' para dar uma probabilidade (0 a 1).
    Dense(1, activation='sigmoid') 
])

# Compila o modelo, definindo como ele vai aprender e medir o sucesso.
modelo.compile(
    optimizer='adam', # Um otimizador popular e eficiente.
    loss='binary_crossentropy', # Função de perda ideal para classificação binária (sim/não, alagada/seca).
    metrics=['accuracy'] # Queremos que ele nos diga a acurácia (precisão) do treino.
)

print("\nModelo construído. Iniciando o treinamento...")

# --- Treinamento do Modelo ---
# O modelo vai "olhar" para as imagens de treino várias vezes (epochs) para aprender.
historico = modelo.fit(
    X_treino, y_treino,
    epochs=15, # 15 passadas completas pelo dataset. Pode aumentar se precisar de mais treino.
    validation_data=(X_teste, y_teste) # Usa os dados de teste para validar a cada passada.
)

print("\nTreinamento concluído!")

# --- Avaliação do Modelo ---
perda, acuracia = modelo.evaluate(X_teste, y_teste)
print(f"\nAcurácia do modelo no conjunto de teste: {acuracia * 100:.2f}%")

# --- Salvando o Modelo Treinado ---
# Salva o "cérebro" treinado em um único arquivo.
modelo.save('modelo_classificador_enchentes.h5')

print("\nModelo treinado foi salvo como 'modelo_classificador_enchentes.h5'!")