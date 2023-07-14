# one-night-werewolf-gpt-bot
This project uses `gpt-4` to build agents to play one night werewolf automatically. 

![werewolf_visual](https://github.com/Yunfei-Ma-McMaster/one-night-werewolf-gpt-bot/assets/95736471/063e8895-5c83-49eb-942d-a9ebecf5e340)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About


Welcome to the One Night Werewolf GPT Bot project. This innovative venture combines the prowess of OpenAI's GPT-4 with the thrilling dynamics of the party game [One Night Werewolf](https://www.fgbradleys.com/rules/rules2/OneNightUltimateWerewolf-rules.pdf). 

One Night Werewolf is a captivating, fast-paced game, assigning each player the role of a Villager, a Wolf, or a unique character. For those desiring an in-depth understanding of the gameplay and rules, please find them [here](https://www.ultraboardgames.com/one-night-ultimate-werewolf/game-rules.php).

This project introduces a quintet of AI players, each powered by GPT-4, fully immersing themselves into every aspect of the game. These digital players are assigned roles, perform night actions, and engage in three rounds of daytime conversation. Informed by the evolving context of the game, they cast votes, resulting in an unpredictable and intellectually engaging gameplay experience by AI players. In addition, at the very end, the AI will give a recap of the game based on the game context. 

The primary aim of this project is to explore the ability of GPT-4 to deceive, reason, infer, and make decisions within the constraints defined by game prompts and context. This is not merely several game bots; it's an investigation into the frontiers of AI's capability in social gaming contexts.

## Features

- **GPT-4 Powered:** Utilizing the state-of-the-art language model `gpt-4`, our bot is capable of sophisticated communication and strategic gameplay.

- **Automated Gameplay:** The bot can perform night actions, participate in three rounds of daytime conversation, and vote, providing a complete automated gameplay experience.

- **Five AI Players:** With five AI players and three rounds of conversation during the day, the game becomes more unpredictable and exciting. 

- **Versatile Roles:** Our AI players can play any roles in the game, be it a Villager, a Wolf, or a special character based on our written prompts.

- **Adaptable Strategies:** The AI players adapt their strategies based on the game's context, leading to dynamic and intriguing game sessions. 



## Getting Started

Follow these steps to get the project up and running on your local machine:

### Prerequisites

- Python 3.8 or above
- OpenAI GPT-4 API Key

### Installation

1. Clone the repository
2. Navigate into the project directory:
```
cd one-night-werewolf-gpt-bot
```
3. Install the necessary dependencies:
```
pip install -r requirements.txt
```
4. Add your OpenAI API Key on `config.json`:
```
"openai_api_key": "<your-api-key>"
```
or add the key in your environment variable.

## Usage


To start using the One Night Werewolf GPT Bot, you'll need to run the main script, as described below:

1. Ensure that you are in the correct directory. You should be in the same directory as the `main.py` file.

2. From the command line, execute the following command:

```
python main.py
```

This will initiate the One Night Werewolf AI Bots, starting the game with five AI players. You can follow the prompts in your terminal track the game progress.

Please note: this is a command-line game. All game progress will take place in your terminal or command prompt.

All the prompts are stored in `./prompt` and all the game logs are stored in `./log` including the night actions, the day conversation, voting, and game recap.


## Contributing

We welcome contributions to the One Night Werewolf GPT Bot! If you're interested in contributing, please read our [contribution guidelines](CONTRIBUTING.md) for more information.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgements

This project wouldn't have been possible without these open-source libraries and resources:

- [GPT-4 by OpenAI](https://openai.com/research/gpt-4): The core AI model that powers the bots in our game.
- [One Night Werewolf](https://beziergames.com/products/one-night-ultimate-werewolf): The original game that inspired this project.

We'd also like to thank the contributors who have participated in this project and helped make it better:

- [Jiyang Tang](https://github.com/tjysdsg)



