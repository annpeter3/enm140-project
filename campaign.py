import numpy as np

# The ammount of effort each campaign can allocate in a week.
effortPerWeek = 3
# The number of Allocation phases until the winner is declared.
numberOfWeeks = 5
# The number of voting districts
numberOfDistricts = 10
# This variable counts the number of votes that player 1 has in each districts minus the votes needed for a draw in a district.
# Hence a positive number means that player one wins the district
districts = np.array([5, 4, 3, 2, 1, -1, -2, -3, -4, -5]) # This is could be a set of states where voter support is to 10-0, 9-1, 8-2, 7-3, 6-4, 4-6, 3-7.. etc (but we dont have to care about the absolute number of voters)

def apply_strategy(districts, week):
    p1effort = player1_allocate(districts)
    p2effort = player2_allocate(districts)

    districts = districts + p1effort + p2effort

    print("Polls after week ", week + 1)
    print(districts)

    return districts

# This strategy puts the effort in the states where the player is losing by the smallest margin. (FLAW: if multiple states are equal, it will choose the first index encountered)
def strat_x(polls):
    allocation = np.zeros(numberOfDistricts)
    pollsAfter = polls.copy()

    for _ in range(effortPerWeek):
        minDifNotWinning = np.argmax(np.nonzero(pollsAfter))
        allocation[minDifNotWinning] += 1
        pollsAfter[minDifNotWinning] += 1

    return allocation

# This strategy puts the effort in the states where the difference is the smalles. (FLAW: if multiple states are equally distant, it will choose the first index encountered)
def strat_y(polls):
    allocation = np.zeros(numberOfDistricts)
    pollsAfter = polls.copy()

    for _ in range(effortPerWeek):
        minDif = np.argmin(np.abs(pollsAfter))
        allocation[minDif] += 1
        pollsAfter[minDif] += 1

    return allocation

# Use to test smth vs a player that does nothing.
def strat_zero(polls):
    return np.zeros(numberOfDistricts)

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
for x in range(numberOfWeeks):
    districts = apply_strategy(districts, x)
# Hold election
declare_winner(districts)