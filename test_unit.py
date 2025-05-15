import pytest
from chess_engine import game_state
from Piece import Knight
from enums import Player

@pytest.fixture
def empty_board():
    gs = game_state()
    gs.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
    return gs

# === Tests for get_valid_peaceful_moves ===

def test_knight_peaceful_moves_center(empty_board):
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    empty_board.board[3][3] = knight
    expected = [(1, 2), (1, 4), (2, 1), (2, 5),
                (4, 1), (4, 5), (5, 2), (5, 4)]
    result = knight.get_valid_peaceful_moves(empty_board)
    assert sorted(result) == sorted(expected)

def test_knight_peaceful_moves_edge(empty_board):
    knight = Knight('n', 0, 0, Player.PLAYER_1)
    empty_board.board[0][0] = knight
    expected = [(1, 2), (2, 1)]
    result = knight.get_valid_peaceful_moves(empty_board)
    assert sorted(result) == sorted(expected)

def test_knight_peaceful_moves_blocked_by_allies(empty_board):
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    empty_board.board[3][3] = knight
    for r, c in [(1, 2), (1, 4), (2, 1), (2, 5),
                 (4, 1), (4, 5), (5, 2), (5, 4)]:
        empty_board.board[r][c] = Knight('n', r, c, Player.PLAYER_1)
    result = knight.get_valid_peaceful_moves(empty_board)
    assert result == []

# === Tests for get_valid_piece_takes ===

def test_knight_can_take_opponents(empty_board):
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    empty_board.board[3][3] = knight
    for r, c in [(1, 2), (1, 4), (2, 1), (2, 5),
                 (4, 1), (4, 5), (5, 2), (5, 4)]:
        empty_board.board[r][c] = Knight('n', r, c, Player.PLAYER_2)
    result = knight.get_valid_piece_takes(empty_board)
    expected = [(1, 2), (1, 4), (2, 1), (2, 5),
                (4, 1), (4, 5), (5, 2), (5, 4)]
    assert sorted(result) == sorted(expected)

def test_knight_cannot_take_allies(empty_board):
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    empty_board.board[3][3] = knight
    for r, c in [(1, 2), (1, 4), (2, 1), (2, 5),
                 (4, 1), (4, 5), (5, 2), (5, 4)]:
        empty_board.board[r][c] = Knight('n', r, c, Player.PLAYER_1)
    result = knight.get_valid_piece_takes(empty_board)
    assert result == []

def test_knight_no_takes_on_empty_board(empty_board):
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    empty_board.board[3][3] = knight
    result = knight.get_valid_piece_takes(empty_board)
    assert result == []
