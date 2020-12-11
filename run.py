import numpy as np
import logging
import matplotlib.pyplot as plt

import campaign
import strategies

logging.basicConfig(level=logging.DEBUG, format='%(message)s') # change between logging.DEBUG and logging.INFO for messages or not


######### Parameters ######################
effort_per_week = 3             # The ammount of effort each campaign can allocate in a week.
number_of_weeks = 5             # The number of Allocation phases until the winner is declared.
number_of_districts = 4        # The number of voting districts
T = 1                           # The number of times the simulation is repeated

initial_districts = np.array([2, 1, -1, -2])                        # This variable counts the number of votes that player 1 has in each district 
                                                                    # minus the votes needed for a draw in a district.
                                                                    # Hence a positive number means that player one wins the district
                                                                    # This is could be a set of states where voter support is to 10-0, 9-1, 8-2, 7-3, 6-4, 4-6, 3-7.. etc 
                                                                    # (but we dont have to care about the absolute number of voters)

# Load all available strategies:
strategies_dict = strategies.strategies_as_dict()

# For visualisation of the game:
player1 = np.zeros(number_of_weeks + 1)
player2 = np.zeros(number_of_weeks + 1)
draws = np.zeros(number_of_weeks + 1)

player1[0] = len(initial_districts[initial_districts > 0])
player2[0] = len(initial_districts[initial_districts < 0])
draws[0] = len(initial_districts[initial_districts == 0]) 


# Run T election campaigns:
results = np.zeros(T)
for i in range(T):

    districts = initial_districts
    logging.debug("Initial polls: %s", districts)
    
    # Run campaign for strat_x and strat_y:
    for t in range(number_of_weeks):
        districts = campaign.apply_strategy(districts, t, effort_per_week, strategies_dict['strat_y'], strategies_dict['strat_x']) # change to strategies.user_input_strat for manual input

        player1[t+1] = len(districts[districts > 0])
        player2[t+1] = len(districts[districts < 0])
        draws[t+1] = len(districts[districts == 0]) 

    # Hold election
    results[i] = campaign.declare_winner(districts)

logging.info("Number of draws: %s, number of wins p1: %s, number of wins p2: %s", np.count_nonzero(results==0), np.count_nonzero(results==1), np.count_nonzero(results==-1))

y_min = np.min(np.array([np.min(player1), np.min(player2), np.min(draws)])) - 0.5
y_max = np.max(np.array([np.max(player1), np.max(player2), np.max(draws)])) + 0.5


# Plot results for each week:
for i in range(number_of_weeks+1):
    plt.figure()
    plt.plot(range(i), player1[0:i], 'o-', label='Player 1')
    plt.plot(range(i), player2[0:i], 'o-', label='Player 2')
    plt.plot(range(i), draws[0:i], 'o-', label='Draws')
    plt.ylim(y_min, y_max)
    plt.xlim(0,number_of_weeks+1)
    plt.legend()
    plt.show(block=False)

plt.figure()
plt.plot(range(number_of_weeks+1), player1, 'o-', label='Player 1')
plt.plot(range(number_of_weeks+1), player2, 'o-', label='Player 2')
plt.plot(range(number_of_weeks+1), draws, 'o-', label='Draws')
plt.ylim(y_min, y_max)
plt.xlim(0,number_of_weeks+1)
plt.legend()




plt.show()