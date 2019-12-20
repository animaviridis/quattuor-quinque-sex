import numpy as np

from quatro_piece import Piece
from misc import log_exceptions


class Board(object):
    """Quatro game board.

    The board is of shape 4x4. The board fields are to be populated with the game pieces. No piece can be put on a field
    which is already occupied. Once placed, a piece cannot be moved.
    """

    def __init__(self):
        self._board_state = np.zeros((4, 4), dtype=Piece)

    def __repr__(self):
        b = ''
        sep = ' '.join(4*(6*'-',)) + '\n'

        for i, row in enumerate(self._board_state):
            if i:
                b += sep

            b += ' '
            b += ' | '.join((p.code if p else 4*' ' for p in row))
            b += '\n'

        return f"Game board state: \n{b}"

    @log_exceptions("quattro_board")
    def put_piece(self, piece, pos):
        if not isinstance(pos, tuple):
            raise TypeError(f"'pos' should be a tuple (got {type(pos)})")

        if (len(pos) != 2) or any(map(lambda p: not isinstance(p, int), pos)):
            raise ValueError(f"'pos' should be a 2-tuple of integers")

        if not isinstance(piece, Piece):
            raise TypeError(f"'piece' should be an instance of Piece (got {type(piece)})")

        if self._board_state[pos]:
            raise RuntimeError(f"Board position {pos} is already occupied")

        self._board_state[pos] = piece
        piece.position = pos


if __name__ == '__main__':
    board = Board()
    board.put_piece(Piece(0, 1, 0, 0), (2, 3))
    board.put_piece(Piece(1, 1, 0, 1), (1, 0))
    print(board)
