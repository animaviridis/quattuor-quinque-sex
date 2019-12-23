import random
import re
from time import sleep

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

        self._pos_pattern = r'\[(?P<x>\d),\s*(?P<y>\d)\]'

    def get_coordinates(self):
        def parse_input():
            sleep(0.1)
            pos_str = input("Enter coordinates: ")
            m = re.match(self._pos_pattern, pos_str)
            return tuple(map(lambda i: int(i), m.groupdict().values())) if m else m

        @log_exceptions('quatro_player')
        def check_pos(pos):
            return self._board.check_field(pos)

        valid = False
        xy = ()
        while not valid:
            xy = parse_input()
            while xy is None:
                print(f"Invalid coordinates format. "
                      f"Please use the following regex pattern: {self._pos_pattern} (e.g. [2, 3])")
                xy = parse_input()
            valid = check_pos(xy)

        return xy

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
    player.get_coordinates()

