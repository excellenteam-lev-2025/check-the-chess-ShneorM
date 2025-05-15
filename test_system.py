from chess_engine import game_state
from enums import Player

def test_fools_mate_white_loses_quickly():
    gs = game_state()

    gs.move_piece((1, 2), (2, 2), is_ai=False)  
    gs.move_piece((6, 3), (5, 3), is_ai=False)  

    gs.move_piece((1, 1), (3, 1), is_ai=False)  
    gs.move_piece((7, 4), (3, 0), is_ai=False)  

    result = gs.checkmate_stalemate_checker()
    assert result == 0 
