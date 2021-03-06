import numpy as np
import logging

import campaign
import strategies
import districtbuilder as db

logging.basicConfig(level=logging.INFO, format='%(message)s') # change between logging.DEBUG and logging.INFO for messages or not


######### Parameters ######################
effort_per_week = 10             # The ammount of effort each campaign can allocate in a week.
number_of_weeks = 5             # The number of Allocation phases until the winner is declared.
number_of_districts = 10        # The number of voting districts
T = 1000                           # The number of times the simulation is repeated

initial_districts = db.build(50, "cosine", 10)   # This variable counts the number of votes that player 1 has in each district 
                                                                    # minus the votes needed for a draw in a district.
                                                                    # Hence a positive number means that player one wins the district
                                                                    # This is could be a set of states where voter support is to 10-0, 9-1, 8-2, 7-3, 6-4, 4-6, 3-7.. etc 
                                                                    # (but we dont have to care about the absolute number of voters)

# Load all available strategies:
strategies_dict = strategies.strategies_as_dict()

# Run T election campaigns:
results = np.zeros(T)
for i in range(T):

    districts = initial_districts
    logging.debug("Initial polls: %s", districts)
    
    # Run campaign for two strategies:
    for t in range(number_of_weeks):
        districts = campaign.apply_strategy(districts, t, effort_per_week, strategies_dict['min_losing'], strategies_dict['min_diff']) # change to strategies.user_input_strat for manual input
        
    # Hold election
    results[i] = campaign.declare_winner(districts)

logging.info("Number of draws: %s, number of wins p1: %s, number of wins p2: %s", np.count_nonzero(results==0), np.count_nonzero(results==1), np.count_nonzero(results==-1))