from board import Board


class TicTacToeManager:
    def __init__(self, board: Board = Board(3), pieces_to_win: int = None):
        if not pieces_to_win:
            pieces_to_win = board.size
        self.board: Board = board
        self.crosses: list[int] = []
        self.noughts: list[int] = []
        self.turn: int = 1  # 1 - cross, -1 - nought
        self.pieces_to_win: int = pieces_to_win

    def reset_board(self):
        self.board.create_board()

    def make_move(self, cell: int):
        if self.turn == 1:
            self.crosses.append(cell)
        else:
            self.noughts.append(cell)
        self.board.board[cell] = self.turn
        self.turn *= -1

    def unmake_move(self, cell: int):
        if self.turn == -1:
            self.crosses.remove(cell)
        else:
            self.noughts.remove(cell)
        self.board.board[cell] = 0
        self.turn *= -1

    def find_legal_moves(self):
        legal_moves: list[int] = []
        for i, cell in enumerate(self.board.board):
            if cell == 0:
                legal_moves.append(i)

        return legal_moves

    def check_win(self):
        turn_list: list[int] = self.crosses if self.turn == -1 else self.noughts
        for cell in turn_list:
            finished = self.check_win_at_cell(cell)
            if finished:
                return finished
        return 0

    def check_win_at_cell(self, cell: int):
        size: int = self.board.size
        directions = ((-1, -1), (0, -1), (1, -1),
                      (-1, 0),           (1, 0),
                      (-1, 1),  (0, 1),  (1, 1))

        cell_content: int = self.board.board[cell]
        for direction in directions:
            next_cell: int = cell
            for i in range(1, self.pieces_to_win):

                if not self.check_borders(next_cell, direction):
                    break

                next_cell = cell + (direction[0] + direction[1] * size) * i

                next_cell_content: int = self.board.board[next_cell]

                if next_cell_content != cell_content:
                    break
            else:
                return 1
        return 0

    def check_borders(self, cell: int, direction: tuple[int, int]) -> bool:
        x, y = cell % self.board.size, cell // self.board.size
        return 0 <= x + direction[0] < self.board.size and 0 <= y + direction[1] < self.board.size


class Adversary:
    def __init__(self, manager):
        self.manager = manager

    def search(self, depth: int, alpha=float('-infinity'), beta=float('+infinity')):
        if depth == 0:
            return 0

        win = self.manager.check_win()
        if win:
            return win + depth

        available_moves = self.manager.find_legal_moves()

        if not available_moves:
            return 0

        for cell in available_moves:
            self.manager.make_move(cell)

            evaluation = -self.search(depth - 1, -beta, -alpha)

            self.manager.unmake_move(cell)

            if evaluation >= beta:
                return beta

            if evaluation > alpha:
                alpha = evaluation

        return alpha

    def search_root(self, depth):
        moves: list[int] = self.manager.find_legal_moves()
        best_eval = float('-infinity')
        best_move = None

        for move in moves:
            self.manager.make_move(move)

            evaluation = self.search(depth - 1)

            self.manager.unmake_move(move)

            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move
        return best_move