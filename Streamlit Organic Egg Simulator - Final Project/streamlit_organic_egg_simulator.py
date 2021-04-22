import streamlit as st
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import stats

# --------------------------------------------- Functions Needed for Simulation ---------------------------------------------------------------------------# 

#egg_revenue funtion will be a function that returns the revenue from selling x dozen eggs at x price, laid by x chickens 
@st.cache
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
@st.cache
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
@st.cache
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


def chicken_simulation_function(low_end_chickens, high_end_chickens, days, 
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
    

    chickens_to_sweep = np.linspace(low_end_chickens,high_end_chickens)   
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

st.title("How Many Chickens Should I Have?")
st.subheader("Organic Egg Sales Simulation to Maximize Gross Profit")

st.sidebar.header("Simulation Parameters:")
values = st.sidebar.slider("Range of Chickens to Iterate Over:", 1,50,(5,25))
simulation_runs = st.sidebar.slider("How Many Simulations per Chicken?:", 1,1000)

df, dict_list = chicken_simulation_function(low_end_chickens = values[0], 
                                            high_end_chickens = values[1], 
                                            days = 10, 
                                            sale_price = 4.25,
                                            cost_of_carton = 0.29, 
                                            yearly_low_end_egg_production = 235,
                                            yearly_high_end_egg_production = 275,
                                            bag_of_feed_cost = 23.99, 
                                            lbs_of_feed = 35, 
                                            bag_of_bedding_cost = 8.79, 
                                            cubic_feet_of_bedding = 10, 
                                            low_end_days_to_refresh = 28,
                                            high_end_days_to_refresh = 32, 
                                            additional_cost = 0, 
                                            simulations_per_chicken = simulation_runs)
#st.write(df.index)
st.write(df)

