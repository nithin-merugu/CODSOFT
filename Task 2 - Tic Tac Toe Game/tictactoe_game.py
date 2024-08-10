import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

def minimax(game, maximizing, alpha, beta):
    if game.current_winner == 'O':
        return 1
    elif game.current_winner == 'X':
        return -1
    elif not game.empty_squares():
        return 0

    if maximizing:
        max_eval = -math.inf
        for move in game.available_moves():
            game.make_move(move, 'O')
            eval = minimax(game, False, alpha, beta)
            game.board[move] = ' '
            game.current_winner = None
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in game.available_moves():
            game.make_move(move, 'X')
            eval = minimax(game, True, alpha, beta)
            game.board[move] = ' '
            game.current_winner = None
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(game):
    best_score = -math.inf
    best_move = None
    for move in game.available_moves():
        game.make_move(move, 'O')
        score = minimax(game, False, -math.inf, math.inf)
        game.board[move] = ' '
        game.current_winner = None
        if score > best_score:
            best_score = score
            best_move = move
    return best_move