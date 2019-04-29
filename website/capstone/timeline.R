library(plotly)
library(dplyr)

findLink <- function(data) {
  timeDelta <- 1*60*60
  firstTime <- data[1, 'Timestamp']
  data <- filter(data, Timestamp >= firstTime & Timestamp <= firstTime + timeDelta)
  return(data)
  
}
CreateTimeline <- function(data) {
  data <- findLink(data)
  timeline <- plot_ly(data, x = data$Timestamp, y = data$Source,
                      type = 'scatter',
                      mode = 'markers',
                      color = ~data$Domain,
                      marker = list(size = 15),
                      text = ~sprintf("<br /> Site: %s <br /> Category: %s <br /> Protocol: %s <br /> Transition Type: %s <br />", data$Domain, data$Category, data$Protocol, data$Transition_Type))
  timeline <- layout(timeline, yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
  return(timeline)

}

#timeline <- plot_ly(data, type = 'scatter') %>%
#  add_trace(x = data$Timestamp, y = 1, type='scatter', opacity = 0.5, mode = 'markers',
#            marker = list(width = 10),
#            text = ~sprintf("<br /> Site: %s <br /> Category: %s <br /> Protocol: %s <br /> Transition Type: %s <br />", data$Domain, data$Category, data$Protocol, data$Transition_Type)) %>%
#  layout(yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))


#for(row in 1:nrow(data))
#{
#  timeline <- add_trace(timeline, x = ~data[row, 'Timestamp'], y = 1, type='scatter', opacity = 0.5, mode = 'markers', marker = list(width = 10), text = ~sprintf("<br /> Site: %s <br /> Category: %s <br /> Protocol: %s <br /> Transition Type: %s <br />", data[row, 'Domain'], data[row, 'Category'], data[row,'Protocol'], data[row, 'Transition_Type']))
#}