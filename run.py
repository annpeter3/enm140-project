import numpy as np
import logging

import campaign
import strategies

logging.basicConfig(level=logging.INFO, format='%(message)s') # change between logging.DEBUG and logging.INFO for messages or not


######### Parameters ######################
effort_per_week = 3             # The ammount of effort each campaign can allocate in a week.
number_of_weeks = 5             # The number of Allocation phases until the winner is declared.
number_of_districts = 10        # The number of voting districts
T = 2                           # The number of times the simulation is repeated

initial_districts = np.array([5, 4, 3, 2, 1, -1, -2, -3, -4, -5])   # This variable counts the number of votes that player 1 has in each district 
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
    
    # Run campaign for strat_x and strat_y:
    for t in range(number_of_weeks):
        districts = campaign.apply_strategy(districts, t, effort_per_week, strategies_dict['strat_x'], strategies_dict['strat_y']) # change to strategies.user_input_strat for manual input
    
    # Hold election
    results[i] = campaign.declare_winner(districts)

logging.info("Number of draws: %s, number of wins p1: %s, number of wins p2: %s", np.count_nonzero(results==0), np.count_nonzero(results==1), np.count_nonzero(results==-1))