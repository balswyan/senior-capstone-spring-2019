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
library(jsonlite)

source("topsites.R")
source("timeline.R")
source("comparison.R")

browsing.data <- read.csv('data.csv')
domain.cat <- read.csv('domainCat.csv')
allsides.domains <- read.csv('allside_domains.csv')
allsides.json <- fromJSON('allsides_scores.json')

browsing.data$Date <- as.Date(browsing.data$Date, "%Y-%m-%d")
browsing.data$Timestamp <- as.POSIXct(browsing.data$Timestamp, origin='1970-01-01')
domain.cat$Category <- as.character(domain.cat$Category)


data <- left_join(browsing.data, domain.cat)
categories <- c("All", na.exclude(unique(data$Category)))

allsides.combined <- left_join(allsides.domains, allsides.json) %>% filter(Domain != "")
allsides.combined$Domain <- gsub("\\/.*","", allsides.combined$Domain)
allsides.data <- left_join(data, allsides.combined) %>% filter(!is.na(news_source))

left <- nrow(filter(allsides.data, allsides_rating == 71))
lean_left <- nrow(filter(allsides.data, allsides_rating == 72))
center <- nrow(filter(allsides.data, allsides_rating == 73))
lean_right <- nrow(filter(allsides.data, allsides_rating == 74))
right <- nrow(filter(allsides.data, allsides_rating == 75))
unranked <- nrow(filter(allsides.data, allsides_rating == 2690))

shinyServer(function(input, output, session) {
  
  output$pie <- renderPlotly({
    updateSelectInput(session, "pie.category", "Category:", categories, selected = input$pie.category)
    count <- input$slider.count
    if(input$pie.category == "All")
    {
      pie.data <- group_by(data, Domain) %>%
        filter(Domain != 'docs.google.com') %>%
        summarise(Count = n()) %>%
        arrange(Count) %>%
        top_n(count)
    }
    else
    {
      pie.data <- group_by(data, Domain) %>%
        filter(Domain != 'docs.google.com', Category == input$pie.category) %>%
        summarise(Count = n()) %>%
        arrange(Count) %>%
        top_n(count)
    }
    pie <- CreatePieChart(pie.data)
    })
  
  output$bar <- renderPlotly({
    updateSelectInput(session, "bar.category", "Category:", categories, selected = input$bar.category)
    minDate <- format(input$date.range[1])
    maxDate <- format(input$date.range[2])
    count <- input$bar.slider.count
    if(input$bar.category == "All")
    {
      bar.data <- filter(data, Date >= minDate, Date <= maxDate) %>%
        group_by(Domain) %>%
        summarise(Count = n()) %>%
        arrange(Count) %>%
        top_n(count)
    }
    else
    {
      bar.data <- filter(data, Date >= minDate, Date <= maxDate, Category == input$bar.category) %>%
        group_by(Domain) %>%
        summarise(Count = n()) %>%
        arrange(Count) %>%
        top_n(count)
    }
    bar <- CreateBarChart(bar.data)
  })
    
  output$plot <- renderPlotly({
    plot.data <- group_by(data, Category) %>%
      filter(Category != 'google') %>%
      summarise(DCount = n())
    
    plot <- CreatePlot(plot.data)
    })
  
  output$timeline <- renderPlotly({
    timeline.data <- filter(data, Domain != 'mail.google.com') %>%
      arrange(Source, Timestamp) %>%
      slice(sample(1:n()-50,1):n())
    #timeline.data$Timestamp <- as.POSIXct(round(timeline.data$Timestamp, "mins"), origin='1970-01-01')
    #timeline.data <- distinct(timeline.data, Timestamp, .keep_all = TRUE)
    timeline <- CreateTimeline(timeline.data)

  })
  
  output$groupBar <- renderPlotly({
    groupBar.data <- group_by(data, Source)
    groupBar <- CreateTimeline(groupBar.data)
  })
  
  output$comparison <- renderPlotly(({
    domain1 <- input$comparison.domain1
    domain2 <- input$comparison.domain2
    updateSelectInput(session, "comparison.domain1", "Domain1:", sort(unique(data$Domain)), selected = input$comparison.domain1)
    updateSelectInput(session, "comparison.domain2", "Domain2:", sort(unique(data$Domain)), selected = input$comparison.domain2)
    comparison1 <- nrow(filter(data, Domain == domain1))
    comparison2 <- nrow(filter(data, Domain == domain2))
    comparison <- CreateComparison(comparison1, comparison2)
  }))
  
  output$allsides <- renderPlotly({
    allsides <- CreateAllsides(left, lean_left, center, lean_right, right, unranked)
  })

})
