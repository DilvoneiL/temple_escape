from game.constants import WIDTH, HEIGHT
from game.entities import Button

def build_menu_buttons(start_game_cb, toggle_audio_cb, exit_game_cb, music_on):
    sound_text = "Music: ON" if music_on else "Music: OFF"
    return [
        Button("Start Game", (WIDTH // 2 - 110, 200), start_game_cb),
        Button(sound_text, (WIDTH // 2 - 110, 280), toggle_audio_cb),
        Button("Exit", (WIDTH // 2 - 110, 360), exit_game_cb),
    ]

def build_end_buttons(play_again_cb, back_to_menu_cb, exit_game_cb):
    return [
        Button("Play Again", (WIDTH // 2 - 110, HEIGHT // 2 + 40), play_again_cb),
        Button("Back to Menu", (WIDTH // 2 - 110, HEIGHT // 2 + 110), back_to_menu_cb),
        Button("Exit", (WIDTH // 2 - 110, HEIGHT // 2 + 180), exit_game_cb),
    ]
