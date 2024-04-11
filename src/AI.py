import copy
from const import ROWS, COLS
from piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King

class AI:

    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        # Obtener todos los movimientos posibles para la IA
        all_moves = self.get_all_moves(board)

        # Evaluar cada movimiento y seleccionar el mejor
        best_move = None
        best_score = float('-inf')
        for move in all_moves:
            # Realizar el movimiento en una copia del tablero para evaluarlo
            temp_board = copy.deepcopy(board)
            temp_board.move(move.piece, move)
            
            # Calcular la puntuación del movimiento
            score = self.evaluate_position(temp_board)

            # Actualizar el mejor movimiento si es necesario
            if score > best_score:
                best_move = move
                best_score = score

        # Realizar el mejor movimiento
        if best_move:
            board.move(best_move.piece, best_move)

    def get_all_moves(self, board):
        # Obtener todos los movimientos posibles para las piezas de la IA en el tablero
        all_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_piece() and square.piece.color == self.color:
                    moves = square.piece.get_moves(board)
                    all_moves.extend(moves)
        return all_moves

    def evaluate_position(self, board):
        """
        Evaluates the current position on the board and assigns a score.
        
        This method should consider various factors such as piece values, king safety,
        pawn structure, control of the center, development, and other strategic elements.

        Returns:
            float: The evaluation score for the current position.
        """
        score = 0

        # Example factors to consider:

        # Piece values
        piece_values = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 0,  # The king's value might be irrelevant for the evaluation
        }

        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    # Add or subtract the piece value based on color
                    if piece.color == self.color:
                        score += piece_values[type(piece)]
                    else:
                        score -= piece_values[type(piece)]

        # Other factors could be considered here, such as pawn structure, control of the center, etc.

        return score
