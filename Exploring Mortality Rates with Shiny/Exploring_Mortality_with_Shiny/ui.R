#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(tidyverse)
library(plotly)

cdc <- readr::read_csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')


# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
    # Application title
    titlePanel("US Mortality Analysis"),

    h3("Introduction:"),
    p("This dynamic", code("R Shiny"), "app allows the user to interactively explore US mortality data from 1999 through 2010. The plots in this app are built with", code("Plotly"), " which allows for further interaction and drill down capabilities.This data was collected and distributed by the CDC. You can read more about the dataset", a('here.', href = 'https://wonder.cdc.gov/ucd-icd10.html')),
  #  br(),
    h4("Key Metric:"),
    p(em("Crude Death Rate:"), "Crude rates are expressed as the number of deaths reported each calendar year per 100,000 persons.", 
       br(),br(), strong("Crude Death Rate = (Count of Deaths / Population) * 100,000")),
    
    br(),



    tabsetPanel(
        tabPanel("State Comparison",

        sidebarLayout(
            sidebarPanel(
              h3("Comparing Crude Mortality Rates Across States"),
              br(),
              p("This tab allows you to compare crude mortality rates from particular causes across different states. The selectors below allow you to select a year to analyze as well as a cause of death."),
              br(),
     
                sliderInput("year", "Select Year:", min = min(cdc$Year), max = max(cdc$Year), value = 2010),
                selectInput("cause", "Cause of Death:", selected = "Diseases of the digestive system", choices = unique(cdc$ICD.Chapter))
            ),
    
            # Show a plot of the generated distribution
            mainPanel(
                htmlOutput('state_hist_title'),
                plotly::plotlyOutput("state")
            )
        )
        ),
  tabPanel("State vs National Rate",
       
           sidebarLayout(
               sidebarPanel(
                 h3("Comparing State Crude Mortality to the National Rate"),
                 br(),
                 p("This tab allows you to compare a state's mortality rate against the national average (weighted by the national population). The selectors below allow you to select a state to compare as well as a cause of death."),
                 br(),
                  selectInput("state", "State:", selected = "AZ", choices = unique(cdc$State)),
                  selectInput("cause2", "Cause of Death:", selected = "Diseases of the digestive system", choices = unique(cdc$ICD.Chapter))
                   
               ),
               
               # Show a plot of the generated distribution
               mainPanel(
                   htmlOutput('state_title') ,
                   htmlOutput('state_subtitle'),
                   plotly::plotlyOutput("national")
               )
           )
           
  )
    )
))
