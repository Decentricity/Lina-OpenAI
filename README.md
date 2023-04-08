# Lina Telegram Chatbot
Lina is a sophisticated Telegram chatbot that uses OpenAI GPT-4 to generate human-like responses to users' messages. It is capable of understanding and responding to text messages and, optionally, converting those responses into voice messages. Additionally, Lina can fetch and display content from websites by executing the links -dump <URL> command. Lina also has the ability to execute console commands, providing even greater interactivity.

### ⚠️ WARNING: ⚠️ Due to Lina's ability to interact with the operating system via console commands, it is highly recommended to run Lina in a secure and isolated environment, such as a virtual machine, and away from sensitive files, such as private keys or passwords. This precaution will prevent unauthorized access to sensitive data.

## Features
- Text and voice message support
- Website content fetching
- Chat history logging
- Easy mode toggling between text and voice responses
- Recognizes when the bot is mentioned in a group chat
- Ability to execute console commands

## Installation
Clone the repository:

```
git clone https://github.com/decentricity/Lina-OpenAI.git
cd Lina-OpenAI
```
Install the required packages:
```
pip install -r requirements.txt
```
Replace the placeholders in the code with the corresponding API keys and tokens:

Replace "put here" with your OpenAI API key
Replace "somekey" with your ElevenLabs API key
Replace 'telegram key aw' with your Telegram bot token
Set up a secure and isolated environment, such as a virtual machine, to run the bot.

Run the bot:

```
python linavotelcon.py
```
## Usage
To interact with the bot, simply send a message in a private chat or mention the bot in a group chat by typing @botusername. The bot will recognize when it is mentioned and respond accordingly.

To toggle between text and voice modes, send a message containing the #toggle keyword. The bot will switch modes and send a confirmation message indicating the new mode.

To fetch website content, include the URL in your message, and the bot will automatically extract the content and display it in the chat.

## Contributing
Contributions are welcome! Please submit a pull request or create an issue to propose changes or report bugs.
