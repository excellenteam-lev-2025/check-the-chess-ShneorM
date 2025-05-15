import pytest

import chess_engine
import ai_engine

@pytest.fixture
def empty_game_state():
    return chess_engine.game_state()


def test_initial_board_setup(empty_game_state):
    board = empty_game_state.board
    assert board[7][4]._name == 'q'
    assert board[0][0]._name == 'r'

def test_move_piece(empty_game_state):
    # This test checks that moving pieces works

    empty_game_state.move_piece((1, 3), (3, 3), is_ai=False) # Move black pawn from (1,3) to (3,3)
    
    assert empty_game_state.board[3][3]._name == 'p'
    assert empty_game_state.board[1][3] == chess_engine.Player.EMPTY

def test_white_pawn_captures_black_pawn(empty_game_state):
    # This test checks that capturing pieces works
    empty_game_state.board[2][3] = empty_game_state.board[6][3]  # Move black pawn from (6,3) to (2,3)
    empty_game_state.board[6][3] = chess_engine.Player.EMPTY

    empty_game_state.move_piece((1, 4), (2, 3), is_ai=False)

    assert len(empty_game_state.black_captives) == 1

def test_move_log(empty_game_state):
    empty_game_state.move_piece((1, 4), (2, 4), is_ai=False)
    empty_game_state.undo_move()
    assert len(empty_game_state.move_log) == 0