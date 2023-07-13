from abc import abstractmethod
import random
import json
import os


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.role = None
        self.role_prompt_path = None
        self.nigtht_action_path = os.path.join(".", "log", "night_action_memories", "players_night_actions.json")
        
    @abstractmethod
    def do_night_action(self, game):
        pass

    def record_night_action(self, memory):
        
        # Load existing memories
        with open(self.nigtht_action_path, 'r') as f:
            player_memories = json.load(f)
        
        # Update the memory of the specific player
        player_memories[str(self.player_id)] = memory

        # Write the updated memories back to the file
        with open(self.nigtht_action_path, 'w') as f:
            json.dump(player_memories, f)

    def do_day_action(self, conversation, total_rounds, round_number, count):
        conversation.generate_response(self, total_rounds, round_number, count)

    def cast_vote(self, conversation):
        vote = conversation.generate_vote(self)
        return vote
    
    def cast_vote_tie(self, conversation, tie_players_ids, combined_vote_message):
        vote = conversation.generate_vote_tie(self, tie_players_ids, combined_vote_message)
        return vote


class Werewolf(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.assigned_role = 'Werewolf'
        self.role = "Werewolf"
        self.role_prompt_path = os.path.join('.', 'prompts', 'role_prompts', 'werewolf_role.txt')

    def do_night_action(self, game):
        # Werewolves only open their eyes to see each other.
        
        # Find other werewolves
        other_werewolves = [player for player in game.players if player.role == 'Werewolf' and player != self]

        # If there are other werewolves, the werewolf can remember who they are
        if other_werewolves:
            other_werewolves_ids = [werewolf.player_id for werewolf in other_werewolves]
            memory = f"I have seen that players {other_werewolves_ids} are werewolves."
        else:
            center_card = random.choice(game.center_roles)
            memory = f"I am the only werewolf. I have seen the center card: {center_card}."

        # store the memory
        super().record_night_action(memory)

        


class Seer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.assigned_role = "Seer"
        self.role = "Seer"
        self.role_prompt_path = os.path.join('.', 'prompts', 'role_prompts', 'seer_role.txt')

    def do_night_action(self, game):
        # Seer can see another player's card or two of the center cards.

        if random.random() < 0.5:
            # Look at a player's card
            other_players = [player for player in game.players if player.player_id != self.player_id]
            chosen_player = random.choice(other_players)
            memory = f"I have seen that player {chosen_player.player_id} is a {chosen_player.role}."
        else:
            # Look at two center cards
            center_cards = random.sample(game.center_roles, 2)
            memory = f"I have seen the center cards: {center_cards}."
        
        # store the memory
        super().record_night_action(memory)

class Robber(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.assigned_role = "Robber"
        self.role = "Robber"
        self.role_prompt_path = os.path.join('.', 'prompts', 'role_prompts', 'robber_role.txt')

    def do_night_action(self, game):
        # Robber may steal another player's role card and becomes that role.
        if random.random() < 0.8:
            other_players = [player for player in game.players if player.player_id != self.player_id]
            chosen_player = random.choice(other_players)
            chosen_player_role = chosen_player.role
            chosen_player.role = self.role
            self.role = chosen_player_role
            
            memory = f"I swapped roles with player {chosen_player.player_id} and now I am a {self.role}."
        else:
            memory = f"I had the opportunity to swap but chose not to do anything."
        
        # store the memory
        super().record_night_action(memory)

class Troublemaker(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.assigned_role = "Troublemaker"
        self.role = "Troublemaker"
        self.role_prompt_path = os.path.join('.', 'prompts', 'role_prompts', 'troublemaker_role.txt')

    def do_night_action(self, game):
        # Troublemaker can swap two other players' cards.

        if random.random() < 0.5:
            other_players = [player for player in game.players if player.player_id != self.player_id]
            selected_players = random.sample(other_players, 2)
            selected_players[0].role, selected_players[1].role = selected_players[1].role, selected_players[0].role
            memory = f"I swapped roles between player {selected_players[0].player_id} and player {selected_players[1].player_id}."
        else:
            memory = f"I had the opportunity to swap between players but chose not to do anything."
        
        # store the memory
        super().record_night_action(memory)

class Villager(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.assigned_role = "Villager"
        self.role = "Villager"
        self.role_prompt_path = os.path.join('.', 'prompts', 'role_prompts', 'troublemaker_role.txt')

    def do_night_action(self, game):
        # Villager doesn't have any special action at night.
        
        memory = "As a villager, I did nothing during the night."

        # store in memory
        super().record_night_action(memory)
