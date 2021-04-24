import streamlit as st
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import stats
import plotly.express as px

# --------------------------------------------- Functions Needed for Simulation ---------------------------------------------------------------------------# 

#egg_revenue funtion will be a function that returns the revenue from selling x dozen eggs at x price, laid by x chickens 
def egg_revenue(chickens, days, sale_price, cost_of_carton, yearly_low_end_egg_production, yearly_high_end_egg_production): 
    
    #chickens - number of chickens in the flock
    #days - number of days you want to simulate (i.e. 31 for month, 365 for year, etc.)
    #sale_price - the price at which you can sell 1 dozen eggs (will vary by location)
    #cost_of_carton - cost of indiviudal egg carton
    #yearly_low_end_egg_production - low end of how many eggs an average chicken lays a year
    #yearly_high_end_egg_production - high end of how many eggs an average chicken lays a year
    
    total_egg_count = []
    
    #total_egg_count will hold the count of eggs laid each day
    #We will take this count, sum it, and then multiply by the
    #price of the eggs to get revenue

    for day in range(days): 
        
    #for loop to loop through each of the days chosen in the input parameter
        
        egg = [0,1]  # egg is setting our outcomes, 0 for no egg, 1 for an egg
        eggs_today = [] # will hold the count of the eggs laid by each chicken in a day

        daily_egg_prob = np.random.uniform(low = yearly_low_end_egg_production, high = yearly_high_end_egg_production,
                                           size = chickens)
        
        #daily_egg_prob uses a uniform distribution to randomly select values between 
        #yearly_low_end_egg_production and yearly_high_end_egg_production, which is 
        #is the interval for how many eggs a chicken lays per year. The size parameter above will be set
        #to select a random sample for every chicken in the flock. Defaul is 235 and 275

        for i in daily_egg_prob: 
            
        #here we loop through the above samples for each chicken and use the sample to calculate
        #a probability that a chicken will lay an egg that day (i.e. p = 275/365)
            
            probabilities = [1-(i/365),(i/365)] #[0] is the outcome where an egg is NOT laid, [1] is an egg is laid
            
            outcome = np.random.choice(egg, size = 1, p= probabilities) 
            
            #based on the probabilities, picks an outcome
            #of an egg or no egg for a day
            
            eggs_today.append(outcome[0]) #adds the outcome for that chicken to the list. 
            
        total_egg_count.append(sum(eggs_today)) #adds the sum of the eggs for a day from each chicken in the flock 

    total_eggs = sum(total_egg_count) #sums all eggs for all days selected in the input parameter
    
    dozen_eggs = total_eggs / 12 #divide by 12 to get how many dozen eggs we can sell
    
    return math.floor(dozen_eggs) * (sale_price - cost_of_carton) 


#food_consumption function will calculate how much cost is incurred by feeding x amount of birds based on the cost of the feed and how many lbs were purchased
def food_consumption(chickens, days, bag_of_feed_cost, lbs_of_feed):
    
    #chickens - number of chickens in the flock
    #days - number of days you want to simulate (i.e. 31 for month, 365 for year, etc.)
    #bag_of_feed_cost - price of a single bag of feed
    #lbs_of_feed - lbs of feed that were purchased from a single bag
    
    food_consumption = np.random.uniform(low = .23, high = .27, size = days*chickens)
    
    # A laying hen will consume between 
    #.23 and .27 lbs of feed per day. This function pulls a sample between .23 and .27 for each chicken for every day 
    #of the simulation allowing us to calculate how many pounds of feed x amount of chickens ate over the selected
    #time period    
    
    bags_of_feed = math.ceil(sum(food_consumption)/lbs_of_feed) 
    
    #food consumed divided by the lbs of feed you purchase to 
    #calculate how many bags of feed were purchased
    
    return round(bags_of_feed * bag_of_feed_cost,2) #returns the cost as bags of feed consumed * cost of the bags


