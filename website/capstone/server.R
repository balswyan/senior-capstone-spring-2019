#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library("shiny")
library("dplyr")
library("plotly")

source("topsites.R")

browsing.data <- read.csv('data.csv')
domain.cat <- read.csv('domainCat.csv')

browsing.data$Date <- as.Date(browsing.data$Date, "%Y-%m-%d")

data <- left_join(browsing.data, domain.cat)

shinyServer(function(input, output) {
  
  output$pie <- renderPlotly({
    count <- input$slider.count
    pie.data <- group_by(data, Domain) %>%
      filter(Domain != 'docs.google.com') %>%
      summarise(Count = n()) %>%
      arrange(Count) %>%
      top_n(count)
    pie <- CreatePieChart(pie.data)
    })
  
  output$bar <- renderPlotly({
    minDate <- format(input$date.range[1])
    maxDate <- format(input$date.range[2])
    count <- input$bar.slider.count
    bar.data <- filter(data, Date >= minDate, Date <= maxDate, Domain != 'docs.google.com') %>%
      group_by(Domain) %>%
      summarise(Count = n()) %>%
      arrange(Count) %>%
      top_n(count)
    bar <- CreateBarChart(bar.data)
  })
    
  output$plot <- renderPlotly({
    plot.data <- group_by(data, Category) %>%
      filter(Category != 'google') %>%
      summarise(DCount = n())
    
    plot <- CreatePlot(plot.data)
    })

})
