#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import ai_engine
import chess_engine
import pygame as py
from chess_check_logger import logger
from enums import Player

"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]


# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    """ Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    """
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


def after_move_func(number_of_move: int, current_pieces_on_the_board: str):
    logger.info("After move #" + str(number_of_move+1) + " the pieces on the board are:" + current_pieces_on_the_board)
    return number_of_move + 1


def end_of_game_state_log(number_of_checks: int, number_of_moves_the_knights_made: int, all_whites_together: int,
                          all_blacks_together: int):
    logger.info("The amount of checks that were in the game: " + str(number_of_checks))
    logger.info(
        "The number of moves the knights made: " + str(number_of_moves_the_knights_made))
    logger.info("The number of turns that all the pieces of the white color survived is: " + str(all_whites_together))
    logger.info("The number of turns that all the pieces of the black color survived is: " + str(all_blacks_together))


def main():
    # Check for the number of players and the color of the AI
    logger.info("New game.")
    human_player = ""
    while True:
        try:
            number_of_players = input("How many players (1 or 2)?\n")
            if int(number_of_players) == 1:
                while True:
                    human_player = input("What color do you want to play (w or b)?\n")
                    if human_player in ("w", "b"):
                        if human_player == "w":
                            logger.info("The human player chose the white pieces, The human player is PLAYER_1 and"
                                        " the computer player is PLAYER_2")
                            # Part of the game rules and also based on the chess_engine.get_state() function
                            logger.info("The human player starts the game")
                        else:
                            logger.info("The human player chose the black pieces, The human player is PLAYER_2 and "
                                        "the computer player is PLAYER_1 ")
                        break
                    else:
                        print("Enter w or b.\n")
                break
            elif int(number_of_players) == 2:
                break
            else:
                print("Enter 1 or 2.\n")
        except ValueError:
            print("Enter 1 or 2.")

    # Part of the game rules and also based on the chess_engine.get_state() function
    logger.info("PLAYER_1(with the white pieces) starts the game")

    # Initialize Pygame modules
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False

    ai = ai_engine.chess_ai()
    game_state = chess_engine.game_state()
    number_of_checks = 0
    moves_counter = 0
    logger.info("The pieces on the board are:" + game_state.get_pieces_on_the_board())
    # If the ai player begins this is his first turn
    if human_player == 'b':
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        game_state.move_piece(ai_move[0], ai_move[1], True)
        moves_counter = after_move_func(moves_counter, game_state.get_pieces_on_the_board())

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
                game_over = True
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        # this if is useless right now
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        else:
                            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                  (player_clicks[1][0], player_clicks[1][1]), False)
                            moves_counter = after_move_func(moves_counter, game_state.get_pieces_on_the_board())
                            if human_player == "w":
                                if game_state.check_for_check(game_state.get_current_player_king_location(),
                                                              Player.PLAYER_2)[0]:
                                    number_of_checks += 1
                            elif game_state.check_for_check(game_state.get_current_player_king_location(),
                                                            Player.PLAYER_1)[0]:
                                number_of_checks += 1
                            endgame = game_state.checkmate_stalemate_checker()
                            if endgame != 3:
                                running = False
                                game_over = True
                                break
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                            if human_player == 'w':
                                ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                                moves_counter = after_move_func(moves_counter, game_state.get_pieces_on_the_board())
                                if game_state.check_for_check(game_state.get_current_player_king_location(),
                                                              Player.PLAYER_1)[0]:
                                    number_of_checks += 1
                                endgame = game_state.checkmate_stalemate_checker()
                                if endgame != 3:
                                    running = False
                                    game_over = True
                                    break
                            elif human_player == 'b':
                                ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                                moves_counter = after_move_func(moves_counter, game_state.get_pieces_on_the_board())
                                if game_state.check_for_check(game_state.get_current_player_king_location(),
                                                              Player.PLAYER_2)[0]:
                                    number_of_checks += 1
                                endgame = game_state.checkmate_stalemate_checker()
                                if endgame != 3:
                                    running = False
                                    game_over = True
                                    break

                    else:
                        valid_moves = game_state.get_valid_moves((row, col))
                        if valid_moves is None:
                            valid_moves = []
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r:
                    game_over = False
                    game_state = chess_engine.game_state()
                    valid_moves = []
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                elif e.key == py.K_u:
                    game_state.undo_move()
                    print(len(game_state.move_log))

        draw_game_state(screen, game_state, valid_moves, square_selected)
        endgame = game_state.checkmate_stalemate_checker()
        clock.tick(MAX_FPS)
        py.display.flip()
    endgame = game_state.checkmate_stalemate_checker()
    if endgame == 0:
        game_over = True
        draw_text(screen, "Black wins.")
        logger.info("PLAYER_2 won.")
    elif endgame == 1:
        game_over = True
        draw_text(screen, "White wins.")
        logger.info("PLAYER_1 won.")
    elif endgame == 2:
        game_over = True
        draw_text(screen, "Stalemate.")
        logger.info("Stalemate.")
    clock.tick(MAX_FPS)
    py.display.flip()

    if game_over:
        end_of_game_state_log(number_of_checks, game_state.get_number_of_moves_the_knights_made(),
                              game_state.all_whites_together, game_state.all_blacks_together)

    # elif human_player is 'w':
    #     ai = ai_engine.chess_ai()
    #     game_state = chess_engine.game_state()
    #     valid_moves = []
    #     while running:
    #         for e in py.event.get():
    #             if e.type == py.QUIT:
    #                 running = False
    #             elif e.type == py.MOUSEBUTTONDOWN:
    #                 if not game_over:
    #                     location = py.mouse.get_pos()
    #                     col = location[0] // SQ_SIZE
    #                     row = location[1] // SQ_SIZE
    #                     if square_selected == (row, col):
    #                         square_selected = ()
    #                         player_clicks = []
    #                     else:
    #                         square_selected = (row, col)
    #                         player_clicks.append(square_selected)
    #                     if len(player_clicks) == 2:
    #                         if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
    #                             square_selected = ()
    #                             player_clicks = []
    #                             valid_moves = []
    #                         else:
    #                             game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
    #                                                   (player_clicks[1][0], player_clicks[1][1]), False)
    #                             square_selected = ()
    #                             player_clicks = []
    #                             valid_moves = []
    #
    #                             ai_move = ai.minimax(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
    #                             game_state.move_piece(ai_move[0], ai_move[1], True)
    #                     else:
    #                         valid_moves = game_state.get_valid_moves((row, col))
    #                         if valid_moves is None:
    #                             valid_moves = []
    #             elif e.type == py.KEYDOWN:
    #                 if e.key == py.K_r:
    #                     game_over = False
    #                     game_state = chess_engine.game_state()
    #                     valid_moves = []
    #                     square_selected = ()
    #                     player_clicks = []
    #                     valid_moves = []
    #                 elif e.key == py.K_u:
    #                     game_state.undo_move()
    #                     print(len(game_state.move_log))
    #         draw_game_state(screen, game_state, valid_moves, square_selected)
    #
    #         endgame = game_state.checkmate_stalemate_checker()
    #         if endgame == 0:
    #             game_over = True
    #             draw_text(screen, "Black wins.")
    #         elif endgame == 1:
    #             game_over = True
    #             draw_text(screen, "White wins.")
    #         elif endgame == 2:
    #             game_over = True
    #             draw_text(screen, "Stalemate.")
    #
    #         clock.tick(MAX_FPS)
    #         py.display.flip()
    #
    # elif human_player is 'b':
    #     pass


def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
