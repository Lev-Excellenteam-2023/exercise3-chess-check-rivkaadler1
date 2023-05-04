#
# The Chess AI class
# Will utilize minimax and alpha beta pruning
#
# Author: Boo Sung Kim
# Note: Code inspired from the pseudocode by Sebastian Lague
# from enums import Player
# TODO: switch undo moves to stack data structure
import chess_engine
from enums import Player
from chess_check_logger import logger


class chess_ai:
    '''
    call minimax with alpha beta pruning
    evaluate board
    get the value of each piece
    '''

    # ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
    # in case that the human player is white
    def minimax_white(self, game_state, depth, alpha, beta, maximizing_player, player_color):
        csc = game_state.checkmate_stalemate_checker()
        if maximizing_player:
            if csc == 0:
                return 5000000
            elif csc == 1:
                return -5000000
            elif csc == 2:
                return 100
        elif not maximizing_player:
            if csc == 1:
                return 5000000
            elif csc == 0:
                return -5000000
            elif csc == 2:
                return 100

        if depth <= 0 or csc != 3:
            return self.evaluate_board(game_state, Player.PLAYER_1)

        if maximizing_player:
            max_evaluation = -10000000
            all_possible_moves = game_state.get_all_legal_moves("black")
            for move_pair in all_possible_moves:
                game_state.move_piece(move_pair[0], move_pair[1], True)
                evaluation = self.minimax_white(game_state, depth - 1, alpha, beta, False, "white")
                game_state.undo_move()

                if max_evaluation < evaluation:
                    max_evaluation = evaluation
                    best_possible_move = move_pair
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            if depth == 3:
                return best_possible_move
            else:
                return max_evaluation
        else:
            min_evaluation = 10000000
            all_possible_moves = game_state.get_all_legal_moves("white")
            for move_pair in all_possible_moves:
                game_state.move_piece(move_pair[0], move_pair[1], True)
                evaluation = self.minimax_white(game_state, depth - 1, alpha, beta, True, "black")
                game_state.undo_move()

                if min_evaluation > evaluation:
                    min_evaluation = evaluation
                    best_possible_move = move_pair
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            if depth == 3:
                return best_possible_move
            else:
                return min_evaluation

    # 0 if white lost, 1 if black lost, 2 if stalemate, 3 if not game over
    # ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
    # game_state.move_piece(ai_move[0], ai_move[1], True)
    # in case that the human is black this is the function the ai calls
    # the value of maximizing player is always true(also when you call the white minimax)
    def minimax_black(self, game_state, depth, alpha, beta, maximizing_player, player_color):
        # this is the only time this function is called in this module so it can print just "white lost"
        # in the first time csc definitely equals to three
        csc = game_state.checkmate_stalemate_checker()
        if maximizing_player:
            if csc == 1:
                return 5000000
            elif csc == 0:
                return -5000000
            elif csc == 2:
                return 100
        elif not maximizing_player:
            if csc == 0:
                return 5000000
            elif csc == 1:
                return -5000000
            elif csc == 2:
                return 100
        # It seems that the condition csc!=3 is never satisfied here because the function in this case returns a
        # value before this line so in case that depth=0 it returns the value of the board
        if depth <= 0 or csc != 3:
            return self.evaluate_board(game_state, Player.PLAYER_2)

        if maximizing_player:
            max_evaluation = -10000000
            all_possible_moves = game_state.get_all_legal_moves("white")
            for move_pair in all_possible_moves:
                # the true is just for cases of pawn
                game_state.move_piece(move_pair[0], move_pair[1], True)
                evaluation = self.minimax_black(game_state, depth - 1, alpha, beta, False, "black")
                game_state.undo_move()

                if max_evaluation < evaluation:
                    max_evaluation = evaluation
                    best_possible_move = move_pair
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            if depth == 3:
                return best_possible_move
            else:
                return max_evaluation
        else:
            min_evaluation = 10000000
            all_possible_moves = game_state.get_all_legal_moves("black")
            for move_pair in all_possible_moves:
                game_state.move_piece(move_pair[0], move_pair[1], True)
                evaluation = self.minimax_black(game_state, depth - 1, alpha, beta, True, "white")
                game_state.undo_move()

                if min_evaluation > evaluation:
                    min_evaluation = evaluation
                    best_possible_move = move_pair
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            if depth == 3:
                return best_possible_move
            else:
                return min_evaluation

    # the player parameter represents the human player
    def evaluate_board(self, game_state, player):
        evaluation_score = 0
        for row in range(0, 8):
            for col in range(0, 8):
                '''
                def is_valid_piece(self, row, col):
                evaluated_piece = self.get_piece(row, col)
                return (evaluated_piece is not None) and (evaluated_piece != Player.EMPTY)
                '''
                if game_state.is_valid_piece(row, col):
                    evaluated_piece = game_state.get_piece(row, col)
                    '''                 
                    def get_piece_value(self, piece, player):
                        # if the human player is white
                        if player is Player.PLAYER_1:
                            if piece.is_player("black"):
                                if piece.get_name() is "k":
                                    return 1000
                                elif piece.get_name() is "q":
                                    return 100
                    '''
                    evaluation_score += self.get_piece_value(evaluated_piece, player)
        return evaluation_score

    def get_piece_value(self, piece, player):
        # if the human player is white
        if player is Player.PLAYER_1:
            if piece.is_player("black"):
                if piece.get_name() is "k":
                    return 1000
                elif piece.get_name() is "q":
                    return 100
                elif piece.get_name() is "r":
                    return 50
                elif piece.get_name() is "b":
                    return 30
                elif piece.get_name() is "n":
                    return 30
                elif piece.get_name() is "p":
                    return 10
            else:
                if piece.get_name() is "k":
                    return -1000
                elif piece.get_name() is "q":
                    return -100
                elif piece.get_name() is "r":
                    return -50
                elif piece.get_name() is "b":
                    return -30
                elif piece.get_name() is "n":
                    return -30
                elif piece.get_name() is "p":
                    return -10
        else:
            if piece.is_player("white"):
                if piece.get_name() is "k":
                    return 1000
                elif piece.get_name() is "q":
                    return 100
                elif piece.get_name() is "r":
                    return 50
                elif piece.get_name() is "b":
                    return 30
                elif piece.get_name() is "n":
                    return 30
                elif piece.get_name() is "p":
                    return 10
            else:
                if piece.get_name() is "k":
                    return -1000
                elif piece.get_name() is "q":
                    return -100
                elif piece.get_name() is "r":
                    return -50
                elif piece.get_name() is "b":
                    return -30
                elif piece.get_name() is "n":
                    return -30
                elif piece.get_name() is "p":
                    return -10
