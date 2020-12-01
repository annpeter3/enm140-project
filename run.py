import numpy as np
import campaign
import strategies

######### Parameters ######################
effort_per_week = 3             # The ammount of effort each campaign can allocate in a week.
number_of_weeks = 5             # The number of Allocation phases until the winner is declared.
number_of_districts = 10        # The number of voting districts

districts = np.array([5, 4, 3, 2, 1, -1, -2, -3, -4, -5])   # This variable counts the number of votes that player 1 has in each district 
                                                            # minus the votes needed for a draw in a district.
                                                            # Hence a positive number means that player one wins the district
                                                            # This is could be a set of states where voter support is to 10-0, 9-1, 8-2, 7-3, 6-4, 4-6, 3-7.. etc 
                                                            # (but we dont have to care about the absolute number of voters)

# Load all available strategies:
strategies = strategies.strategies_as_dict()

print("Initial polls:")
print(districts)
# Run campaign for strat_x and strat_y:
for t in range(number_of_weeks):
    districts = campaign.apply_strategy(districts, t, effort_per_week, strategies['strat_x'], strategies['strat_y'])
# Hold election
campaign.declare_winner(districts)