#bedding_cost function will calculate the cost incurred from having to change the nesting bedding. The function
#assumes the bedding needs to be changed every 27-31 days and the number of chickens you have affects how much bedding
#you need
def bedding_cost(chickens, days, bag_of_bedding_cost, cubic_feet_of_bedding, low_end_days_to_refresh, 
                 high_end_days_to_refresh):
    
    #chickens - number of chickens in the flock
    #days - number of days you want to simulate (i.e. 31 for month, 365 for year, etc.)
    #bag_of_bedding_cost - price of a single bag of bedding
    #cubic_feet_of_bedding - cubic feed of bedding that were purchased from a single bag of bedding
    #low_end_days_to_refresh - low end of days when bedding needs to be refreshed (i.e. - after 27 days)
    #high_end_days_to_refresh - high end of days when bedding needs to be refreshed (i.e. - after 35 days)
    
    days_to_refresh = math.ceil(np.random.uniform(low = low_end_days_to_refresh, 
                                                  high = high_end_days_to_refresh, size = 1))
        
    #randomly chooses a number between low_end_days_to_refresh 
    # and high_end_days_to_refresh days which is how often the bedding needs to be refreshed
    #default is 27 and 31, respectively
    
    times_to_refresh_bedding = math.ceil(days/days_to_refresh)
    
    #calculates how many times the bedding needed to be 
    #refreshed during the time period entered into for the simulation
        
    chickens_for_10_cubic_feet = math.ceil(np.random.uniform(low = 23, high = 26, size = 1)) 
    
    # selects a random number
    #between 23 and 26, which is the number of chickens that can be provided nesting with 10 cubic feet of bedding
   
    if chickens <= chickens_for_10_cubic_feet: 
        
    #if we less than or equal to the number of chickens randomly selected
    #from above, we won't need to buy an additional bag 
    
        feet_from_chickens = 0 #no additional bag needed
        
    else:
        feet_from_chickens = math.ceil(((10/chickens_for_10_cubic_feet) * chickens)/cubic_feet_of_bedding)
        
        #divide 10 by the number of chickens that 10 cubic feet will provide for to get a rate per bird
        #then multiply that rate by how many chickens are in our simulation
        #finally, divide that amount by how many cubic feet of bedding are in a single bag, to determine how 
        #many bags we need.
   
    return round(bag_of_bedding_cost * (times_to_refresh_bedding + feet_from_chickens),2) #returns cost of bedding


