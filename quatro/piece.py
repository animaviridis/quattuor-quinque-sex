from enum import Enum


class PieceProperty(int, Enum):
    def __new__(cls, *args):
        value = len(cls.__members__)
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    def __init__(self, *args):
        super().__init__()
        self._code = self.name[0]

    @property
    def code(self):
        return self._code


color = PieceProperty('Color', 'Blue Red')


class Piece(object):
    """Quatro game piece.

    A piece has four binary properties, with values:
        - Short of Tall
        - Blue or Red
        - Square of Circular
        - Hollow or Solid.
    Piece type code is a string of 4 characters - initial letters of the property values.

    There are 16 pieces in the game - unique combinations of the 4 properties.
    """
