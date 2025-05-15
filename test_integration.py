import pytest
from chess_engine import game_state
from Piece import Knight
from enums import Player
from ai_engine import chess_ai

@pytest.fixture
def knight_in_center_board():
    gs = game_state()
    gs.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    gs.board[3][3] = knight
    return gs, knight

def test_knight_valid_piece_moves(knight_in_center_board):
    gs, knight = knight_in_center_board
    expected = [(1, 2), (1, 4), (2, 1), (2, 5),
                (4, 1), (4, 5), (5, 2), (5, 4)]
    actual = knight.get_valid_piece_moves(gs)
    assert sorted(actual) == sorted(expected)

def test_ai_evaluate_board():
    gs = game_state()
    gs.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
    white_knight = Knight('n', 4, 4, Player.PLAYER_1)
    gs.board[4][4] = white_knight

    from Piece import Rook
    black_rook = Rook('r', 0, 0, Player.PLAYER_2)
    gs.board[0][0] = black_rook

    ai = chess_ai()
    score = ai.evaluate_board(gs, Player.PLAYER_1)

    assert isinstance(score, (int, float))
    assert score == 20  
