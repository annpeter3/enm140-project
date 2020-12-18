import numpy as np
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

import strategies
from run_all_vs_all import run_all_vs_all_fcn 
from run_all_vs_all import process_results
import districtbuilder as db

logging.basicConfig(level=logging.INFO, format='%(message)s') # change between logging.DEBUG and logging.INFO for messages or not

######### Parameters ######################
effort_per_week_array = np.arange(start=1, stop=20)            # The amount of effort each campaign can allocate in a week.
number_of_districts_array = np.arange(start=1, stop=20)        # The number of voting districts
number_of_weeks = 15                                           # The number of Allocation phases until the winner is declared.
number_of_weeks_array = np.arange(start=1,stop=20)
T = 100                                                          # The number of times the simulation is repeated

######### Main loop ######################
# Load all available strategies:
strategies_dict = strategies.strategies_as_dict()
mean_payoffs = np.zeros((effort_per_week_array.shape[0], number_of_districts_array.shape[0], len(strategies_dict)))

# Run sweep over effort and number of districts:
logging.info("Start sweep over effort and number of districts")
i = 0 
for effort_per_week in effort_per_week_array:
    j = 0
    
    for number_of_districts in number_of_districts_array:

        initial_districts = db.build(number_of_districts, "flat", 0)
        strategies_dict = strategies.strategies_as_dict()

        results = run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts)
        _, _, _, mean_payoffs[i,j,:] = process_results(results)

        j += 1
    
    logging.info("Iteration %d of %d finished", i, len(effort_per_week_array))

    i += 1

# Run sweep over weeks:
logging.info("Start sweep over weeks")
number_of_districts = 10
effort_per_week = 10
strategies_dict = strategies.strategies_as_dict()
initial_polls_distribution = ['stair', 'flat', 'polarized', 'cosine']
mean_payoffs_weeks = np.zeros((number_of_weeks_array.shape[0], len(initial_polls_distribution), len(strategies_dict)))

l = 0
for distribution in initial_polls_distribution:
    k = 0
    logging.info("Running for initial distrbution %s", distribution)
    for number_of_weeks in number_of_weeks_array:
        initial_districts = db.build(number_of_districts, "flat", 10)
        strategies_dict = strategies.strategies_as_dict()

        results = run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts)
        _, _, _, mean_payoffs_weeks[k,l,:] = process_results(results)

        k += 1

    l += 1

# Run sweep over initial polls distribution:
logging.info("Start sweep over initial distribution")
m = 0
initial_polls_distribution = ['stair', 'flat', 'polarized', 'cosine']
number_of_districts = 10
effort_per_week = 3
number_of_weeks = 15
strategies_dict = strategies.strategies_as_dict()
mean_payoffs_polls = np.zeros((len(initial_polls_distribution), len(strategies_dict)))

for distr in initial_polls_distribution:
    initial_districts = db.build(number_of_districts, distr, 10)
    strategies_dict = strategies.strategies_as_dict()

    results = run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts)
    _, _, _, mean_payoffs_polls[m,:] = process_results(results)

    m += 1


# Save the result:
with open('parameter-sweep-results-2.txt', 'wb') as f:
    pickle.dump(mean_payoffs, f)

with open('parameter-sweep-results-3.txt', 'wb') as f:
    pickle.dump(mean_payoffs_weeks, f)

with open('parameter-sweep-results-4.txt', 'wb') as f:
    pickle.dump(mean_payoffs_polls, f)


# To access the results, do:
# with open('parameter-sweep-results-2.txt', 'rb') as f:
#     mean_payoffs = pickle.load(f)

# with open('parameter-sweep-results-3.txt', 'rb') as f:
#     mean_payoffs_weeks = pickle.load(f)

# with open('parameter-sweep-results-4.txt', 'rb') as f:
#     mean_payoffs_polls = pickle.load(f)

######### Visualise ######################
# Effort and number of districts:
strategies_dict = strategies.strategies_as_dict()
labels = list(strategies_dict.keys()) # OBS Might be in the wrong order as dicts does not have a fix order?
X,Y = np.meshgrid(effort_per_week_array, number_of_districts_array)
vmin = np.min(mean_payoffs)
vmax = np.max(mean_payoffs)

for i in range(len(labels)):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf1 = ax.plot_surface(X, Y, mean_payoffs[:,:,i].T, cmap='viridis', vmin=vmin, vmax=vmax)
    ax.set_zlim(vmin,vmax)
    fig.colorbar(surf1, shrink=0.5, aspect=5)

    ax.set_xlabel('Effort per week')
    ax.set_ylabel('Number of districts')
    ax.set_zlabel('Mean payoff')
    plt.title('Parameter Sweep ' + labels[i])
    plt.show(block=False)

# Number of weeks:
fig = plt.figure()
for i in range(len(labels)):
    plt.plot(number_of_weeks_array, mean_payoffs_weeks[:,0,i], label=labels[i])
plt.xlabel('Number of weeks')
plt.ylabel('Mean payoff')
plt.legend()
plt.title("Stair")
plt.show(block=False)

fig = plt.figure()
for i in range(len(labels)):
    plt.plot(number_of_weeks_array, mean_payoffs_weeks[:,1,i], label=labels[i])
plt.xlabel('Number of weeks')
plt.ylabel('Mean payoff')
plt.legend()
plt.title('Flat')
plt.show(block=False)

fig = plt.figure()
for i in range(len(labels)):
    plt.plot(number_of_weeks_array, mean_payoffs_weeks[:,2,i], label=labels[i])
plt.xlabel('Number of weeks')
plt.ylabel('Mean payoff')
plt.legend()
plt.title('Polarized')
plt.show(block=False)

fig = plt.figure()
for i in range(len(labels)):
    plt.plot(number_of_weeks_array, mean_payoffs_weeks[:,3,i], label=labels[i])
plt.xlabel('Number of weeks')
plt.ylabel('Mean payoff')
plt.legend()
plt.title('Cosine')
plt.show(block=False)

# Initial polls distribution:
x = np.arange(len(labels))
width = 0.2
fig = plt.figure()
plt.bar(x - 3/2*width, mean_payoffs_polls[0,:], width, label=initial_polls_distribution[0], tick_label=labels)
plt.bar(x - 1/2*width, mean_payoffs_polls[1,:], width, label=initial_polls_distribution[1], tick_label=labels)
plt.bar(x + 1/2*width, mean_payoffs_polls[2,:], width, label=initial_polls_distribution[2], tick_label=labels)
plt.bar(x + 3/2*width, mean_payoffs_polls[3,:], width, label=initial_polls_distribution[3], tick_label=labels)
plt.ylabel('Mean payoff')
plt.legend()
plt.axhline(0,color='black')
for loc in x:
    plt.axvline(loc+2.5*width,color='black')
plt.show(block=False)

plt.show() # to block the script