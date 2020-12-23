# Name: Josh Nguyen
# Date: 11/30/2020
# Description: This is an implementation of a single player game of Mastermind. The computer will create the color
#              sequence, and the user will attempt to guess it.

from random import randint
from random import shuffle


class WrongFormatError(Exception):
    pass


class MastermindGame:
    """Keeps track of the current game"""

    def __init__(self):
        self.board = {}
        self.turn = 1
        self.solution = []
        self.max_turns = 10
        self.generate_board()
        self.make_solution()

    def __str__(self):
        """Format board for entire board print out"""
        output = ""
        for i in range(1, 11):
            if i < 10:
                output += str(i) + ":  " + str(self.board[i]) + "\n"
            else:
                output += str(i) + ": " + str(self.board[i]) + "\n"
        return output

    def generate_board(self):
        """Generates an empty board"""
        for i in range(1, 11):
            self.board[i] = [0, 0, 0, 0]

    def make_solution(self):
        """Randomly generate solution code"""

        while len(self.solution) != 4:
            num = randint(0, 5)
            if num not in self.solution:
                self.solution.append(num)

    def player_turn(self, player_input):
        """Allow player to make their turn"""
        if player_input.lower() == "q":
            self.exit_game("q")

        attempt = []
        try:
            for char in player_input:
                if char == " ":
                    continue
                else:
                    if 0 <= int(char) < 6:
                        attempt.append(int(char))
                    else:
                        raise WrongFormatError

            if len(attempt) != 4:
                raise WrongFormatError

            self.add_move_to_board(attempt)
            win_condition = self.verify_turn(attempt)
            self.print_up_to()
            self.increment_turn()
            return win_condition
        except:
            print("Wrong format, please try again.")

    def print_up_to(self):
        """Prints the board up to the current term"""

        print("----------------------------\n"
              "     Code Pegs    Key Pegs\n"
              "----------------------------")

        output = ""
        for i in range(1, self.turn+1):
            line = [str(number) for number in self.board[i][0]]
            key = [str(number) for number in self.board[i][1]]
            if i < 10:
                output += str(i) + ":  | " + " ".join(line) + " |  | " + " ".join(key) + " |\n"
            else:
                output += str(i) + ": | " + " ".join(line) + " |  | " + " ".join(key) + " |\n"
        print(output)

    def add_move_to_board(self, move):
        """Adds the move to self.board"""
        self.board[self.turn] = move

    def verify_turn(self, move):
        """Checks the player inputs against solution"""
        key_pegs = ["_", "_", "_", "_"]
        solution_copy = list(self.solution)
        pos = 0
        for code in move:
            if code in solution_copy:
                if move.index(code) == self.solution.index(code):
                    key_pegs[pos] = "B"
                else:
                    key_pegs[pos] = "W"
                pos += 1
                solution_copy.remove(code)

        shuffle(key_pegs)  # randomize key peg positions
        self.board[self.turn] = self.board[self.turn], key_pegs
        if key_pegs == ["B", "B", "B", "B"]:
            return True
        else:
            return False

    def increment_turn(self):
        """Increments the turn"""
        self.turn += 1

    def exit_game(self, result):
        """Exits the game by ending program"""
        solution = [str(num) for num in self.solution]

        if result == "w":
            print("""WINNER WINNER CHICKEN DINNER!!
Solution Code: """ + " ".join(solution))
        elif result == "l":
            print("""Out of turns. YOU LOSE.
Solution Code: """ + " ".join(solution))
        print("Thanks for playing!")
        quit()


game = MastermindGame()  # initialize game

# print(game.solution, "\n")
print("""Welcome to the game of Mastermind!
-----------------------------------

             RULES
----------------------------------
Numbers 0 through 5 represent the possible code pegs.
B = a black peg, indicates a peg is the right number and right position
W = a white peg, indicates a peg is the right number in the wrong position
Key peg positions do not correlate to the code peg positions.
To play, enter your guess in the format: 1 2 3 4
The solution will not have any blank spots or duplicates.
The max amount of turns is 10 before you lose.
To quit game, type q.\n""")

# Runs turns
while game.turn < game.max_turns+1:
    print("[Turn " + str(game.turn ) + "] Enter guess:")
    guess = input()
    if game.player_turn(guess):
        game.exit_game("w")

# if out of turns, call loss
game.exit_game("l")