def chicken_simulation_function(low_end_chickens, high_end_chickens, by_how_many_chickens, days, 
                                sale_price, cost_of_carton, yearly_low_end_egg_production, yearly_high_end_egg_production,
                                bag_of_feed_cost, lbs_of_feed, bag_of_bedding_cost, cubic_feet_of_bedding, 
                                low_end_days_to_refresh, high_end_days_to_refresh, additional_cost,
                                simulations_per_chicken):
    
    #low_end_chickens - low end of the range of chickens you could maintain
    #high_end_chickens- high end of the range of chickens you could maintain
    #by_how_many_chickens - simulate increases of 1,2,3,4, etc. chickens at a time. If you want to run the 
        #simulation for every chicken in the range, subtract the high_end_chickens from the low_end_chickens and 
        #enter the number, otherwise, divide that number by the number you want to increase in each simulation. 
    #days - number of days you want to simulate (i.e. 31 for month, 365 for year, etc.)
    #sale_price - the price at which you can sell 1 dozen eggs (will vary by location)
    #cost_of_carton - cost of indiviudal egg carton
    #yearly_low_end_egg_production - low end of how many eggs an average chicken lays a year
    #yearly_high_end_egg_production - high end of how many eggs an average chicken lays a year
    #bag_of_feed_cost - price of a single bag of feed
    #lbs_of_feed - lbs of feed that were purchased from a single bag
    #bag_of_bedding_cost - price of a single bag of bedding
    #cubic_feet_of_bedding - cubic feed of bedding that were purchased from a single bag of bedding
    #low_end_days_to_refresh - low end of days when bedding needs to be refreshed (i.e. - after 27 days)
    #high_end_days_to_refresh - high end of days when bedding needs to be refreshed (i.e. - after 35 days)
    #additional_cost - you can enter a value here if you have incremental costs not included in the simulation
    #simulations_per_chicken - how many simulations per chicken should be run (i.e. 100 simulations)
    

    chickens_to_sweep = np.linspace(low_end_chickens,high_end_chickens, by_how_many_chickens)   
    #an array holding the values of the chicken range (i.e. 15-25 chickens)
    
    #lists to hold avg, min, max, and var of the gross profit, revenue, food cost, bedding cost and total cost of the 
    #simulations per chicken
    avg_gross_profit_amounts = []
    avg_revenue_amounts = []
    avg_food_cost_amounts = []
    avg_bed_cost_amounts = []
    avg_total_cost_amounts = []
    
    min_gross_profit_amounts = []
    min_revenue_amounts = []
    min_food_cost_amounts = []
    min_bed_cost_amounts = []
    min_total_cost_amounts = []
    
    max_gross_profit_amounts = []
    max_revenue_amounts = []
    max_food_cost_amounts = []
    max_bed_cost_amounts = []
    max_total_cost_amounts = []
    
    var_gross_profit_amounts = []
    var_revenue_amounts = []
    var_food_cost_amounts = []
    var_bed_cost_amounts = []
    var_total_cost_amounts = []
    
    #dictionaries that will hold the current value of chickens being simulated as the key and the raw values (list)
    #of the simulation  
    gp_dict = dict()
    rev_dict = dict()
    food_dict = dict()
    bed_dict = dict()
    tot_cost_dict = dict()
    
    #sweeps through range of chickens and stores each run of the simulation in its given list: gross profit, 
    #revenue, food cost, bed cost, and total cost
    for n_chickens in chickens_to_sweep:
        gross_profit_amounts = []
        revenue_amounts = []
        food_cost_amounts = []
        bed_cost_amounts = []
        total_cost_amounts = []

        #loops through the desired amount of simulations per chicken
        for i in range(0,simulations_per_chicken):

            chickens = int(n_chickens)
        

            #storing output of egg_revenue function
            revenue = egg_revenue(chickens, days, sale_price, cost_of_carton, yearly_low_end_egg_production,
                                  yearly_high_end_egg_production)
            
            #storing output of food_consumption function
            food_cost = food_consumption(chickens, days, bag_of_feed_cost, lbs_of_feed)
            
            #storing output of bedding_cost function
            bed_cost = bedding_cost(chickens, days, bag_of_bedding_cost, cubic_feet_of_bedding, low_end_days_to_refresh, 
                                    high_end_days_to_refresh)
            
            #calculating total cost
            total_cost = food_cost + bed_cost + additional_cost

            #calculating gross profit and appending to list
            gross_profit = revenue - food_cost - bed_cost - additional_cost
            gross_profit_amounts.append(gross_profit)
            
            #appending revenue, food cost, bed cost, and total cost to respective lists
            revenue_amounts.append(revenue)
            food_cost_amounts.append(food_cost)
            bed_cost_amounts.append(bed_cost)
            total_cost_amounts.append(total_cost)
        
        #dictionaries of values for each chicken
        gp_dict[n_chickens] = gross_profit_amounts
        rev_dict[n_chickens] = revenue_amounts
        food_dict[n_chickens] = food_cost_amounts
        bed_dict[n_chickens] = bed_cost_amounts
        tot_cost_dict[n_chickens] = total_cost_amounts
               
        #lists of the averages
        avg_gross_profit_amounts.append(np.average(gross_profit_amounts)) 
        avg_revenue_amounts.append(np.average(revenue_amounts))
        avg_food_cost_amounts.append(np.average(food_cost_amounts))
        avg_bed_cost_amounts.append(np.average(bed_cost_amounts))
        avg_total_cost_amounts.append(np.average(total_cost_amounts))
        
        #lists of the minimums
        min_gross_profit_amounts.append(min(gross_profit_amounts)) 
        min_revenue_amounts.append(min(revenue_amounts))
        min_food_cost_amounts.append(min(food_cost_amounts))
        min_bed_cost_amounts.append(min(bed_cost_amounts))
        min_total_cost_amounts.append(min(total_cost_amounts))
        
        #lists of the maximums
        max_gross_profit_amounts.append(max(gross_profit_amounts)) 
        max_revenue_amounts.append(max(revenue_amounts))
        max_food_cost_amounts.append(max(food_cost_amounts))
        max_bed_cost_amounts.append(max(bed_cost_amounts))
        max_total_cost_amounts.append(max(total_cost_amounts))
        
        #lists of the variances
        var_gross_profit_amounts.append(np.var(gross_profit_amounts)) 
        var_revenue_amounts.append(np.var(revenue_amounts))
        var_food_cost_amounts.append(np.var(food_cost_amounts))
        var_bed_cost_amounts.append(np.var(bed_cost_amounts))
        var_total_cost_amounts.append(np.var(total_cost_amounts))
        
    #list of dictionaries    
    dictionary_list = [gp_dict, rev_dict, food_dict, bed_dict, tot_cost_dict]
    
    #the below data frame aggregates all of the lists collected above to return in a simple format that can be analyzed.  
    chicken_df = pd.DataFrame(list(zip(avg_gross_profit_amounts, avg_revenue_amounts, avg_food_cost_amounts,
                                       avg_bed_cost_amounts, avg_total_cost_amounts, min_gross_profit_amounts, 
                                       min_revenue_amounts,min_food_cost_amounts,min_bed_cost_amounts, 
                                       min_total_cost_amounts, max_gross_profit_amounts, max_revenue_amounts, 
                                       max_food_cost_amounts, max_bed_cost_amounts, max_total_cost_amounts, 
                                       var_gross_profit_amounts, var_revenue_amounts, var_food_cost_amounts, 
                                       var_bed_cost_amounts, var_total_cost_amounts)),
                              columns = ['avg_gross_profit_amounts', 'avg_revenue_amounts', 'avg_food_cost_amounts', 
                                         'avg_bed_cost_amounts', 'avg_total_cost_amounts', 'min_gross_profit_amounts', 
                                       'min_revenue_amounts','min_food_cost_amounts','min_bed_cost_amounts', 
                                       'min_total_cost_amounts', 'max_gross_profit_amounts', 'max_revenue_amounts', 
                                       'max_food_cost_amounts', 'max_bed_cost_amounts','max_total_cost_amounts', 
                                         'var_gross_profit_amounts', 'var_revenue_amounts', 'var_food_cost_amounts',
                                         'var_bed_cost_amounts', 'var_total_cost_amounts'])
    chicken_df.index = chicken_df.index + low_end_chickens
    chicken_df.index.name = '# of Chickens'
    
    #returns both the data frame containing all the summarized data as well as a dictionary with all of the detailed data
    #from each simulation run
    return chicken_df, dictionary_list

