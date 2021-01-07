import numpy as np
import logging
import itertools
import matplotlib.pyplot as plt

import campaign
import strategies
import districtbuilder as db

logging.basicConfig(level=logging.INFO, format='%(message)s') # change between logging.DEBUG and logging.INFO for messages or not

######### Parameters ######################
effort_per_week = 30             # The amount of effort each campaign can allocate in a week.
number_of_weeks = 15             # The number of Allocation phases until the winner is declared.
number_of_districts = 15        # The number of voting districts
T = 100                           # The number of times the simulation is repeated

initial_districts = db.build(number_of_districts, 'stair', 10)   # This variable counts the number of votes that player 1 has in each district 
                                                            # minus the votes needed for a draw in a district.
                                                            # Hence a positive number means that player one wins the district
                                                            # This is could be a set of states where voter support is to 10-0, 9-1, 8-2, 7-3, 6-4, 4-6, 3-7.. etc 
                                                            # (but we dont have to care about the absolute number of voters)

# Load all available strategies:
strategies_dict = strategies.strategies_as_dict()

######### Functions ######################

# Main function:
def run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts):
    # All pairs of strategies incl against itself:
    all_combinations = itertools.combinations_with_replacement(strategies_dict, 2)
    # Create dict for saving the results: (the array counts nbr of wins, draws, and losses)
    results = {item2: {item: np.array([0,0,0]) for item in strategies_dict} for item2 in strategies_dict}

    for pair in all_combinations:
        p1_strat = strategies_dict[pair[0]]
        p2_strat = strategies_dict[pair[1]]

        # Run T election campaigns:
        for _ in range(T):
            districts = initial_districts
            logging.debug("Initial polls: %s", districts)
    
            # Run campaign:
            for t in range(number_of_weeks):
                districts = campaign.apply_strategy(districts, t, effort_per_week, p1_strat, p2_strat)
    
            # Hold election
            result = campaign.declare_winner(districts)

            if result == 1:
                # Player 1 won
                results[pair[0]][pair[1]][0] += 1
                results[pair[1]][pair[0]][2] += 1
            elif result == -1:
                # Player 2 won
                results[pair[1]][pair[0]][0] += 1
                results[pair[0]][pair[1]][2] += 1
            else:
                # Draw
                results[pair[1]][pair[0]][1] += 1
                results[pair[0]][pair[1]][1] += 1
    
    return results

# Processes the results into number of wins, losses and draws, and computes the mean payoff:
def process_results(results):
    wins = np.zeros(len(strategies_dict.keys()))
    losses = np.zeros(len(strategies_dict.keys()))
    draws = np.zeros(len(strategies_dict.keys()))
    mean_payoff = np.zeros(len(strategies_dict.keys()))
    i = 0

    for key1 in results:
        # Count nbr of wins, losses, and draws for strategy key1:
        for key2 in results[key1]:
            #if key1 != key2: # add if don't want to incl strat against itself
                wins[i] += results[key1][key2][0]
                losses[i] += results[key1][key2][2]
                draws[i] += results[key1][key2][1]
    
        # Count mean payoff for strategy key1:
        mean_payoff[i] = (wins[i]-losses[i])/(wins[i]+losses[i]+draws[i])

        i += 1
    
    return wins, losses, draws, mean_payoff

######### Run and visualise ######################
if __name__ == "__main__":
    results = run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts)
    wins, losses, draws, mean_payoff = process_results(results)

    # Visualise the nbr of wins, losses and draws for each strategy:
    labels = strategies_dict.keys()
    x = np.arange(len(labels))
    width = 0.2

    # Font sizes:
    plt.rc('font', size=12)          
    plt.rc('axes', titlesize=15)     
    plt.rc('axes', labelsize=18)    
    plt.rc('xtick', labelsize=18)   
    plt.rc('ytick', labelsize=12)    
    plt.rc('legend', fontsize=12)    
    plt.rc('axes', titlesize=25)

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, wins, width, label='Wins')
    rects3 = ax.bar(x, draws, width, label='Draws', tick_label = list(labels))
    rects2 = ax.bar(x + width, losses, width, label='Losses')

    # Remove x-ticks:
    # plt.tick_params(
    #     axis='x',
    #     which='both',
    #     bottom=False,
    #     top=False,
    #     labelbottom=False
    # )

    plt.xticks(rotation=50)
    for label in ax.get_xmajorticklabels():
        label.set_horizontalalignment("right")
    fig.subplots_adjust(bottom=0.3)

    ax.set_ylim(0,880)
    ax.legend()

    mean_payoff = np.around(mean_payoff, decimals=2)

    # Add the mean payoffs to the plot:
    table = plt.table(cellText=[mean_payoff],
                        #colLabels=list(labels),
                        rowLabels=['Mean payoff'],
                        rowColours=['lightgray'],
                        #colColours=len(mean_payoff)*['lightgray'],
                        cellLoc='center',
                        loc='top')
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    plt.subplots_adjust(bottom=0.3)

    plt.title('Results per strategy', y = 1.1)

    plt.show()