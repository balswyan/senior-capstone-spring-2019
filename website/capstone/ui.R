#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library("dplyr")
library("markdown")
library("ggplot2")
library("plotly")
library("tidyverse")
library(shinythemes)

# Define UI for application that draws a histogram
shinyUI(navbarPage('Capstone', theme = shinytheme("flatly"), fluid = TRUE,
                   tabPanel('Top Domains',
                            tags$h1("Top N Most Visited Domains"),
                            tags$hr(),
                            sliderInput("slider.count", label = h3("Domain count:"), 
                                        min = 1,
                                        max = 20,
                                        value = 10),
                            plotlyOutput("pie"),
                            
                            tags$h1("Top N Most Visited Domains by Date Range"),
                            tags $hr(),
                            dateRangeInput("date.range", "Date range:",
                                           start  = "2018-01-17",
                                           end    = "2018-01-18",
                                           min    = "2018-01-01",
                                           format = "mm/dd/yy",
                                           separator = " - "),
                            sliderInput("bar.slider.count", "Domain count:",
                                        min = 1,
                                        max = 25,
                                        value = 23),
                            plotlyOutput(("bar")),
                            
                            tags$h1("Domains Sorted by Category"),
                            tags$hr(),
                            plotlyOutput("plot")),
                   tabPanel('Browsing Timeline'),
                   tabPanel('User Polarization')
))
