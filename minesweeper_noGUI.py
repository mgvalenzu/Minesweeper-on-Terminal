# Author: Martin Gabriel Gastelum-Valenzuela
import random

class Game():
    """Operational aspects of the game"""

    def __init__(self, state = "PLAY", difficulty = "NONE"):
        """Initialize Game"""
        self.state = state
        self.difficulty = difficulty

    def get_difficulty(self):
        """returns the games difficulty"""
        return self.difficulty

    def set_difficulty(self):
        """Prompt user to select game difficulty - Easy, Medium, or Hard"""
        self.difficulty = input("Select difficulty:\nEASY -- MEDIUM\n").upper()

        return self.difficulty

    def display_prompt(self):
        """Display start instructions"""
        print(
            "\nWelcome to Minesweeper!\n"
            "Please select tiles you wish to uncover by entering their x,y coordinates.\n"
            "Start with number, followed by a letter (Example: 4C)\n\n"
            "Win the game by uncovering every non-mine tile\n"
            "Enter 'solved' into the command line to be given the solved game board"
            "\n")

        return

    def get_state(self):
        """Returns the current game state"""
        return self.state

    def set_state(self, new_state):
        """Modify game state('PLAY', FINISH)"""
        self.state = new_state.upper()

        return

    def check_state(self, contents):
        """Check if user chosen tile contained game ending contents."""
        if contents == "*":
            self.state = "LOST"
            self.game_over()

        return self.state

    def game_over(self):
        """When the user has failed the game, display game over message"""
        print("You have struck a mine! Game Over!")

        return

    def prompt_input(self):
        """Prompts user for tile selection"""
        print("Select tile: ", end = "")
        return

    def user_input(self):
        """Obtains users input to 'click on cell. Validating the input."""
        is_valid = False
        user_tile = input()

        # validate input
        while is_valid != True:
            if len(user_tile) == 3: # Case when 10th+ row is chosen
                if ord(user_tile[2].upper()) in range(65, 81):    # Valid case - input is 10 and char from A-J
                    tile = [str(user_tile[0] + user_tile[1]), str(user_tile[2]).upper()]
                    is_valid = True
            elif len(user_tile) == 2:   # case when 1-9 rows are chosen
                if int(user_tile[0]) in range(1, 10) and ord(user_tile[1].upper()) in range(65, 75): # 2 character tiles with valid inputs
                    tile = user_tile.upper()
                    is_valid = True
            elif user_tile.upper() == "SOLVED" or user_tile.upper() == "FINISH":    # 'Cheat' used or user is submitting their final solution
                return user_tile.upper()
            else:
                print("That is not a valid tile on this board\nPlease try again\n")
                user_tile = input()

        return tile

    # For Course assignment
    # def soln_verification(self,user_soln, board):
    #     """Algorithm used to check if the users solution is valid"""
    #     board = board.get_board()
    #     ending_tiles = []
    #     # Obtain all game ending tiles
    #     verified = False # initialize verification, must prove is a correct answer
    #     for row_i in range(10):
    #         for col_j in range(10):
    #             if board[row_i][col_j].is_open() and board[row_i][col_j].get_contents() == "*": # if any open tiles on baord are also mines
    #                 return verified
    #             elif not board[row_i][col_j].is_open() and board[row_i][col_j].get_contents() != "*": # there is unopened correct step of solution
    #                 return verified
    #     verified = True # Successful complete iteration through board
    #
    #     return verified


