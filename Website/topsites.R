library(plotly)
library(dplyr)

CreatePieChart <- function(data) {
  count <- count(data)
  pie <- plot_ly(data, labels = ~Domain, values = ~Count, type = 'pie') %>%
    layout(title = ~sprintf('Top %s Domains', count),
           xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
           yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
}

CreateBarChart <- function(data) {
  bar <- plot_ly(data, y = ~Domain, x = ~Count, type = 'bar',
                 marker = list(line = list(color = 'rgb(8,48,107)',
                                           width = 1.2)))
  return(bar)
}

CreatePlot <- function(data) {
  data$ntile <- ntile(data$DCount, 6)
  plott <- plot_ly(data, x=data$Category, y=data$DCount, type='scatter', mode='markers',
                   #Multiple by 5 to make bubbles larger
                   marker=list(size=data$ntile*5),
                   text = ~sprintf("<br /> Category: %s <br /> Count: %s <br />", data$Category, data$DCount)) %>% 
    layout(xaxis = list(title = 'Category', dtick=1), yaxis = list(title = 'Count'))
  return(plott)
}
