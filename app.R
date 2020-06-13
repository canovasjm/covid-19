# required libraries ------------------------------------------------------
library(tidyverse)
library(shiny)
library(plotly)

# read data ---------------------------------------------------------------
df <- read_csv(file = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=722f3143b586a83f")

# transform to tidy data
df <- df %>% 
  filter(country_region_code == "AR") %>% 
  select(-c(country_region_code, sub_region_2, iso_3166_2_code, census_fips_code)) %>% 
  pivot_longer(-c(country_region, sub_region_1, date), names_to = "type", values_to = "values") %>% 
  mutate(sub_region_1 = sub("Buenos Aires$", "CABA", sub_region_1)) %>% 
  mutate(sub_region_1 = sub("* Province", "", sub_region_1)) %>%
  mutate(sub_region_1 = replace_na(sub_region_1, "Todas las provincias")) %>% 
  mutate(type = sub("_percent_change_from_baseline$", "", type))

# set system locale to spanish in order to show days ----------------------
# Sys.getlocale("LC_TIME")
Sys.setlocale("LC_TIME", "es_AR.UTF-8")

# shiny app ---------------------------------------------------------------
# create vector of choices for provinces
province_choices <- c("Todas las provincias", 
                      sort(unique(df$sub_region_1)))[-25]

ui <- fluidPage(
  headerPanel("COVID-19 reporte de movilidad de Google para Argentina"),
  fluidRow(
    column(3,
           selectInput("provinceInput", h4("Seleccione una provincia:"), 
                       choices = province_choices,
                       selected = "Todas las provincias"),
           dateRangeInput("dateInput", h4("Seleccione una fecha:"),
                          start = min(df$date), 
                          end = max(df$date),
                          min = min(df$date), 
                          max = max(df$date), 
                          startview = "week",
                          language = "es",
                          separator = " a "),
           actionButton(inputId = "resetInput", 
                        label = "Reestablecer fechas", 
                        icon = icon("undo")),
           br(),
           br(),
           h4("Sobre los datos:"),
           HTML("<p> Los datos provienen de Google (ver fuente abajo) y
           muestran cómo las visitas y su duración varían en diferentes lugares en comparación
           con una línea base. <p>"),
           HTML("<p> Los cambios para cada día se comparan con una línea base para el mismo día de la semana:
           el valor base es la mediana, para el correspondiente día de la semana, durante el periodo de 5 
           semanas del 3 de enero al 6 de febrero de 2020. <p>"),
           br(),
           h4("Fuente:"),
           em("Google LLC 'Google COVID-19 Community Mobility Reports'"),
           HTML("<a href=https://www.google.com/covid19/mobility/> https://www.google.com/covid19/mobility/ </a>"),
           paste("Consultado:", as.character(Sys.Date()))
           ),

  column(9,
    plotlyOutput("provincePlot"),
    br(),
    h4("Detalles de cada serie:"),
    HTML("<p> <b> grocery_and_pharmacy</b>: lugares como mercados, almacenes, ferias, maxi kioscos y farmacias. <p>"),
    HTML("<p> <b> parks</b>: lugares como parques, parques nacionales, playas, embarcaderos, plazas y jardines públicos. <p>"),
    HTML("<p> <b> residential</b>: lugares residenciales. <p>"),
    HTML("<p> <b> retail_and_recreation</b>: lugares como restaurants, cafes, shopping, parques temáticos, museos, bibliotecas y cines. <p>"),
    HTML("<p> <b> transit_stations</b>: sitios de transporte público como estaciones de subterraneo, colectivos y trenes. <p>"),
    HTML("<p> <b> workplaces</b>: lugares de trabajo. <p>")
    
    )
  )
)


server <- function(input, output, session) {
  
  output$provincePlot <- renderPlotly({
    
    # filter data based on date
    df_filtered <- subset(df, 
                          date >= input$dateInput[1] & 
                          date <= input$dateInput[2] & 
                          sub_region_1 == input$provinceInput)

    # make ggplot 
    p <- ggplot(df_filtered, aes(x = date, y = values, color = type)) +
      geom_line() +
      scale_x_date(date_breaks = "4 days", date_labels = "%a, %d-%b") +
      labs(
        title = paste("Mostrando datos de", input$provinceInput),
        # subtitle = paste("Selected date range from ", input$dateInput[[1]], "to", input$dateInput[[2]]),
        # caption = "Google LLC 'Google COVID-19 Community Mobility Reports' \n
        #         https://www.google.com/covid19/mobility/ Accessed: <Date>",
        color = "Tipo",
        y = "% de cambio respecto a la linea base",
        x = "Fecha"
      ) +
      theme_bw() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position = "bottom")
    
    # make that ggplot interactive with plotly
    ggplotly(p, tooltip = c("all"))
  })
  
  # reset button
  observeEvent(
    eventExpr = input$resetInput,
    handlerExpr = updateDateRangeInput(session,
                                       inputId = "dateInput",
                                       start = min(df$date),
                                       end = max(df$date),
                                       min = min(df$date),
                                       max = max(df$date))
  )
}

shinyApp(ui, server)


