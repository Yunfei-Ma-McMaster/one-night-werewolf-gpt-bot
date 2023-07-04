from player import Player
from werewolf import Game

class GameRunner:
    def __init__(self, player_names):
        self.roles = ['Werewolf', 'Werewolf', 'Seer', 'Robber', 'Troublemaker', 'Villager', 'Villager', 'Villager']
        self.players = self._create_players(player_names)
        self.game = Game(self.roles, self.players)

    def _create_players(self, player_names):
        player_num = len(player_names)
        players = []
        for i in range(player_num):
            players.append(Player(player_names[i]))
        return players

    def run_game(self):
        self.game.start()