# ---------------------------------------- Building the Simulation App ---------------------------------------------------------------------------------------#

#Setting page configuration to wide
st. set_page_config(layout="wide", page_title = "Chicken Simulation")
st.markdown("# How Many Chickens Should I Have? :chicken:")

#Creating a 3 column layout, will only use 1 and 3 and 2 will be for spacing between columns
col1, col2, col3 = st.beta_columns([1.25,.15,2])

#---------------------------------- Main Text Section -------------------------------------------------------------#
with col1: 
    st.markdown("### **Introduction** :wave:")
    st.write("Over the past decade, the desire for organic food has grown exponentially. As demand increases, many people wonder what it takes to produce and sell their own organic food. Raising laying hens to sell organic eggs is one of the easiest ways to break into this area. Chickens are low maintenance and fairly cheap to care for as well. Before jumping in it's worth looking to see if you would be able to break even or turn a profit. There are quite a few variables to account for, and having the wrong quantity of laying hens can negatively affect your profit.")
    st.markdown("### **Why Simulation** :question:")
    st.markdown("When it comes to chickens, nothing is certain. For example, organic chickens generally don't lay an egg every day, they don't eat the same amount of food every day, and will need to have their bedding changed when it is soiled, which may not happen at the same interval every time. When running a side business with lower margins, simulation works better than *manual calculations*, because we can use probability distributions to model each of these variables and run the simulation many times to analyze how much variance there is with the profits (by looking at average, maximum, and minimum values). Then, based on our risk profile, we can make the most informed decision.")
    st.markdown("### **What are the Variables?** :gear:")
    st.markdown("For the *casual hen owner (1-50 chickens)* looking to sell eggs, there are really three areas of interest that need to be accounted for:")
    
    st.markdown("* **Revenue** - How much money do you make from the sale of dozens of eggs?\n* **Feed Cost** - The cost of feeding your chickens\n* **Bedding Cost** - The cost of buying and replacing bedding that periodically gets soiled")
    st.markdown("### **How It Works** :hammer:")
    st.markdown("We model the variables above individually using probability distributions based on the input from the user in the **Simulation Parameter** pane :arrow_left:. Below is a general outline of the questions that need to be answered for each variable: ")
    st.markdown("**General** :rooster:")
    st.markdown("* How many chickens are in the flock? (simulate a range to find the optimal value) \n* How many days we want to simulate (i.e. 31 for a month, 60 for two months, 90 for a quarter)\n")
    st.markdown("**Revenue** :moneybag:")
    st.markdown("* How much can we sell a dozen organic eggs for?\n* How much does each individual egg carton cost (i.e. $0.23/carton)\n* What is the low and high end of egg production per year for the type of hens you have? Most birds lay between 235 to 275 eggs a year")
    st.markdown("**Feed Cost** :stew:")
    st.markdown("* The cost of a single bag of feed\n* How many pounds of feed are in a single bag\n* How much feed does a single chicken consume on a given day?")
    st.markdown("**Bedding Cost** :bed:")
    st.markdown("* The cost of a single bag of bedding\n* The cubic feet of bedding in a single bag\n* How long does the bedding last before it is soiled?")
    st.markdown("### **Putting It All Together** :building_construction:")
    st.markdown("Finally, we can tie these models together and visualize :bar_chart: :arrow_right: the minimums, averages, and maximums of gross profit, revenue, and costs in order to make the best decision based on how averse to risk we are.")

