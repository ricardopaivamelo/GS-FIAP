# Análise Inteligente de Desastres Naturais: Detecção de Enchentes (Global Solution 2025.1)

Projeto desenvolvido para a Global Solution da FIAP, com o objetivo de criar uma pipeline híbrida de Visão Computacional e IoT para prever, monitorar e mitigar os impactos de enchentes.

---

### Integrantes do Grupo

*   Nicolas Lemos Ribeiro: RM 553273
*   Luiz Felipe Alves Gomes: RM 565151
*   Ricardo de Paiva Melo: RM 565522
*   Artur de Carvalho: RM 558646
*   Caíque de Souza maulen: RM 560700

---

### 🚀 Tecnologias Utilizadas

*   **Linguagem Principal:** Python
*   **Machine Learning:** TensorFlow / Keras (para a Rede Neural Convolucional)
*   **Análise e Visualização de Dados:** R / R Shiny (para o Dashboard Interativo)
*   **IoT:** C++ (Arduino) para o firmware do ESP32 (simulado no Wokwi)
*   **Bibliotecas Python:** Pillow, NumPy, Scikit-learn
*   **Fonte de Dados:** UNOSAT / Disasters Charter (Relatório sobre a enchente em Kinshasa, RD Congo)

---

### 📂 Estrutura do Repositório

*   `preparar_dataset.py`: Script para processar as imagens brutas e criar o dataset.
*   `treinar_modelo.py`: Script que carrega o dataset, constrói, treina e salva o modelo de CNN.
*   `pipeline_imagens.py`: Script principal que carrega o modelo treinado e classifica novas imagens de satélite.
*   `dashboard.R`: Código da aplicação R Shiny para visualização dos resultados em tempo real.
*   `firmware_esp32.ino`: Código para o sensor simulado no Wokwi.
*   `/dataset_kinshasa`: Pasta contendo as imagens de treino e teste.

---

### 📋 Como Executar

1.  **Pré-requisitos:** Ter Python, R e as bibliotecas listadas instaladas.
2.  **Treinamento (Opcional, modelo já treinado):**
    *   Execute `python preparar_dataset.py` para criar o arquivo `dataset_processado.npz`.
    *   Execute `python treinar_modelo.py` para treinar a CNN.
3.  **Execução da Pipeline:**
    *   Execute `python pipeline_imagens.py`. O programa pedirá o caminho de uma imagem para analisar.
    *   Inicie a aplicação R Shiny executando o arquivo `dashboard.R` no RStudio.
4.  **Simulação IoT:**
    *   O código `firmware_esp32.ino` pode ser colado no simulador Wokwi para demonstrar o alerta do sensor.
