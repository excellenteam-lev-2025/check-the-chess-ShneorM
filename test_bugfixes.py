import pytest
from chess_engine import game_state
from Piece import Knight, Queen, King
from enums import Player
from ai_engine import chess_ai


# Fixtures

@pytest.fixture
def empty_board():
    """Returns a game state with an empty 8x8 board (no pieces)."""
    gs = game_state()
    gs.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
    return gs


@pytest.fixture
def ai_and_game():
    """Returns a tuple with a new AI instance and a new game state."""
    return chess_ai(), game_state()


# Bug 1: Knight should detect all enemy pieces
# This test will fail if the knight does not return exactly 8 capture moves.
def test_bug1_knight_should_take_all_surrounding_enemies(empty_board):
    knight = Knight('n', 3, 3, Player.PLAYER_1)
    empty_board.board[3][3] = knight

    # Place 8 enemy pieces in all positions a knight can capture
    enemy_positions = [(1, 2), (1, 4), (2, 1), (2, 5),
                       (4, 1), (4, 5), (5, 2), (5, 4)]

    for r, c in enemy_positions:
        empty_board.board[r][c] = Knight('n', r, c, Player.PLAYER_2)

    takes = knight.get_valid_piece_takes(empty_board)

    # Assert the knight sees exactly all 8 capture targets
    assert sorted(takes) == sorted(
        enemy_positions), f"Expected 8 takes, got {len(takes)} — {takes}"


# Bug 2: get_piece_value returns wrong sign for player's own pieces
# This test ensures own pieces return a negative score
def test_bug2_get_piece_value_negative_for_own_piece():
    ai = chess_ai()
    white_knight = Knight('n', 3, 3, Player.PLAYER_1)
    value = ai.get_piece_value(white_knight, Player.PLAYER_1)

    # Own piece should be scored negatively (e.g., -30), not positively
    assert value < 0, "Own piece should have a negative value in evaluation, got: " + \
        str(value)


# Bug 3: minimax_black logic returned incorrect scores for checkmate/stalemate scenarios
# This test ensures correct return values for all checkmate/stalemate states under both roles.
@pytest.mark.parametrize("csc, maximizing_player, expected_score, description", [
    (0, True, 5000000, "Checkmate against black (maximizing)"),
    (1, True, -5000000, "Checkmate for black (maximizing)"),
    (1, False, 5000000, "Checkmate for black (minimizing)"),
    (0, False, -5000000, "Checkmate against black (minimizing)"),
    (2, True, 100, "Stalemate (maximizing)"),
    (2, False, 100, "Stalemate (minimizing)")
])
def test_bug3_minimax_black_checkmate_logic(ai_and_game, csc, maximizing_player, expected_score, description):
    ai, gs = ai_and_game

    # Simulate checkmate/stalemate result manually
    gs.checkmate_stalemate_checker = lambda: csc

    score = ai.minimax_black(
        game_state=gs,
        depth=1,
        alpha=-9999,
        beta=9999,
        maximizing_player=maximizing_player,
        player_color=Player.PLAYER_2
    )

    assert score == expected_score, f"{description} — got {score}, expected {expected_score}"


# Bug 4: check_for_check failed to identify check threats correctly
# This check checks whether the king is threatened if he is being threatened
def test_bug4_check_for_check_detects_queen_check():
    gs = game_state()
    gs.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]

    white_king = King('k', 0, 4, Player.PLAYER_1)
    gs.board[0][4] = white_king
    gs._white_king_location = [0, 4]

    black_queen = Queen('q', 7, 4, Player.PLAYER_2)
    gs.board[7][4] = black_queen

    # Run threat detection
    checks, _, _ = gs.check_for_check(gs._white_king_location, Player.PLAYER_1)

    # Assert the queen is identified as checking the king
    assert (7, 4) in checks, "Expected queen at (7, 4) to be detected as a check on the white king"
