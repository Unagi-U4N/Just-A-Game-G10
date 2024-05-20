import math, copy, sys, pygame
from utils import *

X = "X"
O = "O"
EMPTY = None
operations = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if board == initial_state():
        # print("X's turn")
        return X
    else:

        # Count the number of X and O on the board
        x_count = 0
        o_count = 0
        for row in board:
            for cell in row:
                if cell == X:
                    x_count += 1
                elif cell == O:
                    o_count += 1
        
        # Logic that x always goes first, hence x value is always greater than o
        if x_count > o_count:
            # print("O's turn")
            return O
        else:
            # print("X's turn")
            return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Iterate through the board and find all the empty cells
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    try:
        i, j = action

        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
            raise IndexError("Invalid move: Index out of range")

        if board[i][j] != EMPTY:
            raise ValueError("Invalid move: Cell already taken")

        # using deepcopy to make a copy of the board (DO NOT USE shallow copy due to 2 dimensional list)
        newboard = copy.deepcopy(board)
        newboard[i][j] = player(board)

    except Exception as e:
        raise e

    return newboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows of 3
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
        
    # Check columns of 3
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
            
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    # If no winner
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or not any(EMPTY in sublist for sublist in board):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    In this case X is the max, trying to get as high as possible, O is the min, trying to get as low as possible
    """

    if winner(board) == X:
        # print(type(1))
        return int(1)
    elif winner(board) == O:
        # print(type(-1))
        return int(-1)
    else:
        # print(type(0))
        return int(0)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Define the max and min functions, both functions will call each other recursively
    # Alpha = max value, Beta = min value
    # https://www.youtube.com/watch?v=SLgZhpDsrfc
    
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            global operations
            operations += 1

            # Call the min function, and find the maximum value as v
            v = max(v, min_value(result(board, action), alpha, beta))

            # Compare the value of v with alpha(maximum value from previous branch), and update alpha if v is greater
            alpha = max(alpha, v)

            # If alpha is greater than or equal to beta(minimum value from previous branch), break the loop, stop searching the down the branch
            if alpha >= beta:
                break
        return v

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            global operations
            operations += 1
            # Call the max function, and find the minimum value as v
            v = min(v, max_value(result(board, action), alpha, beta))

            # Compare the value of v with beta(minimum value from previous branch), and update beta if v is smaller
            beta = min(beta, v)

            # If alpha is greater than or equal to beta(minimum value from previous branch), break the loop, stop searching the down the branch
            if alpha >= beta:
                break
        return v

    if terminal(board):
        return None

    else:


        choice = []
        alpha = -math.inf
        beta = math.inf

        # If the board is not in initial state, use the minimax algorithm to find the best move
        if player(board) == X:
            val = []
            action = []
            for act in actions(board):
                val.append(max_value(result(board, act), alpha, beta))
                action.append(act)
            choice.append(action[val.index(max(val))])
            
        
        # If the board is not in initial state, use the minimax algorithm to find the best move
        elif player(board) == O:
            val = []
            action = []
            for act in actions(board):
                val.append(min_value(result(board, act), alpha, beta))
                action.append(act)
            choice.append(action[val.index(min(val))])
        global operations
        # print("Total operations: ", operations)
        operations = 0
        return choice[0]
    
#--------------------------------------------------------------------#

class TicTacToe:
    def __init__(self, game):
        self.font1 = pygame.font.Font("data/monogram.ttf", 70)
        self.font2 = pygame.font.Font("data/monogram.ttf", 40)
        self.playername = game.player.name
        self.board = initial_state()
        self.state = "1"
        self.timer = 0
        self.place = [1, 1]
        self.choice = 0
        self.game = game
        self.user = None
        self.display = game.display
        self.ai_turn = False
        self.winner = None
        self.tile = [[(521, 282),(602, 282),(678, 282)],
                     [(521, 355),(602, 355),(678, 355)],
                     [(521, 438),(602, 438),(678, 438)]]
        self.title = ""

    def getplayer(self):

        if self.user is None:
            if self.state == "1":
                self.display.blit(self.game.assets["ttt1"], (0, 0))
            
            elif self.state == "2":
                self.display.blit(self.game.assets["ttt2"], (0, 0))
                if self.choice == 0:
                    render_img(self.game.assets["X"], 500, 350, self.display, True)
                    render_img(self.game.assets["O"], 700, 350, self.display, True, transparency=150)
                elif self.choice == 1:
                    render_img(self.game.assets["O"], 700, 350, self.display, True)
                    render_img(self.game.assets["X"], 500, 350, self.display, True, transparency=150)

        if self.user is not None and self.timer < 100 and self.state != "3":
            self.display.blit(self.game.assets["ttt2"], (0, 0))
            render_img(self.game.assets[self.user], 600, 350, self.display, True)
            render_text(self.user + " chosen", self.game.font, "black", 600, 450, self.display, True)
            self.timer += 1
        elif self.user is not None:
            self.state = "3"
            return self.play()

    def play(self):
        self.display.blit(self.game.assets["ttt3"], (0, 0))
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != EMPTY:
                    render_text(self.board[i][j], self.font1, "black", self.tile[i][j][0], self.tile[i][j][1], self.display, True)
        
        game_over = terminal(self.board)
        player_ = player(self.board)

        # If game over
        if game_over:
            self.timer += 1
            if self.timer < 200:
                self.winner = winner(self.board)
                if self.winner is None:
                    self.title = "It's a tie!"
                else:
                    self.title = f"{self.winner} wins!"
            elif self.timer >= 200:
                if self.winner == self.user and self.winner is not None:
                    return "Win"
                elif self.winner != self.user and self.winner is not None:
                    return "Lose"
                else:
                    return "Draw"
                
        elif self.user == player_:
            self.title = f"{self.user}'s turn"
        else:
            self.title = "Computer thinking..."
        render_text(self.title, self.game.font, "black", 600, 500, self.display, True)

        # Check for AI move
        if self.user != player_ and not game_over:
            if self.ai_turn:
                self.board = result(self.board, minimax(self.board))
                self.ai_turn = False
            else:
                self.ai_turn = True

        # Check for user move, allow player to navigate using arrow keys and press space to choose
        x = self.place[0]
        y = self.place[1]
        if self.user == player_ and not game_over:
            render_text(self.user, self.font1, "black", self.tile[x][y][0], self.tile[x][y][1], self.display, True, transparency=150)
            if self.board[x][y] != EMPTY:
                render_text("Choose another tile", self.game.font, "red", 600, 230, self.display, True)

    def run(self):
        img=pygame.Surface((1200, 675))
        img.fill((0,0,0))
        img.set_alpha(150)
        self.display.blit(img, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "1":
                        self.state = "2"
                    elif self.state == "2":
                        if self.choice == 0:
                            self.user = X
                        elif self.choice == 1:
                            self.user = O
                    elif self.state == "3":
                        if self.board[self.place[0]][self.place[1]] == EMPTY:
                            self.board = result(self.board, (self.place[0], self.place[1]))
                            self.place = [1, 1]
                if event.key == pygame.K_LEFT and self.state == "2":
                    self.choice = (self.choice + 1) % 2
                if event.key == pygame.K_RIGHT and self.state == "2":
                    self.choice = (self.choice - 1) % 2
                if event.key == pygame.K_UP or event.key == pygame.K_w and self.state == "3":
                    self.place[0] = (self.place[0] - 1) % 3
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and self.state == "3":
                    self.place[0] = (self.place[0] + 1) % 3
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and self.state == "3":
                    self.place[1] = (self.place[1] - 1) % 3
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and self.state == "3":
                    self.place[1] = (self.place[1] + 1) % 3

        return self.getplayer()        
