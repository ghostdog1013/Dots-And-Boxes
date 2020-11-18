# CS 111 Intro to Programming
# Shuhang Xue, Yilun Liu
# Professor Aaron Bauer
# Final Project: Dots And Boxes
# 2019/11/23



import copy

def get_opponent(player):
    if player == "A":
        return "B"                   # The user is represented by letter 'A' on his move and the computer is represented by 'B'
    return "A"

colors = {
"A": "\u001b[34;1m",                 # The moves by the user and AI are represented by blue and red colors, respectively.
"B": "\u001b[31;1m"
}

class DotsAndBoxesState():              # Create a class DotsAndBoxesState to display the current state of the board
    score1 = 0                          #a static vaiable to keep track of Player's score
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn




    def get_next_moves1(self):
            """returns a list of DotsAndBoxesState for the set of possible moves from the current state"""
            moves = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == "":
                        next_board = copy.deepcopy(self.board)
                        next_board[i][j] = colors[self.turn] + self.turn + "\u001b[0m"
                        next_turn = get_opponent(self.turn)
                        moves.append(DotsAndBoxesState(next_board, next_turn))
            return moves

    def get_next_moves2(self):
            """returns a list of DotsAndBoxesState for the set of moves that can complete a sqaure"""
            moves = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == "" and self.move_makes_box(i, j):
                        next_board = copy.deepcopy(self.board)
                        next_board[i][j] = colors[self.turn] + self.turn + "\u001b[0m"
                        next_turn = get_opponent(self.turn)
                        moves.append(DotsAndBoxesState(next_board, next_turn))
            return moves

    def get_next_moves3(self):
            """returns a list of DotsAndBoxesState for the set of moves that will not let the opponent to complete a sqaure"""
            """ These moves avoid completing the third side of a box, so that the player will not be able to score that box"""
            moves = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == "" and self.move_second_inbox(i, j):
                        next_board = copy.deepcopy(self.board)
                        next_board[i][j] = colors[self.turn] + self.turn + "\u001b[0m"
                        next_turn = get_opponent(self.turn)
                        moves.append(DotsAndBoxesState(next_board, next_turn))
            return moves



    def move_makes_box(self, i, j):
            """the function checking whether there is one line left for a box"""
            if i == 0:       #top
                if self.board[i+1][j-1] != "" and self.board[i+1][j+1] != "" and self.board[i+2][j] != "":
                    return True
                return False
            if i == 6:      #bottom
                if self.board[i-1][j-1] != "" and self.board[i-1][j+1] != "" and self.board[i-2][j] != "":
                    return True
                return False
            if j == 0:     #left
                if self.board[i-1][j+1] != "" and self.board[i+1][j+1] != "" and self.board[i][j+2] != "":
                    return True
                return False
            if j == 6:     #right
                if self.board[i-1][j-1] != "" and self.board[i+1][j-1] != "" and self.board[i][j-2] != "":
                    return True
                return False
            if i == 2 or i == 4:        # # possible horizontal moves
                if self.board[i-1][j-1] != "" and self.board[i-1][j+1] != "" and self.board[i-2][j] != "":
                    return True
                if self.board[i+1][j-1] != "" and self.board[i+1][j+1] != "" and self.board[i+2][j] != "":
                    return True
                return False
            if j == 2 or j == 4:        # # possible vertical moves
                if self.board[i-1][j-1] != "" and self.board[i+1][j-1] != "" and self.board[i][j-2] != "":
                    return True
                if self.board[i-1][j+1] != "" and self.board[i+1][j+1] != "" and self.board[i][j+2] != "":
                    return True
                return False

    def move_second_inbox(self, i, j):
        """the function checking whether there is a chance for the player to score one box"""
        """the function achieves the above statement by not filling in the third line of any possible sqaure """
        if i == 0:       #top
            return check_two_spots(self.board[i+1][j-1], self.board[i+1][j+1], self.board[i+2][j])

        if i == 6:      #bottom
            return check_two_spots(self.board[i-1][j-1], self.board[i-1][j+1], self.board[i-2][j])

        if j == 0:     #left
            return check_two_spots(self.board[i-1][j+1], self.board[i+1][j+1], self.board[i][j+2])


        if j == 6:     #right
            return check_two_spots(self.board[i-1][j-1], self.board[i+1][j-1], self.board[i][j-2])


        if i == 2 or i == 4:    # possible horizontal moves
            return check_two_spots(self.board[i-1][j-1], self.board[i-1][j+1], self.board[i-2][j]) and check_two_spots(self.board[i+1][j-1], self.board[i+1][j+1], self.board[i+2][j])

        if j == 2 or j == 4:    # possible vertical moves
            return check_two_spots(self.board[i-1][j-1], self.board[i+1][j-1], self.board[i][j-2]) and check_two_spots(self.board[i-1][j+1], self.board[i+1][j+1], self.board[i][j+2])




    def check_finished_boxes(self):
        """ the function checks how many boxes have been filled in the current board"""
        finished_boxes = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == " ":
                    if self.board[i - 1][j] != "" and self.board[i + 1][j] != "" and self.board[i][j - 1] != "" and self.board[i][j + 1] != "":
                        finished_boxes += 1
        return finished_boxes



    def check_score(self, move):
        """ the function checks if the current move the player makes completes a box"""

        i = int(move) // 7
        j = int(move) % 7             #find the corresponding index of the input move

        if i == 0:       #top
            if self.board[i+1][j-1] != "" and self.board[i+1][j+1] != "" and self.board[i+2][j] != "":
                return 1
            return 0
        if i == 6:      #bottom
            if self.board[i-1][j-1] != "" and self.board[i-1][j+1] != "" and self.board[i-2][j] != "":
                return 1
            return 0
        if j == 0:     #left
            if self.board[i-1][j+1] != "" and self.board[i+1][j+1] != "" and self.board[i][j+2] != "":
                return 1
            return 0
        if j == 6:     #right
            if self.board[i-1][j-1] != "" and self.board[i+1][j-1] != "" and self.board[i][j-2] != "":
                return 1
            return 0
        if i == 2 or i == 4:        # horizontal
            score = 0
            if self.board[i-1][j-1] != "" and self.board[i-1][j+1] != "" and self.board[i-2][j] != "":
                score += 1
            if self.board[i+1][j-1] != "" and self.board[i+1][j+1] != "" and self.board[i+2][j] != "":
                score += 1
            return score

        if j == 2 or j == 4:        # vertical
            score = 0
            if self.board[i-1][j-1] != "" and self.board[i+1][j-1] != "" and self.board[i][j-2] != "":
                score += 1
            if self.board[i-1][j+1] != "" and self.board[i+1][j+1] != "" and self.board[i][j+2] != "":
                score += 1
            return score

    def check_winner(self):
        """the function checks which side is the winner"""
        if DotsAndBoxesState.score1 > 4:            # Because the total score is fixed at nine, if player's score is greater than four,
                                                    # then the player is the winner.
            return "A"
        else:
            return "B"

    def is_full(self):
        """return True if all spaces have been filled, otherwise False"""
        full = True
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == "":
                    full = False
        return full

    def make_move(self, move):
        """move must be odd numbers between 0 and 48 and correspond to an open board location
           modifies this state as if self.turn made a mark at the location indicated by move"""
        if int(move) < 0 or int(move) > 48 or self.board[int(move) // 7][int(move) % 7] != "" or int(move) % 2 == 0:
            raise ValueError("{} is not a valid move for {}".format(move, self.board))
        DotsAndBoxesState.score1 += self.check_score(move)
        self.board[int(move) // 7][int(move) % 7] = colors[self.turn] + self.turn + "\u001b[0m"
        self.turn = get_opponent(self.turn)               #change into another player's trun


    def get_best_move(self):
        """AI will prioritize the optimal moves"""
        moves1 = self.get_next_moves1()         # moves1 represents all legal moves.
        moves2 = self.get_next_moves2()         # moves2 represents the moves that allow the AI to score a box.
        moves3 = self.get_next_moves3()         # moves3 represents the moves that will allow the player to score a box.


        if len(moves1) == 0:                    # the siuation that there is no legal move
            return self
        if len(moves2) != 0:
            return moves2[len(moves2) // 2]                    # the siuation that there is(are) move(s) to score

        elif len(moves3) != 0:
            return moves3[len(moves3) // 2]                    # the siuation that there is(are) moves(s) to allow the player to score

        else:
            return moves1[len(moves1) // 2]                    # if there is no better moves, the AI will play sequentially, starting from the top left.


    def __repr__(self):
        """instructing how the class DotsAndBoxesState is displayed"""
        r = ""
        for row in self.board:
            for cell in row:
                if cell == "":
                    cell = color_magenta("_")
                r += cell + "   "               # for all the empty strings, we will replace it with an '_'.
            r += "\n"
        return r

def take_turn(state, hint):
    """take a human turn in DotsAndBoxes"""
    """ display the current state and the labels for choosing a move"""

    print(state)                                                                        # print the game board
    print(color_magenta(hint))
    print("")                #add a space                                                                         # print the numbers that correspond to all moves in the game board
    print(color_green("Your current score is: "), color_green(str(state.score1)))
    print(color_green("AI's current score is: "), color_green(str(state.check_finished_boxes() - state.score1)))       # record the scores of the player and AI at the moment
    print("")                #add a space

    move = input(color_yellow("Please enter a number to connect: "))

    """prompt again for a move until it's a valid input and corresponds to an empty space in the board"""
    while not move.isnumeric() or not (0 <= int(move) <= 48) or (int(move) % 2 == 0) or state.board[int(move) // 7][int(move) % 7] != "":
        move = input(color_yellow("Please enter a valid connection: "))
    number = move
    if number in hint:
        index = hint.find(number)
        if len(number) == 1:
            hint = hint[0:index] + " " + hint[index + 1:]                               # Make the moves player already made disappear
        else:
            hint = hint[0:index] + "  " + hint[index + 2:]

    state.make_move(move)
    return hint

def check_two_spots(a, b, c):
    """the function checks whether there has been two moves played in a box"""

    if a != "" and b != "" and c == "":
        return False
    if a != "" and b == "" and c != "":
        return False
    if a == "" and b != "" and c != "":
        return False
    return True

"""the functions that give the string different colors"""

def color_green(str):
    return "\u001b[32;1m" + str + "\u001b[0m"

def color_cyan(str):
    return "\u001b[36;1m" + str + "\u001b[0m"

def color_yellow(str):
    return "\u001b[33;1m" + str + "\u001b[0m"

def color_magenta(str):
    return "\u001b[35;1m" + str + "\u001b[0m"

def play():
    board = [ [".", "", ".", "", ".", "", "."],
            ["", " ", "", " ", "", " ", ""],
            [".", "", ".", "", ".", "", "."],
            ["", " ", "", " ", "", " ", ""],
            [".", "", ".", "", ".", "", "."],
            ["", " ", "", " ", "", " ", ""],
            [".", "", ".", "", ".", "", "."] ]

    hint = ("""    1       3       5
7       9       11      13
    15      17      19
21      23      25      27
    29      31      33
35      37      39      41
    43      45      47""")

# Text description of how to play the game,

    print(" ")
    print("This game is called Dots And Boxes.")
    print("The user plays the first move on any dash lines.")
    print("The user is represented by 'A' and computer by 'B'.")
    print("Enter the corresponding numbers below to make your move.")

    print("")
    print("HINT")
    print("For any box, the one who fills the last empty dash will score that box.")
    print("So, you should try to fill the last empty dash of any box.")
    print("")


    root = DotsAndBoxesState(board, "A")    # before each side makes a move
    while not root.is_full():
        hint = take_turn(root, hint)

        root = root.get_best_move()        # make AI move
    print(root)
    print(color_green("Your score is: "), color_green(str(DotsAndBoxesState.score1)) )
    print(color_green("AI's score is: ") + color_green(str(9 - DotsAndBoxesState.score1)) )
    print("")                              #add a space

    if root.check_winner() == "A":
        print(color_cyan("You win!"))
        if DotsAndBoxesState.score1 == 5:
            print(color_cyan("But ... You only beat AI by one point..."))

    if root.check_winner() == "B":
        if DotsAndBoxesState.score1 < 4:
            print(color_cyan("Come on! Are you serious? You need to close to AI's score at least!"))
        else:
            print(color_cyan("Sorry, AI beats you! Try harder next time!" + "\u001b[0m"))
    print("")                              #add a space

play()
