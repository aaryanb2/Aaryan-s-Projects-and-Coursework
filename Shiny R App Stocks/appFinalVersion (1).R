#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

# Library Imports
library(quantmod)
library(shiny)
library(shinythemes)


computeWeightedParams = function(alpha, returns) {
  weights = numeric(length(returns))
  
  for (i in 1:length(weights)) {
    weights[i] = (1 + alpha)^i
  }
  
  diff = (returns - mean(returns))^2
  
  mu = sum(weights * returns) / sum(weights)
  sigma = sqrt((sum(weights) * sum(diff * weights)) / (sum(weights)^2 - sum(weights^2)))
  
  return (c(mu, sigma))
}

# Main Calculation Function
runMCSims = function(num_sim, total_days, ticker, alpha) {
  stock_data = getSymbols(ticker, auto.assign = F)
  returns = dailyReturn(stock_data)
 
  # # code from groupe
  if (alpha > 0) {
    weighted_params = computeWeightedParams(alpha, returns)
    mu = weighted_params[1]
    sigma = weighted_params[2]
  } else {
    mu = mean(returns)
    sigma = sd(returns)
  }
  
  sim_mat = matrix(0, nrow = num_sim, ncol = total_days + 1)
  sim_mat[, 1] = tail(Cl(stock_data), 1)[[1]] # All sims start off with most recent closing price
  
  drift = (mu - sigma^2 / 2)

  for (k in 1:num_sim) {
    for (i in 1:total_days) {
      shock = sigma * rnorm(1)
      
      # MCMC process 
      sim_mat[k, i + 1] = sim_mat[k, i] * exp(drift + shock)
    }
  } 
  
  return (sim_mat)
}



ticker_list = stockSymbols()$Symbol

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Load in shiny theme
   theme = shinytheme("superhero"),
   
   # Application title
   titlePanel(h1("Monte Carlo Stock Price Simulator", align = "center")),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      
     sidebarPanel(
         # Select stock ticker 
         selectInput(inputId = "ticker",
                     label = "Select a stock",
                     choices = ticker_list),
         
         # Select number of days to simulate prices for 
         numericInput(inputId = 'total_days',
                      label = 'Choose number of days to simulate prices for (5-759)',
                      min = 5,
                      max = 759,
                      value = 253),
         
         # Select number of simulations to run
         numericInput(inputId = 'num_sim',
                     label = 'Choose number of Monte Carlo simulations to run (1-1000)',
                     min = 1,
                     max = 1000,
                     value = 100),
         
         # Select confidence level
         sliderInput(inputId = "confLevel", 
                     label = 'Select confidence level (%)',
                     min = 80,
                     max = 99, 
                     value = 90),
         
         sliderInput(
            inputId = "alpha", 
            label = 'Select weight',
            min = 0,
            max = .01, 
            value = 0 
         ),
         
         # Select mean trimming
         sliderInput(inputId = "kTrim", 
                     label = 'Select trim for mean calculation',
                     min = 0,
                     max = 30, 
                     value = 0
         ),
      
        h3("Confidence Interval of Final Price:", align = "center") ,  
        h2(textOutput("confIntvl"), align = "center")
      ),

      
      # Show a plot of the generated distribution
      mainPanel(
            plotOutput("simPlot"),
            plotOutput('histPrices'),
            plotOutput("rmsePlt")
      )
      
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   sim_results = reactive({
     sim_mat = runMCSims(input$num_sim, input$total_days, input$ticker, input$alpha)
     return (sim_mat)
   })
  
   output$simPlot <- renderPlot({
      return (matplot(t(sim_results()), type = 'l', ylab = "Price ($)", xlab = "Number of Days Passed"))
   })
   
   output$confIntvl = renderText({
     final_prices = sim_results()[, input$total_days + 1]
     
     k = input$kTrim / length(final_prices)
     x_bar = mean(log(final_prices), trim = k)
     std_err = sd(log(final_prices))
     z = -qnorm((1 - (input$confLevel/100)) / 2)
     
     conf_interval = c(x_bar - z * std_err, x_bar + z * std_err)
     conf_interval = exp(conf_interval)
     conf_interval = round(conf_interval, 2)
     
     return (paste0("[",conf_interval[1],
                    ", " , conf_interval[2], "]"))
   })
   
   output$rmsePlt = renderPlot({
      
      final_prices = sim_results()[, input$total_days + 1]
      rmse = numeric(30)
      for(i in 1:30){
         x = sort(final_prices)
         max = length(final_prices)
         x_t = x[(i+1):(max-i)]
         x_bar = mean(x_t)
         rmse[i] = sqrt(mean((x_bar - x)^2))
      }
      
      return(plot(1:30, rmse
                  , main = "RMSE of Mean Estimation by Trim"
                  , xlab = "Trim"
                  , ylab = "RMSE"
                  , type = "o"))
      
   })
   
   output$histPrices = renderPlot({
     final_prices = sim_results()[, input$total_days + 1]
     
     upper = quantile(final_prices)[4]
     lower = quantile(final_prices)[2]
     IQR = upper - lower
     
     # Eliminate outliers 
     final_prices = final_prices[final_prices > lower - 1.5 * IQR & final_prices < upper + 1.5 * IQR] 
     
     return (hist(final_prices, main = "Histogram of Final Prices", xlab = "Final Closing Price ($)"))  
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

