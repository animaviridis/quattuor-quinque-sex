import random
import re
from time import sleep
from typing import Tuple, Union

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
        self._piece_pattern = r'[A-Z]{4}'

    @property
    def board(self):
        return self._board

    def get_piece_code(self):
        check_piece = log_exceptions('quatro_player')(self._board.check_piece)

        valid = False
        piece_str = ''
        while not valid:
            sleep(0.1)
            piece_str = input("Enter piece code: ")

            if piece_str == '0':
                if self._board.empty:
                    return 0
                else:
                    print("The '0' code is only allowed for the first move (when the board is empty)")
                    continue

            if re.match(self._piece_pattern, piece_str) is None:
                print(f"Invalid piece code format. Please use the following pattern: {self._piece_pattern}")
                continue

            valid = check_piece(piece_str)

        return piece_str

    def get_coordinates(self) -> Tuple[int, int]:
        def parse_input() -> Union[Tuple[int, int], None]:
            sleep(0.1)
            pos_str = input("Enter coordinates: ")
            m = re.match(self._pos_pattern, pos_str)
            return tuple(map(lambda i: int(i), m.groupdict().values())) if m else m

        check_pos = log_exceptions('quatro_player')(self._board.check_field)

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
    position = player.get_coordinates()
    piece = player.get_piece_code()
    if piece:
        player.board.put_piece(piece, position)
    player.get_piece_code()