class Board():
    """Representing the game board"""

    def __init__(self, board = []):
        """Initialize game board"""
        self.board = board

    def get_board(self):
        """Retreive game board"""

        return self.board

    def get_range(self):
        """Returns the row and column index max range, dependent on chosen difficulty"""

        difficulty = game.get_difficulty()
        if difficulty == "EASY":
            row = 10
            col = 10
        elif difficulty == "MEDIUM":
            row = 16
            col = 16

        return (row,col)

    def display_board(self):
        """Displays Board representation in 2d matrix"""
        col_count = 0
        row_letter = 65

        for row in self.get_board():
            col_count += 1
            space = ""
            if col_count < 10:
                space = " "
            print(str(col_count) + space, end = "")
            for col in row:
                print("" + col.get_display() , end = "")
            print("")

        while col_count != 0:
            print("    " + chr(row_letter), end = "")
            row_letter += 1
            col_count -= 1
        print("")

        return

    def display_under_board(self):
        """Displays everything beneath the tiles, for testing purposes"""
        col_count = 0
        row_letter = 65 # ASCII letter

        # Iterate through 2d array
        for row in self.get_board():
            col_count += 1
            for col in row:
                contents = str(col.get_contents())
                if contents == "0": # Display empty cells as empty
                    contents = " "
                print(" " + contents, end="")   # display contents of cell
            print("")

        return

    def generate_rand_mines(self, data_tupl):
        """Generate randon indices for placing mines - allows for game to make random board each instance, not necessary as it turns out"""

        rand_mines = [[] for y in range(int(data_tupl[2]))] # Initilaize nested array to store values
        mine_count = int(data_tupl[2])     # number of mines
        arr_index = 0       # Index tracker for rand_mines array

        #Randomize indicies
        while mine_count != 0:
            mine = []
            rand_row = random.randint(0, int(data_tupl[0]) - 1)
            rand_col = random.randint(0, int(data_tupl[1]) - 1)
            # add to particular mine
            mine.append(rand_row)
            mine.append(rand_col)
            # Store mine location
            if mine not in rand_mines:
                rand_mines[arr_index] = mine
                mine_count -= 1
                arr_index += 1  # next element in storage
            else:   # Prevent chance of duplicate mine locations
                continue

        return rand_mines

    def generate_board(self, board_data):
        """Creates a M x N board representing the minesweeper board, fills in the board with Tile objects."""
        for row in range(int(board_data[0])):
            col = []
            for column in range(int(board_data[1])):
                tile = Tile()   # single tile
                col.append(tile)
            self.board.append(col)

        return self.board

    def place_elements(self, rand_mines):
        """Initializes mines and numbers on board"""
        # Place mines
        for mine in rand_mines:
            self.board[mine[0]][mine[1]].set_contents("*")

            # Obtain adjacent tile indices relative to mine - stored as 2 element array
            up_tile = [mine[0] - 1, mine[1]]
            down_tile = [mine[0] + 1, mine[1]]
            right_tile = [mine[0], mine[1] + 1]
            left_tile = [mine[0], mine[1] - 1]
            # Diagonals
            up_right_tile = [mine[0] - 1, mine[1] + 1]
            up_left_tile = [mine[0] - 1, mine[1] - 1]
            down_right_tile = [mine[0] + 1, mine[1] + 1]
            down_left_tile = [mine[0] + 1, mine[1] - 1]

            # Place/update number in adjacent tile
            # Validate indices - ensuring out of bounds indices are disregarded

            ranges = board.get_range()  # obtain row/col index ranges
            row_limit = ranges[0]
            col_limit = ranges[1]

            #Above
            if up_tile[0] in range(0,row_limit) and up_tile[1] in range(0,col_limit):
                curr_contents = self.board[up_tile[0]][up_tile[1]].get_contents()       # obtain current tile relative to mine
                if curr_contents != "*":    # Adjacent tile isnt a mine
                    self.board[up_tile[0]][up_tile[1]].set_contents(int(curr_contents) + 1)    # increment value of adj mines

            #Below - Derrivation of Above
            if down_tile[0] in range(0,row_limit) and down_tile[1] in range(0,col_limit):
                curr_contents = self.board[down_tile[0]][down_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[down_tile[0]][down_tile[1]].set_contents(int(curr_contents) + 1)

            #Right
            if right_tile[0] in range(0,row_limit) and right_tile[1] in range(0,col_limit):
                curr_contents = self.board[right_tile[0]][right_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[right_tile[0]][right_tile[1]].set_contents(int(curr_contents) + 1)

            #Left
            if left_tile[0] in range(0,row_limit) and left_tile[1] in range(0,col_limit):
                curr_contents = self.board[left_tile[0]][left_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[left_tile[0]][left_tile[1]].set_contents(int(curr_contents) + 1)

            # Diagonals
            # Upper-Right
            if up_right_tile[0] in range(0,row_limit) and up_right_tile[1] in range(0,col_limit):
                curr_contents = self.board[up_right_tile[0]][up_right_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[up_right_tile[0]][up_right_tile[1]].set_contents(int(curr_contents) + 1)

            # Upper-Left
            if up_left_tile[0] in range(0, row_limit) and up_left_tile[1] in range(0, col_limit):
                curr_contents = self.board[up_left_tile[0]][up_left_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[up_left_tile[0]][up_left_tile[1]].set_contents(int(curr_contents) + 1)

            # Lower-Right
            if down_right_tile[0] in range(0, row_limit) and down_right_tile[1] in range(0, col_limit):
                curr_contents = self.board[down_right_tile[0]][down_right_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[down_right_tile[0]][down_right_tile[1]].set_contents(int(curr_contents) + 1)

            # Lower-Left
            if down_left_tile[0] in range(0, row_limit) and down_left_tile[1] in range(0, col_limit):
                curr_contents = self.board[down_left_tile[0]][down_left_tile[1]].get_contents()
                if curr_contents != "*":
                    self.board[down_left_tile[0]][down_left_tile[1]].set_contents(int(curr_contents) + 1)

        return

    def open_tile(self, tile):
        """Uncovers a board tile to expose contents of tile"""
        if type(tile[0]) == str:   # Extract indices
            row_i = int(tile[0]) - 1
            col_i = ord(tile[1]) - 65
        else:       # for recursive calls - when tile is already array of indices
            row_i = int(tile[0])
            col_i = int(tile[1])

        # Uncover tile
        tile_obj = self.board[row_i][col_i]
        tile_obj.set_display()

        # For cases when tile is empty need to open all adjacent tiles that empty as well - per minesweeper rules
        if tile_obj.get_contents() == 0:
            surround_tiles = [[row_i - 1, col_i - 1], [row_i - 1, col_i],[row_i - 1, col_i + 1],[row_i + 1, col_i - 1], [row_i, col_i - 1],
                              [row_i, col_i + 1], [row_i + 1, col_i], [row_i + 1, col_i + 1]]

            # Visit each adjacent tiles
            ranges = board.get_range()  # Obtain index ranges(stored as tuple)
            row_limit = ranges[0]
            col_limit = ranges[1]
            for adj in surround_tiles:
                if adj[0] in range(0,row_limit) and adj[1] in range(0,col_limit):   # if adjacent tiles are in board boundaries
                    if self.board[adj[0]][adj[1]].is_open():   # Prevent infinite recursion - does not revisit already opened tiles
                        continue
                    else:
                        self.open_tile(adj) # recursively expand outwards and open other empty adj tiles
                        continue

        return tile_obj.get_contents()      # Used to check and validate game state


class Tile():
    """Representing a single board tile"""

    def __init__(self, contents = 0 , display = '[   ]', open = False ):

        self.contents = contents
        self.display = display
        self.open = open

    def get_display(self):
        """Retreive display representation of tile"""

        return self.display

    def set_display(self):
        """Change display representation on Game board to uncover conents of tile"""
        if self.contents == 0:
            contents = "     "
        else:
            contents = "  " + str(self.contents) + "  "

        self.display = contents
        self.open = True

        return

    def is_open(self):
        """Returns T/F bool, to determine if tile has already been 'clicked' on."""
        if self.open == True:
            return True
        else:
            return False

    def get_contents(self):
        """Retrieve particular tile contents"""

        return self.contents

    def set_contents(self, new_contents):
        """Modify tile contents - for initializing"""

        new_contents = str(new_contents)
        self.contents = new_contents.upper()

        return


if __name__ == "__main__":
    # Initialize game
    game = Game()
    # board_data = (10,10,10)     # Initialized M x N and K dimensions for game board - hard code 10 x 10 for course project

    # Display start game
    game.display_prompt()
    difficulty = game.set_difficulty()
    if difficulty == "EASY":
        board_data = (10,10,10)
    elif difficulty == "MEDIUM":
        board_data = (16,16,40)
    # elif difficulty == "HARD":
    #     board_data = (16,30,99)


    # Create populated game board
    board = Board()
    rand_mines = board.generate_rand_mines(board_data)    # create array of indices storing location of mines
    board.generate_board(board_data)    # board of M x N dimension
    board.place_elements(rand_mines)     # Place mines/numbers on board - randomized

    board.display_board()
    # board.display_under_board() # for testing

    # Begin play
    user_soln = []
    curr_state = game.get_state()


    # game play loop
    while curr_state == "PLAY":
        game.prompt_input()
        user_tile = game.user_input()   # Obtain user chosen tile name


        contents = board.open_tile(user_tile)      # Uncover tile
        print('\n')
        board.display_board()            # Display updated board
        curr_state = game.check_state(contents)      # check/update game state if necessary
        user_soln.append(user_tile) # save user inputs

    # Display solution/verification
    print("Answers: ",end = "")
    print(user_soln)















