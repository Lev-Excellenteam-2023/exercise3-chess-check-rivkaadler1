import pytest
import ai_engine
import chess_engine
from enums import Player
from Piece import Knight
from unittest.mock import Mock


# the run command:pytest test_chess_game.py::TestChessGame

class TestChessGame:
    knight = Knight('n', 3, 4, Player.PLAYER_1)

    # Test cases for knight.get_valid_peaceful_moves method

    def test_get_valid_peaceful_moves_all_empty(self):
        # Create a mock for the `game_state.get_piece` method
        mock_get_piece = Mock(return_value=Player.EMPTY)
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        # Call the `Knight.get_valid_peaceful_moves` method
        result = self.knight.get_valid_peaceful_moves(game_state)
        # Assert that the method returned the expected result
        assert result == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]

    def test_get_valid_peaceful_moves_all_full(self):
        mock_get_piece = Mock(return_value='p')
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        assert self.knight.get_valid_peaceful_moves(game_state) == []

    def test_knight_get_valid_peaceful_moves_some_empty_some_full(self):
        # Create a mock for the `game_state.get_piece` method that returns `Player.EMPTY` for some positions and a
        # non-empty value for others
        mock_get_piece = Mock(side_effect=[Player.EMPTY, 'p', Player.EMPTY, 'r', 'b', 'n', Player.EMPTY, Player.EMPTY])
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        # Call the `Knight.get_valid_peaceful_moves` method
        result = self.knight.get_valid_peaceful_moves(game_state)
        # Assert that the method returned the expected result
        assert result == [(1, 3), (2, 2), (5, 5), (5, 3)]

    # Test cases for knight.get_valid_piece_takes method

    def test_get_valid_piece_takes_all_empty(self):
        # Create a mock for the `game_state.get_piece` method
        mock_get_piece = Mock(return_value=1)
        # Create a mock for the `game_state.is_valid_piece` method
        mock_is_valid_piece = Mock(return_value=False)
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        game_state.is_valid_piece = mock_is_valid_piece
        # Call the `Knight.get_valid_piece_takes` method
        result = self.knight.get_valid_piece_takes(game_state)
        # Assert that the method returned the expected result
        assert result == []

    def test_get_valid_piece_takes_when_all_full_of_pieces_of_opponent(self):
        mock_get_piece = Mock(return_value=self.knight)
        mock_is_valid_piece = Mock(return_value=True)
        # Create a Knight object and a mock game_state object
        knight = Knight('n', 3, 4, Player.PLAYER_2)
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        game_state.is_valid_piece = mock_is_valid_piece
        # Call the `Knight.get_valid_piece_takes` method
        result = knight.get_valid_piece_takes(game_state)
        # Assert that the method returned the expected result
        assert result == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]

    def test_get_valid_piece_takes_some_full_of_pieces_of_opponent_some_empty_and_some_full_of_pieces_that_belong_to_the_player(
            self):
        # Create a mock for the `game_state.get_piece` method that returns `Player.EMPTY` for some positions and a
        # non-empty value for others
        mock_get_piece = Mock(side_effect=[Player.EMPTY, Knight('n', 3, 4, Player.PLAYER_1), Player.EMPTY,
                                           Knight('n', 3, 4, Player.PLAYER_1), Knight('n', 3, 4, Player.PLAYER_2),
                                           Knight('n', 3, 4, Player.PLAYER_2), Player.EMPTY, Player.EMPTY])
        mock_is_valid_piece = Mock(side_effect=[False, True, False, True, True, True, False, False])

        game_state = Mock()
        game_state.get_piece = mock_get_piece
        game_state.is_valid_piece = mock_is_valid_piece
        # Call the `Knight.get_valid_peaceful_moves` method
        result = self.knight.get_valid_piece_takes(game_state)
        # Assert that the method returned the expected result
        assert result == [(4, 2), (4, 6)]

    # Integration tests

    def test_get_valid_piece_moves(self):
        # Create a mock for the `game_state.get_piece` method
        mock_get_piece = Mock(return_value=Player.EMPTY)
        mock_is_valid_piece = Mock(return_value=False)
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        game_state.is_valid_piece = mock_is_valid_piece
        assert self.knight.get_valid_piece_moves(game_state) == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5),
                                                                 (5, 3)]

    def test_evaluate_board(self):
        ai = ai_engine.chess_ai()
        mock_get_piece = Mock(return_value=self.knight)
        mock_is_valid_piece = Mock(return_value=True)
        game_state = Mock()
        game_state.get_piece = mock_get_piece
        game_state.is_valid_piece = mock_is_valid_piece
        result = ai.evaluate_board(game_state, Player.PLAYER_2)
        assert result == 1920

    # system test

    def test_chess_game(self):
        game_state = chess_engine.game_state()
        game_state.move_piece((1, 2), (2, 2), False)
        game_state.move_piece((6, 3), (4, 3), False)
        game_state.move_piece((1, 1), (3, 1), False)
        game_state.move_piece((7, 4), (3, 0), False)
        assert game_state.checkmate_stalemate_checker() == 0
