import random

from quatro.quatro_board import Board
from misc import log_exceptions


class Player(object):
    """Quatro game player.

    Basic role: takes a string denoting piece type and outputs a position to place it on the board.
    Outputs a piece type string for the opponent and awaits the coordinates the opponent puts the piece at.
    """

    def __init__(self):
        self._board = Board()
        self._pick_piece_method = self._pick_piece_random
        self._pick_field_method = self._pick_field_random

    def pick_piece(self):
        return self._pick_piece_method()

    def _pick_piece_random(self):
        return random.choice(self._board.piece_codes_available)

    def pick_field(self, piece_code):
        return self._pick_field_method(piece_code)

    def _pick_field_random(self, *args):
        return random.choice(self._board.board_fields_available)


if __name__ == '__main__':
    player = Player()
