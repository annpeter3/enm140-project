# Possible structure:
# Assuming 2 players, equal amount of inhabitants and representatives

# Parameters:
# n = the number of rounds
# d = the number of districts
# N = the number of inhabitants in each district
# districts = array of size d x n, indicating the current poll/result in each district (either 0 or 1, 
#   or as a number <= N for the inhabitants voting for player 1) (i.e. as a whole or on an inhabitant level?)
# effort = array of size 2 x d, the available amount of effort for each player and each week


# Strategy functions:
#def strategy_1():
    # Input: the result for the districts for the last round(s), the number of the current round, the effort for this player (for this week or in total)
    # Output: the resource allocation for this round for this player

# and more ...
# Store the set of strategy functions: probably in a dict?


# Play a round of a 2-player-game:
#def play_2_player_round():
    # Input: the result for the districts for the last round(s), the strategy functions for the 2 players, 
    #        the number of the current round, the effort
    # Output: the result for the districts for this round


# Play the whole game:
    # Run play_2_player_round() in a loop for the set number of rounds
