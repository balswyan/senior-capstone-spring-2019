CreateComparison <- function(data1, data2) {
  timeline <- plot_ly(x = c("Domain1", "Domain2"), y = c(data1, data2),
                      type = 'bar')
  # timeline <- layout(timeline, yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
  return(timeline)
  
}

CreateAllsides <- function(data1, data2, data3, data4, data5, data6) {
  table <- data.frame(x = c("Left", "Lean Left", "Center", "Lean Right", "Right", "Unranked"),
                      y = c(data1, data2, data3, data4, data5, data6))
  col <- c("blue", "deepskyblue", "mediumpurple3", "indianred1", "red", "gray60")
  
  table$x <- factor(table$x, levels = c(as.character(table$x)))
  timeline <- plot_ly(x = table$x, y = table$y, color = table$x, colors = col,
                      type = 'bar')
  # timeline <- layout(timeline, yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
  return(timeline)
  
}