# ------------------------------------------------- Sidebar Section -------------------------------------------------------------------------------------------#
st.sidebar.markdown("### Instructions:")
st.sidebar.write("Adjust the below inputs to see how different scenarios affect gross profit. Hover over the question mark *tooltips* for additional details about each input.")
#pulling chicken image
st.sidebar.image('https://media.istockphoto.com/photos/portrait-of-a-funny-chicken-closeup-isolated-on-white-background-picture-id1132026121?k=6&m=1132026121&s=612x612&w=0&h=B1TjA88Qd5CtpC2NczetV86LR2qYImqMOb9C9OE34P0=')
st.sidebar.markdown("### Simulation Parameters:")
#-------------------------------------------------Sliders and Input Values in Sidebar Section ----------------------------#
#Building Range of Chickens to Iterate Over Slider which allows for two values 
values = st.sidebar.slider("Range of Chickens to Iterate Over:", 1,50,(5,25), help="Input the range of chickens you are willing to have. The simulation will help you determine what the optimal value in this range is.")
#only allows for one value -- capping at 100 so user experience isn't poor
simulation_runs = st.sidebar.slider("Simulations per Chicken:", 1,100, value = 10, help="The benefit of running a simulation is you can run it many times to see what variability there is. We can run multiple simulations for each chicken in the range you've chosen. This will allow us to see many conceivable scenarios and then to choose the option that brings the higest value with the lowest risk. Increasing scenarios will increase the run time of the calculation.") 
# simulating anywhere from a month to full quarter -- longer affects user experience
days_to_simulate = st.sidebar.slider("Days to Run the Simulation Over:", 30,90, help = "How many days should we simulate? Do you want to see what gross profit looks like each month? Each quarter? Enter the value in days (i.e. 1 month = 31 days, 1 quarter = 90 days). Increasing this value will increase the run time of the calculation.") 
#number input for price you will sell a dozen eggs for
dozen_price = st.sidebar.number_input("Sale Price of a Dozen Eggs:", value = 4.25, help = "How much do you plan to sell a dozen eggs for?")
#the actual cost of the carton you will be selling the eggs in
carton_cost = st.sidebar.number_input("Cost of Carton:", value = 0.29, help = "You are packaging the dozen eggs you are selling in a carton. How much does each individual carton cost you?")
#chickens have a range of eggs they'll produce based on breed, this input allows you to play with that
egg_production = st.sidebar.slider("Range of Yearly Egg Production:", 150,340,(235,275), help = "What is the low end and high end of egg production per year for the type of hens you have? Most birds lay between 235 to 275 eggs a year. You can google the type of hens you plan to have and find a reasonable estimate.")
#input allowing you to specify your feed cost
feed_cost = st.sidebar.number_input("Cost of Feed:", value = 23.99, help = "How much does a single bag of feed cost you?")
#input allowing you to specify you much feed you bought in pounds
pounds_of_feed = st.sidebar.number_input("Pounds of Feed:", value = 35, help = "How many pounds of feed are in the bag you purchased?")
#number input allowing you to change the cost of a bag of bedding
bedding_bag_cost = st.sidebar.number_input("Cost of Bedding:", value = 8.79, help = "How much does a bag of bedding cost?")
#number input to specify how much bedding you bought in cubic feet
cubic_feet_bedding = st.sidebar.number_input("Cubic Feet of Bedding:", value = 10, help = "How many cubic feet are in the bag of bedding you purchased?")
#how often in days you will fresh the bedding
days_to_refresh = st.sidebar.slider("Range of Days to Refresh Bedding:", 5,40,(28,32), help = "How often will you need to change the bedding?")
#additional costs over the time period you've selected
additional_costs = st.sidebar.number_input("Additional Costs:", value = 0, help = "Any additional costs can be entered here. For example if you are providing vitamins, meal worms, etc.")

