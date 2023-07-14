from src.player import Player
from src.werewolf import Game

class GameRunner:
    """
    The GameRunner class creates player and starts the game
    """
    def __init__(self, player_names):
        self.roles = ['Werewolf', 'Werewolf', 'Seer', 'Robber', 'Troublemaker', 'Villager', 'Villager', 'Villager']
        self.players = self._create_players(player_names)
        self.game = Game(self.roles, self.players)

    def _create_players(self, player_names):
        """
        Create players for the name

        Args:
            player_names (list<str>): The list of players' name

        Returns:
            list<Player>: A list of AI players
        """
        player_num = len(player_names)
        players = []
        for i in range(player_num):
            players.append(Player(player_names[i]))
        return players

    def run_game(self):
        """
        This is a game starter function
        """
        self.game.start()
