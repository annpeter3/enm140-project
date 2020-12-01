import numpy as np

######### Parameters ######################
effort_per_week = 3             # The ammount of effort each campaign can allocate in a week.
number_of_weeks = 5             # The number of Allocation phases until the winner is declared.
number_of_districts = 10        # The number of voting districts

districts = np.array([5, 4, 3, 2, 1, -1, -2, -3, -4, -5])   # This variable counts the number of votes that player 1 has in each district 
                                                            # minus the votes needed for a draw in a district.
                                                            # Hence a positive number means that player one wins the district
                                                            # This is could be a set of states where voter support is to 10-0, 9-1, 8-2, 7-3, 6-4, 4-6, 3-7.. etc 
                                                            # (but we dont have to care about the absolute number of voters)


def apply_strategy(districts, week):
    p1effort = player1_allocate(districts)
    p2effort = player2_allocate(districts)

    districts = districts + p1effort + p2effort

    print("Polls after week ", week + 1)
    print(districts)

    return districts

# This strategy puts the effort in the states where the player is losing by the smallest margin. (FLAW: if multiple states are equal, it will choose the first index encountered)
def strat_x(polls):
    allocation = np.zeros(number_of_districts)
    polls_after = polls.copy()

    for _ in range(effort_per_week):
        min_dif_not_winning = np.where(polls_after == max(polls_after[polls_after<=0]))[0][0] # Todo: does not work when all elements positive
        allocation[min_dif_not_winning] += 1
        polls_after[min_dif_not_winning] += 1

    return allocation

# This strategy puts the effort in the states where the difference is the smalles. (FLAW: if multiple states are equally distant, it will choose the first index encountered)
def strat_y(polls):
    allocation = np.zeros(number_of_districts)
    polls_after = polls.copy()

    for _ in range(effort_per_week):
        min_dif = np.argmin(np.abs(polls_after))
        allocation[min_dif] += 1
        polls_after[min_dif] += 1

    return allocation

# Use to test smth vs a player that does nothing.
def strat_zero(polls):
    return np.zeros(number_of_districts)

# Multiply all values in a list by -1
def flip_list(list): 
    return (-1)*list

# Runs a strategy for player 1
def player1_allocate(polls):
    p1allocation = strat_x(polls)
    return p1allocation

# Runs a strategy for player 2
# Player 2 allocation flips poll numbers before applying strategy so that the strategy doesn't need to be flipped
# Then also flips the allocation before returning since player 2 wants negative numbers
def player2_allocate(polls):
    p2pov = flip_list(polls)
    p2allocation = strat_y(p2pov)
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

print("Initial polls:")
print(districts)
# Run campaign
for x in range(number_of_weeks):
    districts = apply_strategy(districts, x)
# Hold election
declare_winner(districts)