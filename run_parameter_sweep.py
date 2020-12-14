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
effort_per_week_array = np.arange(start=1, stop=20)            # The amount of effort each campaign can allocate in a week.
number_of_districts_array = np.arange(start=1, stop=20)        # The number of voting districts
number_of_weeks = 10                                           # The number of Allocation phases until the winner is declared.
T = 20                                                          # The number of times the simulation is repeated

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
    
    logging.info("Iteration %d of %d finished", i, len(effort_per_week_array))

    i += 1

# Save the result:
file = open('./Results/parameter-sweep-results.txt', 'wb')
pickle.dump(mean_payoffs, file)
file.close()

# To access the results, do:
#file = open('./Results/parameter-sweep-results.txt', 'rb')
#mean_payoffs = pickle.load(file)

######### Visualise ######################
X,Y = np.meshgrid(effort_per_week_array, number_of_districts_array)
vmin = np.min(mean_payoffs)
vmax = np.max(mean_payoffs)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf1 = ax.plot_surface(X, Y, mean_payoffs[:,:,0], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf1, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_x')
plt.show(block=False)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,1], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_y')
plt.show(block=False)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,2], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_zero')
plt.show(block=False)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,3], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_random_1')
plt.show(block=False)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,4], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_random_2')
plt.show(block=False)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,5], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_larger_margin')
plt.show(block=False)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf2 = ax.plot_surface(X, Y, mean_payoffs[:,:,6], cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_zlim(vmin,vmax)
fig.colorbar(surf2, shrink=0.5, aspect=5)

ax.set_xlabel('Effort per week')
ax.set_ylabel('Number of districts')
ax.set_zlabel('Mean payoff')
plt.title('Parameter Sweep strat_mixed')
plt.show()