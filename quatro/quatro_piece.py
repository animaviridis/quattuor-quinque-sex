from enum import Enum, unique
from itertools import product


@unique
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

    @classmethod
    def get_member(cls, value):
        ms = [m for m in cls if m.value == value]
        if not ms:
            raise ValueError(f"No member with value {value}")
        return ms[0]

    @classmethod
    def get_all_values(cls):
        return [m.value for m in cls]


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

    PROP_TEMPLATES = (
        PieceProperty('Height', ['Short', 'Tall']),
        PieceProperty('Color', ['Blue', 'Red']),
        PieceProperty('Shape', ['Square', 'Circular']),
        PieceProperty('Fill', ['Hollow', 'Solid'])
    )

    def __init__(self, *props):
        if len(props) != 4:
            raise TypeError(f"__init__ takes {len(self.PROP_TEMPLATES)} positional arguments ({len(props)} were given)")

        self._value = props
        self._properties = tuple((pt.get_member(props[i]) for i, pt in enumerate(self.PROP_TEMPLATES)))
        self._code = ''.join((p.code for p in self._properties))

        self.position = None

    def __repr__(self):
        t = 'taken' if self.taken else 'available'
        return f"Piece '{self.code}' ('{self.value_code}') - {', '.join((p.name for p in self.properties))} ({t})"

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return ''.join((str(v) for v in self.value))

    @property
    def properties(self):
        return self._properties

    @property
    def code(self):
        return self._code

    @property
    def taken(self):
        return self.position is not None

    @staticmethod
    def generate_pieces():
        possible_values = (pt.get_all_values() for pt in Piece.PROP_TEMPLATES)
        all_pieces = [Piece(*value) for value in product(*possible_values)]
        return {piece.code: piece for piece in all_pieces}


if __name__ == '__main__':
    color = PieceProperty('Color', ['Blue', 'Red'])

    a_piece = Piece(0, 1, 0, 0)
    print(a_piece)

    pieces = Piece.generate_pieces()
