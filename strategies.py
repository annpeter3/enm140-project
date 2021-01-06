import numpy as np
import random as rn


def strategies_as_dict():
    # Save all strategy functions in a dict. Call a fcn using strategies['strat_x'](polls,effort).
    strategies = {}
    strategies['Min losing'] = strat_min_losing
    strategies['Min diff'] = strat_min_diff
    strategies['Zero'] = strat_zero
    strategies['Min losing + defend lead'] = strat_min_losing_and_defend_lead
    strategies['Min diff + defend lead'] = strat_min_diff_and_defend_lead
    strategies['Counter'] = strat_assume_opponent_is_min_losing_and_defend_lead
    strategies['Random_1'] = strat_random_1
    strategies['Random_2'] = strat_random_2
    strategies['larger_margin'] = strat_larger_margin
    strategies['Mixed_1'] = strat_mixed
    strategies['Mixed_2'] = strat_mixed_2
    strategies['Effort'] = strat_effort

    return strategies

# This strategy puts the effort in the states where the player is losing by the smallest margin.
def strat_min_losing(polls, effort): # aka strat_x
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
def strat_min_diff(polls, effort): # aka strat_y
    allocation = np.zeros(polls.shape)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    for _ in range(effort):
        min_dif_val = min(np.abs(polls_after))
        min_dif_ind = rn.choice([i for i in range(number_of_districts) if abs(polls_after[i]) == min_dif_val])
        allocation[min_dif_ind] += 1
        polls_after[min_dif_ind] += 1

    return allocation

# This strategy will attempt to defend a lead by spending effort in the districts where it's leading, if its leading in a majority of districts
# If it is not winning in a majority of states, it will try to win new states by playing strat_min_diff
def strat_min_diff_and_defend_lead(polls, effort):
    allocation = np.zeros_like(polls)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    for _ in range(effort):
        my_score = len(polls_after[polls_after > 0]) # If do this outside the for loop -> worse result

        if my_score <= number_of_districts/2:
            # If loosing or draw, play strat_min_diff:
            allocation_strat_min_diff = strat_min_diff(polls_after,1).astype(int)
            allocation += allocation_strat_min_diff
            polls_after += allocation_strat_min_diff
        else:
            # If winning, put effort in the districts where winning with the smallest margin:
            min_dif_winning_val = min([i for i in polls_after if i >= 0])
            min_dif_winning_ind = rn.choice([i for i in range(number_of_districts) if abs(polls_after[i]) == min_dif_winning_val])
            allocation[min_dif_winning_ind] += 1
            polls_after[min_dif_winning_ind] += 1
        
    return allocation


# This strategy will attempt to defend a lead by spending effort in the districts where it's leading, if its leading in a majority of districts
# If it is not winning in a majority of states, it will try to win new states by playing strat_min_losing
def strat_min_losing_and_defend_lead(polls, effort):
    allocation = np.zeros_like(polls)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    for _ in range(effort):
        my_score = len(polls_after[polls_after > 0]) # # If do this outside the for loop -> worse result

        if my_score <= number_of_districts/2:
            # If loosing or draw, play strat_min_losing:
            allocation_strat_min_losing = strat_min_losing(polls_after,1).astype(int)
            allocation += allocation_strat_min_losing
            polls_after += allocation_strat_min_losing
        else:
            # If winning, put effort in the districts where winning with the smallest margin:
            min_dif_winning_val = min([i for i in polls_after if i >= 0])
            min_dif_winning_ind = rn.choice([i for i in range(number_of_districts) if abs(polls_after[i]) == min_dif_winning_val])
            allocation[min_dif_winning_ind] += 1
            polls_after[min_dif_winning_ind] += 1
    
    return allocation


# This strat will assume the opponent is doing the min losing defend lead strat, and calcualte its oppnents moves
# Then make its own moves
def strat_assume_opponent_is_min_losing_and_defend_lead(polls, effort):
    allocation = np.zeros_like(polls)
    number_of_districts = len(allocation)
    polls_after = polls.copy()
    polls_after = polls_after * -1

    for _ in range(effort):
        my_score = len(polls_after[polls_after > 0]) # # If do this outside the for loop -> worse result

        if my_score <= number_of_districts/2:
            # If loosing or draw, play strat_min_losing:
            for _ in range(effort):
                if min(polls_after) <= 0:
                    min_dif_not_winning_val = max([i for i in polls_after if i <= 0])
                else:
                    min_dif_not_winning_val = min(polls_after)
                if (polls_after == min_dif_not_winning_val).sum() == 1:
                    min_dif_not_winning_ind = rn.choice([i for i in range(number_of_districts) if polls_after[i] == min_dif_not_winning_val])
                    polls_after[min_dif_not_winning_ind] += 1
        else:
            # If winning, put effort in the districts where winning with the smallest margin:
            min_dif_winning_val = min([i for i in polls_after if i >= 0])
            if (polls_after == min_dif_winning_val).sum() == 1:
                min_dif_winning_ind = rn.choice([i for i in range(number_of_districts) if abs(polls_after[i]) == min_dif_winning_val])
                polls_after[min_dif_winning_ind] += 1

    polls_after = polls_after * -1
    
    return strat_min_losing_and_defend_lead(polls_after, effort)


# Use to test smth vs a player that does nothing.
def strat_zero(polls, effort):
    return np.zeros(polls.shape)


# Enter allocation manually e.g. 0001110100
def user_input_strat(polls, effort):
    number_of_districts = len(polls)
    valid_input = False
    while not valid_input:
        print(polls)
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

# Mixed strategy:
def strat_mixed(polls, effort):
    rnd = np.random.rand()

    if rnd < 0.2:
        return strat_min_losing(polls,effort)
    else:
        return strat_min_diff(polls,effort)

def strat_mixed_2(polls, effort):
    rnd = np.random.rand()

    if rnd < 0.5:
        return strat_min_losing_and_defend_lead(polls, effort)
    else:
        return strat_min_diff_and_defend_lead(polls, effort)

# A strategy that puts all its effort in one district each round and takes into account if it is currently winning or not.
def strat_effort(polls, effort):
    allocation = np.zeros_like(polls)
    number_of_districts = len(allocation)
    my_score = len(polls[polls > 0])

    if my_score <= number_of_districts/2:
        # Loosing
        if polls[np.logical_and(polls <= 0, polls > -effort)].shape[0] >= 1:
            # Put all where is loosing by the most (but which is smaller than effort)
            max_loosing = np.min(polls[np.logical_and(polls <= 0, polls > -effort)]) 
            max_loosing_ind = rn.choice([i for i in range(number_of_districts) if polls[i] == max_loosing])
            allocation[max_loosing_ind] = effort   
        else:
            # Is loosing by something larger than effort everywhere, place all where is loosing by the least:
            min_loosing = np.min(polls[polls <= 0])
            min_loosing_ind = rn.choice([i for i in range(number_of_districts) if polls[i] == min_loosing])
            allocation[min_loosing_ind] = effort 
    else:
        # Winning
        # Put all effort where is winning by the smallest margin
        min_winning = np.min(polls[polls >= 0])
        min_winning_ind = rn.choice([i for i in range(number_of_districts) if polls[i] == min_winning])
        allocation[min_winning_ind] = effort

    return allocation