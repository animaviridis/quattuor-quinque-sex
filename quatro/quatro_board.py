import numpy as np
from typing import Tuple
import copy

from quatro.quatro_piece import Piece


class Board(object):
    """Quatro game board.

    The board is of shape 4x4. The board fields are to be populated with the game pieces. No piece can be put on a field
    which is already occupied. Once placed, a piece cannot be moved.
    """

    N = 4
    PIECES = Piece.generate_pieces()

    def __init__(self):
        self._board_state = np.zeros(2*(self.N,), dtype=Piece)
        self._points = np.zeros(3*(self.N,), dtype=int)
        self._piece_codes_available = set(self.PIECES.keys())
        self._piece_codes_taken = set()

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

    @property
    def pieces_available(self):
        return {code: self.PIECES[code] for code in self._piece_codes_available}

    @property
    def pieces_taken(self):
        return {code: self.PIECES[code] for code in self._piece_codes_taken}

    @property
    def piece_codes_available(self):
        return self._piece_codes_available

    @property
    def piece_codes_taken(self):
        return self._piece_codes_taken

    @property
    def piece_codes(self):
        return set(self.PIECES.keys())

    @property
    def piece_values_available(self):
        pieces = self.PIECES
        return {pieces[code].value for code in self._piece_codes_available}

    @property
    def board_state(self):
        """Current state of the board (array of piece objects and zeros where there is no piece)"""

        return self._board_state

    @property
    def board_fields_taken_state(self):
        """State of the board fields (boolean array: True if a field is taken, False otherwise)"""

        return self._board_state != 0

    @property
    def board_fields_available(self):
        """List of coordinates (2-tuples of ints) of available (not yet taken) fields of the board."""

        return list(zip(*np.where(np.invert(self.board_fields_taken_state))))

    @property
    def empty(self) -> bool:
        """Returns True if the board is empty (no fields occupied), False otherwise"""

        return not self.board_fields_taken_state.any()

    @property
    def full(self) -> bool:
        return self.board_fields_taken_state.all()

    def check_piece(self, piece_code):
        if piece_code in self._piece_codes_taken:
            raise RuntimeError(f"Piece {piece_code} has already been taken. Pick from: {self._piece_codes_available}")

        if piece_code not in self._piece_codes_available:
            raise RuntimeError(f"'{piece_code}' is not a valid piece code. Pick from: {self._piece_codes_available}")

        return True

    def check_field(self, pos):
        if self.full:
            raise RuntimeError(f"The board is already full")

        if not isinstance(pos, tuple):
            raise TypeError(f"'pos' should be a tuple (got {type(pos)})")

        if (len(pos) != 2) or any(map(lambda p: not isinstance(p, (int, np.integer)), pos)):
            raise ValueError(f"'pos' should be a 2-tuple of integers")

        if self._board_state[pos]:
            raise RuntimeError(f"Board position {pos} is already occupied")

        return True

    def put_piece(self, piece_code: str, pos: Tuple[int, int]):
        self.check_field(pos)
        self.check_piece(piece_code)

        piece = self.PIECES[piece_code]
        self._board_state[pos] = piece
        self._points[pos] = piece.points
        self._piece_codes_available.remove(piece_code)
        self._piece_codes_taken.add(piece_code)
        piece.position = pos

    @property
    def points(self):
        return self._points

    def get_scores(self):
        points = self._points

        col_scores = points.sum(axis=0)
        row_scores = points.sum(axis=1)

        d1_score = np.trace(points)
        d2_score = np.flip(points, 0).trace()

        scores = np.concatenate((col_scores, row_scores, [d1_score, d2_score]))
        return np.abs(scores).max(axis=-1)

    def get_max_score(self):
        return self.get_scores().max()

    @property
    def game_completed(self):
        return self.get_max_score() == self.N

    def copy(self):
        return copy.deepcopy(self)

    def probe_piece(self, *args, **kwargs):
        """Create a copy of the current board and put the piece in it. Return the new board."""

        new_board = self.copy()
        new_board.put_piece(*args, **kwargs)
        return new_board


if __name__ == '__main__':
    board = Board()
    board.put_piece('TBCH', (2, 3))
    board.put_piece('SRSS', (1, 0))
    print(board)
    board_copy = board.probe_piece('TRCH', (0, 0))
    print(board_copy)
    print(board)
