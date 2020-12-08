import numpy as np
import random as rn


def strategies_as_dict():
    # Save all strategy functions in a dict. Call a fcn using strategies['strat_x'](polls,effort).
    strategies = {}
    strategies['strat_x'] = strat_x
    strategies['strat_y'] = strat_y
    strategies['strat_zero'] = strat_zero
    strategies['strat_random_1'] = strat_random_1
    strategies['strat_random_2'] = strat_random_2
    strategies['strat_larger_margin'] = strat_larger_margin

    return strategies

# This strategy puts the effort in the states where the player is losing by the smallest margin.
def strat_x(polls, effort):
    allocation = np.zeros(polls.shape)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    for _ in range(effort):
        if min(polls_after) <= 0:
            min_dif_not_winning_val = max([i for i in polls_after if i <= 0])
        else:
            min_dif_not_winning_val = min(polls_after)

        min_dif_not_winning_ind = rn.choice([i for i in range(number_of_districts) if polls_after[i] == min_dif_not_winning_val])
        allocation[min_dif_not_winning_ind] += 1
        polls_after[min_dif_not_winning_ind] += 1

    return allocation

# This strategy puts the effort in the states where the difference is the smalles.
def strat_y(polls, effort):
    allocation = np.zeros(polls.shape)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    for _ in range(effort):
        min_dif_val = min(np.abs(polls_after))
        min_dif_ind = rn.choice([i for i in range(number_of_districts) if abs(polls_after[i]) == min_dif_val])
        allocation[min_dif_ind] += 1
        polls_after[min_dif_ind] += 1

    return allocation


# Use to test smth vs a player that does nothing.
def strat_zero(polls, effort):
    return np.zeros(polls.shape)


# Enter allocation manually e.g. 0001110100
def user_input_strat(polls, effort):
    number_of_districts = len(polls)
    valid_input = False
    while not valid_input:
        usr_input = input('Enter allocation of {} effort for {} districs: '.format(effort, number_of_districts))
        allocation = np.array([int(num) for num in usr_input])

        if len(allocation) == number_of_districts and sum(allocation) <= effort:
            valid_input = True
        else:
            print('Invalid allocation')

    return allocation

# Uniformly random allocation:
def strat_random_1(polls, effort):
    allocation = np.zeros(polls.shape)
    idx = np.random.randint(allocation.shape, size=effort)

    for i in range(effort):
        allocation[idx[i]] += 1

    return allocation

# Uniformly random allocation over districts where loosing:
def strat_random_2(polls, effort):
    allocation = np.zeros(polls.shape)
    polls_after = polls.copy()

    for _ in range(effort):
        if min(polls_after) <= 0:
            negative_idx = np.where(polls_after <= 0)[0]
            rnd = np.random.randint(negative_idx.shape, size = 1)
            index = negative_idx[rnd[0]]
        else:
            index = np.random.randint(allocation.shape, size=1)

        allocation[index] += 1
        polls_after[index] += 1

    return allocation

# As strat_x but puts effort until the poll is effort/3:
def strat_larger_margin(polls, effort):
    allocation = np.zeros(polls.shape)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    for _ in range(effort):
        if len(polls_after[np.logical_and(polls_after < effort/3,polls_after >= 0)]) > 0:
            larger_margin = max(polls_after[np.logical_and(polls_after < effort/3,polls_after >= 0)])
        elif min(polls_after) <= 0:
            larger_margin = max([i for i in polls_after if i <= 0])
        else:
            larger_margin = min(polls_after)

        larger_margin_ind = rn.choice([i for i in range(number_of_districts) if polls_after[i] == larger_margin])
        allocation[larger_margin_ind] += 1
        polls_after[larger_margin_ind] += 1

    return allocation