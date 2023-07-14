import openai
import json
import os

class ConversationHandler:
    """
    Handles the conversation and voting based on private and public information in game log(memory)
    """
    def __init__(self):
        self.conversation = []
        self.players_day_conversation_path = os.path.join(".", "log", "day_public_conversation", "players_day_conversation.json")
        self._clear_conversation()

    def add_message(self, player_id, content):
        """Add conversation message to the conversation history

        Args:
            player_id (int): AI player id number
            content (string): Conversational message generative by gpt-4
        """
        self.conversation.append({'player_id': player_id, 'content': content})
        self._save_conversation_to_file()

    def _save_conversation_to_file(self):
        """save the conversation to the conversation history in log
        """
        with open(self.players_day_conversation_path, 'w') as f:
            json.dump(self.conversation, f)

    def generate_response(self, player, total_rounds, round_number, count):
        """
        Constructs a prompt for an AI player's conversation in the game based on the current round and count.
    
        The conversation prompt includes the AI player's night action and the history of day conversations.
        This provides the AI player with the context of which round and which count it is currently at in the game. 

        The reponse is added to the conversation history during the day.
        Args:
            player (Player): The AI player for which the prompt is being constructed.
            total_rounds (int): The total number of conversation rounds in the game.
            round_number (int): The current round number in the game.
            count (int): The current conversation count within the current round.
        """
        messages = []

        # Get the game starting prompt
        game_rule_file_path = os.path.join('.', 'prompts', 'game_prompts', 'game_rule.txt')
        with open(game_rule_file_path, 'r') as file:
            game_rule_text = file.read()
        game_rule_text += f"\n\nYou are {player.player_id} in this game."
        messages.append({
            "role": "system",
            "content": game_rule_text
        })
        
        # Get the role assignment prompt
        role_prompt_file_path = player.role_prompt_path
        with open(role_prompt_file_path, 'r') as file:
            role_prompt_text = file.read()
        messages.append({
            "role": "system",
            "content": role_prompt_text
        })

        # Get night action
        night_action_path = os.path.join('.','log', 'night_action_memories', 'players_night_actions.json')
        with open(night_action_path, 'r') as file:
            night_actions = json.load(file)
        messages.append({
            "role": "assistant",
            "name": player.player_id,
            "content": night_actions.get(player.player_id, '') ##?? test if it is right
        })

        # Get the conversation history
        with open(self.players_day_conversation_path, 'r') as file:
            conversation_history = json.load(file)
        for conversation in conversation_history:
            messages.append({
                "role": "assistant",
                "name": conversation['player_id'],
                "content": conversation['content']
            })

        # Respone prompt
        response_prompt_path = os.path.join('.', 'prompts', 'game_prompts', 'response_rule.txt')
        with open(response_prompt_path, 'r') as file:
            response_prompt_text = file.read()
        response_prompt_text = f"{player.player_id}," + response_prompt_text + f" \n Please note your are now in number {count}" + f"in discussion round {round_number}" + f"Their are total {total_rounds} rounds of discussion. Please adjust your strategy accordingly. "
        messages.append({
            "role": "user",
            "content" : response_prompt_text
        })

        # OPEN AI
        with open("config.json") as f:
            config = json.load(f)
        api_key = config['openai_api_key']
        # API key can be overriden by the environment variable
        env_api_key = os.getenv("OPENAI_API_KEY")
        if env_api_key is not None:
            api_key = env_api_key
        openai.api_key = api_key

        MODEL = "gpt-4" # make it can be modified in commandline later


        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.8 # make it can be modified in commandline later
        )

        # add the conversation
        self.add_message(player.player_id, response['choices'][0]['message']['content'])

        print(f"{player.player_id}:" + response['choices'][0]['message']['content'] + "\n")
    
    def generate_vote(self, player):
        """
        Generate vote based on player's night actions and day conversations

        Args:
            player (Player): The AI player

        Returns:
            str: The player's name
        """
        messages = []
        # Get the game starting prompt
        game_rule_file_path = os.path.join('.', 'prompts', 'game_prompts', 'game_rule.txt')
        with open(game_rule_file_path, 'r') as file:
            game_rule_text = file.read()
        game_rule_text += f"\n\nYou are {player.player_id} in this game."
        messages.append({
            "role": "system",
            "content": game_rule_text
        })
        
        # Get the role assignment prompt
        role_prompt_file_path = player.role_prompt_path
        with open(role_prompt_file_path, 'r') as file:
            role_prompt_text = file.read()
        messages.append({
            "role": "system",
            "content": role_prompt_text
        })

        # Get night action
        night_action_path = os.path.join('.','log', 'night_action_memories', 'players_night_actions.json')
        with open(night_action_path, 'r') as file:
            night_actions = json.load(file)
        messages.append({
            "role": "assistant",
            "name": player.player_id,
            "content": night_actions.get(player.player_id, '') 
        })

        # Get the conversation history
        with open(self.players_day_conversation_path, 'r') as file:
            conversation_history = json.load(file)
        for conversation in conversation_history:
            messages.append({
                "role": "assistant",
                "name": conversation['player_id'],
                "content": conversation['content']
            })
        
        # Get the voting rule
        vote_rule_path = os.path.join('.','prompts', 'game_prompts', 'vote_rule.txt')
        with open(vote_rule_path, 'r') as file:
            vote_rule = file.read()
        messages.append({
            "role": "user",
            "content": vote_rule
        })

        # OPEN AI
        with open("config.json") as f:
            config = json.load(f)
        api_key = config['openai_api_key']
        # API key can be overriden by the environment variable
        env_api_key = os.getenv("OPENAI_API_KEY")
        if env_api_key is not None:
            api_key = env_api_key
        openai.api_key = api_key

        MODEL = "gpt-4" # make it can be modified in commandline later


        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.2 # make it can be modified in commandline later
        )

        voted_player = response['choices'][0]['message']['content'].replace("'","")

        return voted_player
    
    def generate_vote_tie(self, player, tie_players_ids, combined_vote_message):
        """
        This is a backup function to regenerate vote if there is a tie

        Args:
            player (Player): The AI player
            tie_players_ids (list<str>): The list of tied players' ids last round
            combined_vote_message (string): The combined voted message last round

        Returns:
            str: The voted player's name
        """
        messages = []
        # Get the game starting prompt
        game_rule_file_path = os.path.join('.', 'prompts', 'game_prompts', 'game_rule.txt')
        with open(game_rule_file_path, 'r') as file:
            game_rule_text = file.read()
        game_rule_text += f"\n\nYou are {player.player_id} in this game."
        messages.append({
            "role": "system",
            "content": game_rule_text
        })
        
        # Get the role assignment prompt
        role_prompt_file_path = player.role_prompt_path
        with open(role_prompt_file_path, 'r') as file:
            role_prompt_text = file.read()
        messages.append({
            "role": "system",
            "content": role_prompt_text
        })

        # Get night action
        night_action_path = os.path.join('.','log', 'night_action_memories', 'players_night_actions.json')
        with open(night_action_path, 'r') as file:
            night_actions = json.load(file)
        messages.append({
            "role": "assistant",
            "name": player.player_id,
            "content": night_actions.get(player.player_id, '') ##?? test if it is right
        })

        # Get the conversation history
        with open(self.players_day_conversation_path, 'r') as file:
            conversation_history = json.load(file)
        for conversation in conversation_history:
            messages.append({
                "role": "assistant",
                "name": conversation['player_id'],
                "content": conversation['content']
            })
        
        # Get tie voting prompt
        tie_players_ids_string = ", ".join(tie_players_ids)
        vote_rule_tie_path = os.path.join('.','prompts', 'game_prompts', 'vote_rule_tie.txt')
        with open(vote_rule_tie_path, 'r') as file:
            vote_rule_tie = file.read()
        vote_rule_tie = f"The last round of voting results are {combined_vote_message}. These players are tied [" + tie_players_ids_string + "]" + vote_rule_tie 
        messages.append({
            "role": "user",
            "content": vote_rule_tie
        })

        # OPEN AI
        with open("config.json") as f:
            config = json.load(f)
        api_key = config['openai_api_key']
        # API key can be overriden by the environment variable
        env_api_key = os.getenv("OPENAI_API_KEY")
        if env_api_key is not None:
            api_key = env_api_key
        openai.api_key = api_key

        MODEL = "gpt-4" # make it can be modified in commandline later


        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.2 # make it can be modified in commandline later
        )

        voted_player = response['choices'][0]['message']['content'].replace("'","")

        return voted_player
    
    def game_recap(self):
        """
        Generate a game recap with a birds eye view on all the information avaiable

        Returns:
            str: The comprehensive recap of the game
        """
        messages = []
        # Get the game starting prompt
        recap_rule_path = os.path.join('.', 'prompts', 'game_prompts', 'recap_rule.txt')
        with open(recap_rule_path, 'r') as file:
            recap_rule_text = file.read()
        messages.append({
            "role": "system",
            "content": recap_rule_text
        })

        # Get night action
        night_action_path = os.path.join('.','log', 'night_action_memories', 'players_night_actions.json')
        with open(night_action_path, 'r') as file:
            night_actions = json.load(file)
        night_action_string = json.dumps(night_actions)
        messages.append({
            "role": "assistant",
            "content": "Here is the actions each player did during night: \n" + night_action_string
        })

        # Get the conversation history
        with open(self.players_day_conversation_path, 'r') as file:
            conversation_history = json.load(file)
        for conversation in conversation_history:
            messages.append({
                "role": "assistant",
                "name": conversation['player_id'],
                "content": conversation['content']
            })

        # Get the voting and game results
        player_voting_actions_path =  os.path.join(".", "log", "voting_action", "voting_action.txt")
        with open(player_voting_actions_path, "r") as file:
            voting_results = file.read()
        messages.append({
            "role": "assistant",
            "name": "Announcer",
            "content": "Here is the voting and game results: \n" + voting_results
        })

        # Get game recap prompt
        game_recap_path = os.path.join('.', 'prompts', 'game_prompts', 'game_recap.txt')
        with open(game_recap_path, 'r') as f:
            game_recap_instruction_text = f.read()
        messages.append({
            "role": "user",
            "content": game_recap_instruction_text 
        })

        # OPEN AI
        with open("config.json") as f:
            config = json.load(f)
        api_key = config['openai_api_key']
        # API key can be overriden by the environment variable
        env_api_key = os.getenv("OPENAI_API_KEY")
        if env_api_key is not None:
            api_key = env_api_key
        openai.api_key = api_key

        MODEL = "gpt-4" # make it can be modified in commandline later


        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.8 # make it can be modified in commandline later
        )

        return response['choices'][0]['message']['content']

    
    def _clear_conversation(self):
        """
        Clear the conversation history
        """
        with open(self.players_day_conversation_path, 'w') as file:
            json.dump([], file)