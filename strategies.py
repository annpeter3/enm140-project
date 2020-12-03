import numpy as np

def strategies_as_dict():
    # Save all strategy functions in a dict. Call a fcn using strategies['strat_x'](polls,effort).
    strategies = {}
    strategies['strat_x'] = strat_x
    strategies['strat_y'] = strat_y
    strategies['strat_zero'] = strat_zero

    return strategies

# This strategy puts the effort in the states where the player is losing by the smallest margin. (FLAW: if multiple states are equal, it will choose the first index encountered)
def strat_x(polls, effort):
    allocation = np.zeros(polls.shape)
    polls_after = polls.copy()

    for _ in range(effort):
        min_dif_not_winning = np.where(polls_after == max(polls_after[polls_after<=0]))[0][0] # Todo: does not work when all elements positive
        allocation[min_dif_not_winning] += 1
        polls_after[min_dif_not_winning] += 1

    return allocation

# This strategy puts the effort in the states where the difference is the smalles. (FLAW: if multiple states are equally distant, it will choose the first index encountered)
def strat_y(polls, effort):
    allocation = np.zeros(polls.shape)
    polls_after = polls.copy()

    for _ in range(effort):
        min_dif = np.argmin(np.abs(polls_after))
        allocation[min_dif] += 1
        polls_after[min_dif] += 1

    return allocation

# Use to test smth vs a player that does nothing.
def strat_zero(polls):
    return np.zeros(polls.shape)



