import random
import json
import os
import time
from src.conversation_handler import ConversationHandler 
from src.player import Werewolf, Seer, Robber, Troublemaker, Villager

class Game:
    """
    The game instance class
    """
    def __init__(self, roles, players):
        self.roles = roles
        self.players = players
        self.center_roles = []
        self.phase = 'Night'
        self.conversation = ConversationHandler()

    def start(self):
        """
        Game starter: 
        1. Start the game by clear all the log(memory)
        2. Assign roles to players
        3. Perform night actions
        4. Perform day actions
        5. Cast votes
        6. Game recap
        """
        # Game start image
        werewolf_ASCII_image_path = os.path.join('.','assets','ascii-werewolf.txt')
        with open(werewolf_ASCII_image_path, 'r') as file:
            werewolf_ASCII_string = file.read()
        print(werewolf_ASCII_string + '\n\n\n\n')
        time.sleep(3)
        print("\n --------Game Starts--------- \n")

        # Clean the log
        player_night_action_path = os.path.join(".", "log", "night_action_memories", "players_night_actions.json")
        empty_memories = {player.player_id: "" for player in self.players}
        with open(player_night_action_path, 'w') as f:
            json.dump(empty_memories, f)
        
        player_day_conversation_path = os.path.join(".", "log", "day_public_conversation", "players_day_conversation.json")
        with open(player_day_conversation_path, 'w') as f:
            json.dump([], f)

        player_voting_actions_path =  os.path.join(".", "log", "voting_action", "voting_action.txt")
        with open(player_voting_actions_path, 'w') as f:
            f.write("The final voting results of the game is listed below: \n")
        
        game_recap_path = os.path.join(".", "log", "game_recap", "AI_game_recap.txt")
        with open(game_recap_path, "w") as f:
            f.write("")

        # Shuffle roles and assign to players
        self._assign_roles()

        # Perform night actions
        self._night_phase()

        # Perform day actions (discussion)
        self._day_phase()

        # Voting and game end
        self._voting_phase()

        # Game Recap
        self._game_recap_phase()

    @staticmethod
    def create_player(role, player_id):
        """
        Create players based on player's name and assigned roles

        Args:
            role (str): The role randomly assign to players
            player_id (str): The name of the AI player

        Returns:
            Player: The created player
        """
        if role == 'Werewolf':
            return Werewolf(player_id)
        elif role == 'Seer':
            return Seer(player_id)
        elif role == 'Robber':
            return Robber(player_id)
        elif role == 'Troublemaker':
            return Troublemaker(player_id)
        elif role == 'Villager':
            return Villager(player_id)
        else:
            raise ValueError(f"Unknown role: {role}")

    def _assign_roles(self):
        """
        Assign roles to all the players
        """
        shuffled_roles = self.roles[:]
        random.shuffle(shuffled_roles)
        
        for i, player in enumerate(self.players):
            role = shuffled_roles.pop()
            self.players[i] = self.create_player(role, player.player_id)
        
        self.center_roles = shuffled_roles

        print("\nAnnouncer: The role has been assigned to AI players! \n")

    def _night_phase(self):
        """
        The night phase of the game, where all player perform private action based on roles
        """
        print("\nAnnouncer: The night has started, please close your eyes! \n")

        for player in self.players:
            player.do_night_action(self)
    
        # Transition to Day phase after all night actions are complete
        self.phase = 'Day'

    def _day_phase(self):
        """
        The day phase of the game, where all players have public conversations
        """

        print("\nAnnouncer: The day is coming, please start the conversation! \n")

        print("\n --------Conversation Starts--------- \n")

        ### players talk for 2 rounds based on gpt-4

        # random shuffle player for sequence
        random.shuffle(self.players)

        # each play perform do day action twice
        total_rounds = 3
        for i in range(total_rounds):
            count = 1
            for player in self.players:
                player.do_day_action(self.conversation, total_rounds, i+1 , count)
        
        print("\n --------Conversation Ends--------- \n")
        # Transition to Voting phase after all day actions are complete
        self.phase = 'Voting'

    def _voting_phase(self):
        """
        The voting phase, where all the players vote based on public and private log(memory)

        Raises:
            ValueError: The wrong player Id generated by GPT-4
            ValueError: The wrong player Id generated by GPT-4
        """
        print("\nAnnouncer: Please vote who is the Werewolf!")
        # Create a dictionary to map player_id to player
        player_vote_dict = {player: 0 for player in self.players}
        player_dict = {player.player_id : player for player in self.players}
        
        for player in self.players:
            vote = player.cast_vote(self.conversation)
            if vote not in player_dict:
                raise ValueError(f"The vote '{vote}' is not a valid player_id.")
            else:
                player_vote_dict[player_dict[vote]] += 1
        
        # Check if there is a tie
        max_votes = max(player_vote_dict.values())

        # Get all players who have the highest vote count
        highest_voted_players = [player for player, votes in player_vote_dict.items() if votes == max_votes]
        highest_voted_players_ids = [player.player_id for player in highest_voted_players]
        while len(highest_voted_players) > 1:
            for player in self.players:
                print(f"Player {player.player_id} has a vote of {player_vote_dict[player]}. \n ")
            print("\n There is a tie! Addition round of voting triggered \n")

            # Store the voted information in message
            vote_messages = [f"Player {player.player_id} has a vote of {player_vote_dict[player]}." for player in self.players]
            combined_vote_message = "\n".join(vote_messages)

            # Update players dictionary
            player_vote_dict = {player: 0 for player in self.players}
            for player in self.players:
                vote = player.cast_vote_tie(self.conversation, highest_voted_players_ids, combined_vote_message)
                if vote not in player_dict:
                    raise ValueError(f"The vote '{vote}' is not a valid player_id or not the range of player for additional round!")
                else:
                    player_vote_dict[player_dict[vote]] += 1
            # Check if there is a tie
            max_votes = max(player_vote_dict.values())

            # Get all players who have the highest vote count
            highest_voted_players = [player for player, votes in player_vote_dict.items() if votes == max_votes]
            highest_voted_players_ids = [player.player_id for player in highest_voted_players]
        else:
            self.report_the_results(player_vote_dict)

    def report_the_results(self, player_vote_dict):
        """
        Print the game results in command line

        Args:
            player_vote_dict (dict of str: int): The final voting results
        """
        print("\n --------Game Results--------- \n")

        player_voting_actions_path =  os.path.join(".", "log", "voting_action", "voting_action.txt")

        for player in self.players:
            print(f"Player {player.player_id} (Assigned Role : {player.assigned_role}, Final Role : {player.role}) has a vote of {player_vote_dict[player]}. \n ")
            with open(player_voting_actions_path, 'a') as f:
                f.write(f"Player {player.player_id} (Assigned Role : {player.assigned_role}, Final Role : {player.role}) has a vote of {player_vote_dict[player]}. \n ")
        max_voted_player = max(player_vote_dict, key=player_vote_dict.get)

        # Decide the results
        if max_voted_player.role == "Werewolf":
            print("Villager Team Win!!!!!!! \n \n")
            with open(player_voting_actions_path, 'a') as f:
                f.write("The game result: Villager Team Win!!\n")
        else:
            print ("Werewolf Team Win!!!!!!! \n \n")
            with open(player_voting_actions_path, 'a') as f:
                f.write("The game result: Werewolf Team Win!!")

        print("\n --------Game Ends--------- \n")
    
    def _game_recap_phase(self):
        """
        Game recap phase to analysis the game plays
        """

        print("\n --------AI Game Recap--------- \n")
        game_recap_path = os.path.join(".", "log", "game_recap", "AI_game_recap.txt")
        game_recap = self.conversation.game_recap()

        with open(game_recap_path, "w") as file:
            file.write(game_recap)
        
        print(f"{game_recap}")
        
        



        


        


        
