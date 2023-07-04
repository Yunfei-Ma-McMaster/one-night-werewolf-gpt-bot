import openai
import json
import os

class ConversationHandler:
    def __init__(self):
        self.conversation = []
        self.players_day_conversation_path = os.path.join(".", "log", "day_public_conversation", "players_day_conversation.json")
        self._clear_conversation()

    def add_message(self, player_id, content):
        self.conversation.append({'player_id': player_id, 'content': content})
        self._save_conversation_to_file()

    def _save_conversation_to_file(self):
        with open(self.players_day_conversation_path, 'w') as f:
            json.dump(self.conversation, f)

    def generate_response(self, player, total_rounds, round_number, count):
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
        with open(self.players_day_conversation_path, 'w') as file:
            json.dump([], file)