import pygame
import sys
import openai
from const import *
from game import Game
from square import Square
from move import Move
from AI import AI

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.AI = AI('black')

        # Configurar OpenAI
        openai.api_key = "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"
        self.chatgpt_model = "gpt-3.5-turbo-0125"

    def get_ai_move(self, player_move, previous_move):
        # Enviar la posición del jugador y el movimiento anterior al modelo ChatGPT para obtener el mejor movimiento para la IA
        response = openai.ChatCompletion.create(
            model=self.chatgpt_model,
            messages=[
                {"role": "user", "content": f"Jugador 1 movió {player_move}. Jugador 2 movió {previous_move}. ¿Cuál es tu próximo movimiento?"}
            ],
            temperature=0.5,
            max_tokens=50
        )
        ai_move = response.choices[0].message['content'].strip()
        return ai_move

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        previous_move = ""

        while True:
            # Mostrar métodos
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()

                            # obtener el movimiento de la IA basado en el movimiento del jugador anterior
                            ai_move = self.get_ai_move((str(dragger.initial_row + 1) + chr(dragger.initial_col + ord('a')), str(released_row + 1) + chr(released_col + ord('a'))), previous_move)
                            print("Movimiento de la IA:", ai_move)
                            # Aplicar el movimiento de la IA al tablero
                            if "->" in ai_move:
                                ai_initial_row = int(ai_move[0]) - 1  # Convertir de 1-8 a 0-7
                                ai_initial_col = ord(ai_move[1]) - ord('a')  # Convertir de 'a'-'h' a 0-7
                                ai_final_row = int(ai_move[3]) - 1  # Convertir de 1-8 a 0-7
                                ai_final_col = ord(ai_move[4]) - ord('a')  # Convertir de 'a'-'h' a 0-7
                                
                                ai_initial = Square(ai_initial_row, ai_initial_col)
                                ai_final = Square(ai_final_row, ai_final_col)

                                ai_move_obj = Move(ai_initial, ai_final)

                                # Verificar si la pieza seleccionada por la IA es válida
                                if board.squares[ai_initial_row][ai_initial_col].has_piece():
                                    piece = board.squares[ai_initial_row][ai_initial_col].piece
                                    # Verificar si el movimiento es válido para la pieza seleccionada
                                    if board.valid_move(piece, ai_move_obj):
                                        # Realizar el movimiento de la IA
                                        captured = board.squares[ai_final_row][ai_final_col].has_piece()
                                        board.move(piece, ai_move_obj)
                                        board.set_true_en_passant(piece)

                                        # Mostrar métodos
                                        game.show_bg(screen)
                                        game.show_last_move(screen)
                                        game.show_pieces(screen)
                                        # Siguiente turno
                                        game.next_turn()
                                        
                                        print("Movimiento de la IA aplicado correctamente.")
                                        previous_move = ai_move  # Actualizar el movimiento anterior
                                    else:
                                        print("Movimiento de la IA no válido.")
                                else:
                                    print("Movimiento de la IA no válido.")

                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = Game()
                        board = game.board
                        dragger = game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()