st.sidebar.markdown(' ')
st.sidebar.markdown(' ')
st.sidebar.markdown(' ')
st.sidebar.markdown("*This app was built by Christian Thieme using Python and Streamlit*")
#----------------------------------------------------Running the Simulation Based on User Input or Default Values ----------------------------------------#

#Running chicken_simulation_function based on input values from the user (or defaul values)

#I use the values from the sliders and number inputs to feed my function that runs all of the simulations 
#each time an input is changed, the function reruns
df, dict_list = chicken_simulation_function(low_end_chickens = values[0], 
                                            high_end_chickens = values[1],
                                            by_how_many_chickens = (values[1]- values[0])+1,
                                            days = days_to_simulate, 
                                            sale_price = dozen_price,
                                            cost_of_carton = carton_cost, 
                                            yearly_low_end_egg_production = egg_production[0],
                                            yearly_high_end_egg_production = egg_production[1],
                                            bag_of_feed_cost = feed_cost, 
                                            lbs_of_feed = pounds_of_feed, 
                                            bag_of_bedding_cost = bedding_bag_cost, 
                                            cubic_feet_of_bedding = cubic_feet_bedding, 
                                            low_end_days_to_refresh = days_to_refresh[0],
                                            high_end_days_to_refresh = days_to_refresh[1], 
                                            additional_cost = additional_costs, 
                                            simulations_per_chicken = simulation_runs)

