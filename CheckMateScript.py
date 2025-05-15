
import pygame as py
from unittest.mock import patch
import chess_gui
import time

# Fool's Mate with adjusted click path
moves = [
    ((1, 3), (3, 3)),
    ((6, 3), (4, 3)),
    ((0, 4), (4, 0)),
    ((6, 0), (5, 0)),
    ((0, 2), (3, 5)),
    ((6, 7), (5, 7)),
    ((4, 0), (6, 2)),
]

def pos_to_click(square, sq_size=64):
    row, col = square
    x = col * sq_size + sq_size // 2
    y = row * sq_size + sq_size // 2
    return (x, y)

clicks = []
for move in moves:
    for square in move:
        pos = pos_to_click(square)
        clicks.append(('prep', (0, 0)))  # reset mouse
        clicks.append(('click', pos))   # target

def run():
    with patch('builtins.input', side_effect=['2']):
        py.init()
        screen = py.display.set_mode((512, 512))
        time.sleep(1.0)  # Give GUI time to initialize

        def send_clicks():
            for action, pos in clicks:
                py.mouse.set_pos(pos)
                time.sleep(0.15)
                if action == 'click':
                    py.event.post(py.event.Event(py.MOUSEBUTTONDOWN, {'pos': pos}))
                    time.sleep(0.5)

        import threading
        threading.Thread(target=send_clicks, daemon=True).start()

        chess_gui.main()

if __name__ == "__main__":
    run()
