from src.game_runner import GameRunner
import os
def main():
    # Now the game has to be 5 people, could be expand to flexible later.
    player_names = ['AI_Player_A', 'AI_Player_B', 'AI_Player_C', 'AI_Player_D', 'AI_Player_E']
    game_runner = GameRunner(player_names)
    game_runner.run_game()

if __name__ == "__main__":
    main()