#Building columns needed for optimal chicken calc and break even calc
df['answer'] = df['min_gross_profit_amounts'] + df['avg_gross_profit_amounts'] + df['max_gross_profit_amounts']
df['break_even'] = df["min_revenue_amounts"] - df["max_total_cost_amounts"] 

#------------------------------------ Visualization Pane on the far right which has values from Simulation Run ------------------------------------------#
with col3: 
    st.markdown("### **The Answer** :hatching_chick:")
    #finding the optimal amount of chickens
    optimal_chickens = df['answer'].idxmax() 

    #Getting the range of Gross Profit Values for the optimal chicken value
    min_gross_profit = df.iloc[optimal_chickens-values[0]]['min_gross_profit_amounts']
    max_gross_profit = df.iloc[optimal_chickens-values[0]]['max_gross_profit_amounts']

    
    st.markdown("Based on your inputs, you should have **{}** chickens. This number has the highest probability of maximizing gross profit in all scenarios. You can expect to earn between **${}** and **${}** of gross profit every **{}** days.".format(optimal_chickens,round(min_gross_profit,2),round(max_gross_profit,2), days_to_simulate ))
   
    #Gross Profit Chart
    st.markdown("### **Gross Profit Analysis**")
    fig = px.line(df, x = df.index, y = [df['max_gross_profit_amounts'], df['avg_gross_profit_amounts'], df['min_gross_profit_amounts']], labels = dict(value = '$ Gross Profit', variable = ''))
    fig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig, use_container_width= True)
    st.write("For further analysis, we can break down the gross profit calculation and look at revenue and total costs. Total costs can be broken down further into food costs and bedding costs.")
    
    #Revenue Chart
    st.markdown("### **Revenue Analysis**")
    fig1 = px.line(df, x = df.index, y = [df['max_revenue_amounts'], df['avg_revenue_amounts'], df['min_revenue_amounts']], labels = dict(value = '$ Revenue', variable = ''))
    fig1.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig1, use_container_width= True)

    #Total Cost Chart
    st.markdown("### **Total Cost Analysis**")
    fig2 = px.line(df, x = df.index, y = [df['max_total_cost_amounts'], df['avg_total_cost_amounts'], df['min_total_cost_amounts']], labels = dict(value = '$ Total Costs', variable = ''))
    fig2.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig2, use_container_width= True)
  
    #Food Cost Chart
    st.markdown("### **Food Cost Analysis**")
    fig3 = px.line(df, x = df.index, y = [df['max_food_cost_amounts'], df['avg_food_cost_amounts'], df['min_food_cost_amounts']], labels = dict(value = '$ Food Costs', variable = ''))
    fig3.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig3, use_container_width= True)

    #Bedding Cost Chart
    st.markdown("### **Bedding Cost Analysis**")
    fig4 = px.line(df, x = df.index, y = [df['max_bed_cost_amounts'], df['avg_bed_cost_amounts'], df['min_bed_cost_amounts']], labels = dict(value = '$ Bedding Costs', variable = ''))
    fig4.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig4, use_container_width= True)

    #Break Even Chart
    st.markdown("### **Conservative Break Even Point(s)**")
    fig5 = px.line(df, x = df.index, y = [df['min_revenue_amounts'], df['max_total_cost_amounts']], labels = dict(value = '$', variable = ''))
    fig5.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})
    st.plotly_chart(fig5, use_container_width= True)

    #Building table for break even points
    bep = df[df['break_even']>=0].reset_index()
    bep = bep[['# of Chickens','break_even']]
   # bep.reset_index(inplace = True)
    st.markdown("If you wanted to have the least amount of chickens possible and still break even, you should have **{}** chickens. The below table shows additional break even points: ".format(bep['# of Chickens'].head(1)[0]))
    st.write(bep)
