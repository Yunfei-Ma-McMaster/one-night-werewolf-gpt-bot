from game_runner import GameRunner

def main():
    # Now the game has to be 5 people, could be expand to flexible later.
    player_names = ['AlphaByte_Wolfbane', 'DeepNeura_HowlNet', 'CyberPaws_MoonCode', 'QuantumFur_ByteBite', 'ShadowSilicon_PackProtocol']
    game_runner = GameRunner(player_names)
    game_runner.run_game()

if __name__ == "__main__":
    main()