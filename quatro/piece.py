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
