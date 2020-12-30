import numpy as np
import logging
import random as rn


def uncertain_effect(allocation):
    flip = min(allocation) < 0
    
    if flip:
        allocation *= (-1)

    new_allocation = np.array([round(rn.triangular(0, int(allocation[i]), int(allocation[i]))) for i in range(len(allocation))])

    if flip:
        new_allocation *= (-1)

    return new_allocation


def apply_strategy(districts, week, effort, strat_p1, strat_p2, effort_uncertainty = False):
    p1effort = player1_allocate(districts, effort, strat_p1)
    p2effort = player2_allocate(districts, effort, strat_p2)

    if effort_uncertainty:
        p1effort = uncertain_effect(p1effort)
        p2effort = uncertain_effect(p2effort)
            
    districts = districts + p1effort + p2effort

    logging.debug("Polls after week %s: %s", week + 1, districts)

    return districts

# Runs a strategy for player 1
def player1_allocate(polls, effort, strat_p1):
    p1allocation = strat_p1(polls, effort)
    return p1allocation

# Runs a strategy for player 2
# Player 2 allocation flips poll numbers before applying strategy so that the strategy doesn't need to be flipped
# Then also flips the allocation before returning since player 2 wants negative numbers
def player2_allocate(polls, effort, strat_p2):
    p2_polls = (-1)*polls
    p2allocation = strat_p2(p2_polls, effort)
    return (-1)*p2allocation

# P1 wins in states with a positive number
def declare_winner(polls):
    p1score = len(polls[polls > 0])
    p2score = len(polls[polls < 0])

    if p1score == p2score:
        logging.debug("DRAW")
        return 0
    elif p1score > p2score:
        logging.debug("P1 WON")
        return 1
    else:
        logging.debug("P2 WON")
        return -1

