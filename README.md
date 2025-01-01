# IntelliSwift-Tic-Tac-Toe
This repository is related with AIF 2024/2025 projects

It is an algorithm which we called it IntelliSwift which is flexible algorithm to perform tic-tac-toe game with advanced features which showed that it is faster than some algorithm, that used in Adversarial Search.

# Introduction
Tic Tac Toe, a classic strategy game, presents an opportunity to explore efficient 
decision-making algorithms. Our innovative approach, called the IntelliSwift 
Algorithm, is designed to optimize gameplay by selecting the best position on the 
grid as fast as possible. By combining offensive and defensive strategies into a
process, IntelliSwift ensures effective gameplay while maintaining simplicity and 
adaptability.
When compared to the Minimax algorithm, IntelliSwift demonstrates superior 
performance. The execution time of IntelliSwift is significantly reduced, making 
it a highly efficient alternative while maintaining robust decision-making 
capabilities. Additionally, the algorithm's adaptability allows it to function across 
various grid sizes without the need for any computationally expensive 
mathematical operations.

# The IntelliSwift operates on the principle of maintaining two key lists:

1. Defense List: This list is used by the algorithm to prevent the opponent 
from winning by tracking the positions that enable them to win. This list 
is updated whenever the game grid is modified by adding an X or an O.

3. Attack List: This list is used by the algorithm to execute an offensive 
strategy to win. It is updated whenever any modification is made to the 
game grid, whether by adding an X or an O.

## Algorithm Steps:
First: When the opponent plays:
1. The algorithm identifies the neighboring positions of the one chosen by 
the opponent (horizontal, vertical, and diagonal positions, each group in 
one cell). These are the positions that allow the opponent to win and 
achieve his goal.
2. These positions are added to the defense list if they haven’t been added 
previously, to use them by the algorithm to prevent the opponent from 
winning.
3. The entire cell which contains the chosen position is removed from the 
attack array (including the opponent's input and all related positions) 
because it is no longer valid for the algorithm to win. And the only 
chosen position is removed from the defense list.

# Second: How the algorithm selects a position:

1. If there is a cell in the ATTACK list containing only one position in the 
grid e.g. (1,0), it takes priority, as this means the algorithm needs only 
this position to win.
2. If there is a cell in the DEFENSE list containing only one position, it is 
selected to prevent the opponent from winning, as this means the 
opponent needs only this position to win.
3. If there is a shared position between the defense and attack cells, it is 
selected to stop the opponent from winning and bring the algorithm closer 
to winning.
4. If none of the above conditions are met, a position from the DEFENSE 
list is selected, where the selected position must have the larger 
possibilities to be added in ATTACK list, to maximize the chances of the 
algorithm winning.
5. Once the position for the algorithm is chosen, all associated positions in 
the DEFENSE list are removed, as they are no longer valid for the 
opponent, and only the chosen value removed from attack list. Then all 
winning possibilities for the algorithm are then added to the attack row.

## Stop Conditions:
• When both the defense and attack rows are empty, it means no one can 
win.
• When a player places his char X or Y in a row, column, or in diagonal.
