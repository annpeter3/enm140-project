import numpy as np
import random as rn


def strategies_as_dict():
    # Save all strategy functions in a dict. Call a fcn using strategies['strat_x'](polls,effort).
    strategies = {}
    strategies['strat_x'] = strat_x
    strategies['strat_y'] = strat_y
    strategies['strat_zero'] = strat_zero
    strategies['strat_y_but_defend_lead'] = strat_y_but_defend_lead

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

# This strategy will attempt to defend a lead by spending effort in the districts where it's leading, if its leading in a majority of districts
# If it is not winning in a majority of states, it will try to win new states by playing strat x
def strat_y_but_defend_lead(polls, effort):

    allocation = np.zeros(polls.shape)
    number_of_districts = len(allocation)
    polls_after = polls.copy()

    def am_i_winning_majority(polls):
        wins = 0
        for x in polls:
            if x > 0:
                wins += 1
        if wins > len(polls) / 2:
            return True
        else :
            return False

    if am_i_winning_majority(polls):
        for _ in range(effort):
            min_dif_winning_val = max([i for i in polls_after if i > 0])
            min_dif_winning_ind = rn.choice([i for i in range(number_of_districts) if abs(polls_after[i]) == min_dif_winning_val])
            allocation[min_dif_winning_ind] += 1
            polls_after[min_dif_winning_ind] += 1
        return allocation
    else:
        return strat_y(polls, effort)




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
