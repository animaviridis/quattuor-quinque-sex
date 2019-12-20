import numpy as np

from piece import Piece


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


if __name__ == '__main__':
    board = Board()
    print(board)
