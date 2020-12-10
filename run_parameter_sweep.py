import numpy as np
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

import strategies
from run_all_vs_all import run_all_vs_all_fcn 
from run_all_vs_all import process_results 

logging.basicConfig(level=logging.INFO, format='%(message)s') # change between logging.DEBUG and logging.INFO for messages or not

######### Parameters ######################
effort_per_week_array = np.arange(start=1, stop=10)            # The amount of effort each campaign can allocate in a week.
number_of_districts_array = np.arange(start=1, stop=10)        # The number of voting districts
number_of_weeks = 10                                           # The number of Allocation phases until the winner is declared.
T = 1                                                          # The number of times the simulation is repeated

######### Main loop ######################
# Load all available strategies:
strategies_dict = strategies.strategies_as_dict()
mean_payoffs = np.zeros((effort_per_week_array.shape[0], number_of_districts_array.shape[0], len(strategies_dict)))

i = 0 
for effort_per_week in effort_per_week_array:
    j = 0
    
    for number_of_districts in number_of_districts_array:

        initial_districts = np.zeros(number_of_districts)
        strategies_dict = strategies.strategies_as_dict()

        results = run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts)
        _, _, _, mean_payoffs[i,j,:] = process_results(results)

        j += 1
    
    i += 1

# Save the result:
file = open('./Results/parameter-sweep-results.txt', 'wb')
pickle.dump(mean_payoffs, file)
file.close()

# To access the results, do:
#file = open('parameter-sweep-results.txt', 'rb')
#mean_payoffs_2 = pickle.load(file)

######### Visualise ######################
fig = plt.figure(figsize=plt.figaspect(0.5))

X,Y = np.meshgrid(effort_per_week_array, number_of_districts_array)

ax = fig.add_subplot(1, 2, 1, projection='3d')
surf1 = ax.plot_surface(X, Y, mean_payoffs[:,:,0], cmap='hot')
#fig.colorbar(surf1, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff strat_x')

ax = fig.add_subplot(1, 2, 2, projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,1], cmap='hot')
#fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff strat_y')

plt.show()
