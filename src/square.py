import re

class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    def set_piece(self, piece):
        self.piece = piece

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(col):
        return Square.ALPHACOLS[col]
    
    @staticmethod
    def from_notation(notation):
        """
        Convierte la notación de un movimiento en un objeto Square.
        La notación debe ser una cadena en formato "(fila, columna)", por ejemplo, "(5, 4)".
        """
        try:
            # Extraer la notación del movimiento de la cadena completa
            match = re.search(r'\((\d+,\s*\d+)\)', notation)
            if not match:
                raise ValueError("La notación no está en el formato esperado.")

            # Obtener la notación del movimiento
            move_notation = match.group(1)

            # Extraer las coordenadas de fila y columna de la notación del movimiento
            row, col = map(int, move_notation.split(','))

        except ValueError:
            raise ValueError(f"La notación '{notation}' no está en el formato esperado.")

        # Convertir las coordenadas en objetos Square
        return Square(row, col)
