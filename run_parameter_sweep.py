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
effort_per_week_array = np.arange(start=1, stop=40)            # The amount of effort each campaign can allocate in a week.
effort_per_week = 5

number_of_districts_array = np.arange(start=1, stop=40)        # The number of voting districts
number_of_districts = 10

number_of_weeks = 15                                           # The number of Allocation phases until the winner is declared.
number_of_weeks_array = np.arange(start=1,stop=40)

T = 100                                                         # The number of times the simulation is repeated

######### Functions ######################
# Run sweep over effort and number of districts:
def param_sweep_effort_districts():
    logging.info("Start sweep over effort and number of districts")
    
    # Load all available strategies:
    strategies_dict = strategies.strategies_as_dict()
    mean_payoffs = np.zeros((effort_per_week_array.shape[0], number_of_districts_array.shape[0], len(strategies_dict)))
    
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

    # Save the result:
    with open('parameter-sweep-results-effort-districts.txt', 'wb') as f:
        pickle.dump(mean_payoffs, f)

    return mean_payoffs

# Run sweep over weeks:
def param_sweep_weeks(initial_polls_distribution):
    logging.info("Start sweep over weeks")
    strategies_dict = strategies.strategies_as_dict()
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
    
    with open('parameter-sweep-results-weeks.txt', 'wb') as f:
        pickle.dump(mean_payoffs_weeks, f)

    return mean_payoffs_weeks

# Run sweep over initial polls distribution:
def param_sweep_initial_polls(initial_polls_distribution):
    logging.info("Start sweep over initial distribution")
    m = 0
    strategies_dict = strategies.strategies_as_dict()
    mean_payoffs_polls = np.zeros((len(initial_polls_distribution), len(strategies_dict)))

    for distr in initial_polls_distribution:
        initial_districts = db.build(number_of_districts, distr, 10)
        strategies_dict = strategies.strategies_as_dict()

        results = run_all_vs_all_fcn(strategies_dict, effort_per_week, number_of_weeks, number_of_districts, T, initial_districts)
        _, _, _, mean_payoffs_polls[m,:] = process_results(results)

        m += 1

    
    with open('parameter-sweep-results-polls.txt', 'wb') as f:
        pickle.dump(mean_payoffs_polls, f)

    return mean_payoffs_polls


######### Main loop ######################
initial_polls_distribution = ['stair', 'flat', 'polarized', 'cosine']

mean_payoffs = param_sweep_effort_districts()
mean_payoffs_weeks = param_sweep_weeks(initial_polls_distribution)
mean_payoffs_polls = param_sweep_initial_polls(initial_polls_distribution)


# To access the saved results, do:
# with open('parameter-sweep-results-effort-districts.txt', 'rb') as f:
#      mean_payoffs = pickle.load(f)

# with open('parameter-sweep-results-weeks.txt', 'rb') as f:
#     mean_payoffs_weeks = pickle.load(f)

# with open('parameter-sweep-results-polls.txt', 'rb') as f:
#     mean_payoffs_polls = pickle.load(f)


######### Visualise ######################
# Effort and number of districts:
strategies_dict = strategies.strategies_as_dict()
labels = list(strategies_dict.keys())
X,Y = np.meshgrid(effort_per_week_array, number_of_districts_array)
vmin = np.min(mean_payoffs)
vmax = np.max(mean_payoffs)

# Font sizes:
plt.rc('font', size=12)          
plt.rc('axes', titlesize=15)     
plt.rc('axes', labelsize=18)    
plt.rc('xtick', labelsize=18)   
plt.rc('ytick', labelsize=12)    
plt.rc('legend', fontsize=12)    
plt.rc('axes', titlesize=25)

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

plt.show(block=False)

# Number of weeks:
for j in range(len(initial_polls_distribution)):
    fig = plt.figure()
    for i in range(len(labels)):
        plt.plot(number_of_weeks_array, mean_payoffs_weeks[:,j,i], label=labels[i])
    plt.xlabel('Number of weeks')
    plt.ylabel('Mean payoff')
    plt.legend()
    plt.title('Initial distribution is ' + initial_polls_distribution[j] + ', effort = ' + str(effort_per_week) + ', districts = ' + str(number_of_districts))
    plt.show(block=False)

# Initial polls distribution:
x = np.arange(len(labels))
width = 0.2
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.bar(x - 3/2*width, mean_payoffs_polls[0,:], width, label=initial_polls_distribution[0])
plt.bar(x - 1/2*width, mean_payoffs_polls[1,:], width, label=initial_polls_distribution[1], tick_label=labels)
plt.bar(x + 1/2*width, mean_payoffs_polls[2,:], width, label=initial_polls_distribution[2])
plt.bar(x + 3/2*width, mean_payoffs_polls[3,:], width, label=initial_polls_distribution[3])
plt.ylabel('Mean payoff')
plt.xticks(rotation=50)
for label in ax.get_xmajorticklabels():
    label.set_horizontalalignment("right")
fig.subplots_adjust(bottom=0.3)
plt.legend()
plt.axhline(0,color='black')
for loc in x:
    plt.axvline(loc+2.5*width,color='black')
plt.show(block=False)

width = 0.4
for i in range(len(initial_polls_distribution)):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rects = plt.bar(x, mean_payoffs_polls[i,:], width, label=initial_polls_distribution[i], tick_label=labels, color='C' + str(i))
    plt.axhline(0,color='black')
    plt.title('Initial distribution: ' + initial_polls_distribution[i])
    ax.set_ylim(-0.85,0.75)
    plt.xticks(rotation=50)
    for label in ax.get_xmajorticklabels():
        label.set_horizontalalignment("right")
    fig.subplots_adjust(bottom=0.3)
    plt.ylabel('Mean payoff')


plt.show() # to block the script