import numpy as np

def apply_strategy(districts, week, effort, strat_p1, strat_p2):
    p1effort = player1_allocate(districts, effort, strat_p1)
    p2effort = player2_allocate(districts, effort, strat_p2)

    districts = districts + p1effort + p2effort

    print("Polls after week ", week + 1)
    print(districts)

    return districts

# Multiply all values in a list by -1
def flip_list(list): 
    return (-1)*list

# Runs a strategy for player 1
def player1_allocate(polls, effort, strat_p1):
    p1allocation = strat_p1(polls, effort)
    return p1allocation

# Runs a strategy for player 2
# Player 2 allocation flips poll numbers before applying strategy so that the strategy doesn't need to be flipped
# Then also flips the allocation before returning since player 2 wants negative numbers
def player2_allocate(polls, effort, strat_p2):
    p2pov = flip_list(polls)
    p2allocation = strat_p2(p2pov, effort)
    return flip_list(p2allocation)

# P1 wins in states with a positive number
def declare_winner(polls):
    p1score = len(polls[polls > 0])
    p2score = len(polls[polls < 0])

    if p1score == p2score:
        print("DRAW")
    elif p1score > p2score:
        print("P1 WON")
    else:
        print("P2 WON")

