#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

cdc <- readr::read_csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
    
#################State Comparison Tab#######################################################
    
    state_vis <- function(){
        cdc_summed <- cdc %>%
            filter(Year == input$year) %>%
            filter(ICD.Chapter == input$cause) 
        
        fig <- plot_ly(
            data = cdc_summed, 
            x = ~State, y = ~Crude.Rate, type = 'bar', name = 'Mortality Rates'
        )
        
        fig %>% layout(yaxis = list(title = "Crude Death Rate"))
    }

    output$state <- plotly::renderPlotly(state_vis())
    

    output$state_hist_title <- renderText({
        paste0("<H3> Crude Death Rate From ", str_to_title(input$cause), " In ", input$year, "</H3>")
    })
    

################## State vs National Rate ##############################################################
    
    comparison_vis <- function(){
        state <- cdc %>%
            filter(State == input$state) %>%
            filter(ICD.Chapter == input$cause2) %>%
            arrange(Year)
        
        national <- cdc %>%
            filter(ICD.Chapter == input$cause2) %>%
            group_by(ICD.Chapter,Year) %>%
            summarize(
                Deaths = sum(Deaths), 
                Population = sum(Population)
            ) %>%
            mutate(Crude.Rate = round((Deaths/Population)*100000,1)) %>%
            mutate(State = "National") %>%
            relocate(State, .before = Year) %>%
            arrange(Year)
        
        full <- rbind(state, national)
        
        fig1 <- plot_ly(full, x = ~Year, y = ~Crude.Rate, type = 'scatter', mode = 'lines+markers', color = ~State) 
        
        fig1 %>% layout(yaxis = list(title = "Crude Death Rate"))
    }
    
    output$state_subtitle <- renderText({
        paste0("<H5> Crude Death Rate from ", str_to_title(input$cause2), "  </H5>")
    })
    
    output$state_title <- renderText({
        paste0("<H3> ",input$state, " Mortality Rate vs National Average </H3>")
    })
    

    output$national <- plotly::renderPlotly(comparison_vis())

})
