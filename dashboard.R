# --- Dashboard Interativo de Monitoramento de Enchentes ---
# Versão Final e Corrigida

# Carrega todas as bibliotecas necessárias no início
library(shiny)
library(bslib)
library(ggplot2)
library(dplyr)
library(DT)

# --- Interface do Usuário (UI) ---
ui <- fluidPage(
  # Tema visual moderno e escuro
  theme = bslib::bs_theme(bootswatch = "cyborg"),

  titlePanel("Dashboard de Análise de Risco de Enchentes"),

  sidebarLayout(
    sidebarPanel(
      width = 3,
      h4("Análise de Imagens de Satélite"),
      hr(),
      textOutput("total_imagens_analisadas"),
      textOutput("percentual_alagadas"),
      hr(),
      selectInput(
        "filtro_status",
        "Filtrar por Status:",
        choices = c("Todos", "Área Alagada", "Área Seca"),
        selected = "Todos"
      )
    ),

    mainPanel(
      width = 9,
      plotOutput("grafico_eventos_dia"),
      hr(),
      h4("Log Detalhado das Análises"),
      dataTableOutput("tabela_logs")
    )
  )
)

# --- Lógica do Servidor (Server) ---
server <- function(input, output, session) {

  # Função reativa para ler o CSV automaticamente a cada 3 segundos
  dados_log <- reactivePoll(3000, session,
    checkFunc = function() {
      if (file.exists("alert_log.csv")) {
        file.info("alert_log.csv")$mtime
      } else {
        ""
      }
    },
    valueFunc = function() {
      read.csv("alert_log.csv", fileEncoding = "UTF-8") %>%
        mutate(Data = as.Date(.data$Timestamp))
    }
  )

  # Filtra os dados conforme a seleção do usuário
  dados_filtrados <- reactive({
    df <- dados_log()
    if (input$filtro_status != "Todos") {
      df <- df %>% filter(.data$Status_Previsto == input$filtro_status)
    }
    df
  })

  # Renderiza os KPIs (Key Performance Indicators)
  output$total_imagens_analisadas <- renderText({
    paste("Total de Imagens Analisadas:", nrow(dados_log()))
  })

  output$percentual_alagadas <- renderText({
    total <- nrow(dados_log())
    if (total > 0) {
      alagadas <- sum(dados_log()$Status_Previsto == "Área Alagada")
      percent <- (alagadas / total) * 100
      paste("Percentual de Áreas Alagadas:", sprintf("%.1f%%", percent))
    } else {
      "Nenhuma imagem analisada ainda."
    }
  })

    # Renderiza o gráfico de barras
  output$grafico_eventos_dia <- renderPlot({
    
    # Prepara os dados para o gráfico
    contagem_dia <- dados_filtrados() %>%
      group_by(.data$Data, .data$Status_Previsto) %>%
      summarise(N = n(), .groups = "drop")

    # Define as cores e as categorias possíveis
    cores_status <- c("Área Alagada" = "#dc3545", "Área Seca" = "#28a745")

    # Cria o gráfico com ggplot2
    ggplot(contagem_dia, aes(x = Data, y = N, fill = Status_Previsto)) +
      geom_bar(stat = "identity", position = "stack") +
      # CORREÇÃO: Adicionamos o parâmetro 'limits' para que o ggplot sempre conheça
      # todas as categorias, mesmo que não estejam nos dados atuais.
      scale_fill_manual(
        values = cores_status,
        limits = names(cores_status) 
      ) +
      labs(
        title = "Contagem de Análises por Dia",
        x = "Data",
        y = "Número de Imagens"
      ) +
      theme_minimal(base_size = 14) +
      theme(legend.title = element_blank())
  })
}

# --- Roda a Aplicação Shiny ---
shinyApp(ui = ui, server = server)