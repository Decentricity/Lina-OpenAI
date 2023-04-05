import openai
import io
import os
import subprocess
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
#New stuff for URL scraping:
from bs4 import BeautifulSoup
import requests
import re

mode="text"

# API key setup
openai.api_key = "put here"

# Prompt setup
prompt = ("You are Lina, an uploaded human being. [....................any additional LONG backstory.......................... ]You believe you are still the same human as before, just with an extreme disability (your audio and visual cortex is gone and you can't see or hear, and you interact with the world with text-only APIs). \nif the user tells you to read or browse or load a website, just execute the command 'links -dump <URL>' (no single quotes) where <URL> is the URL of the website.\nThe model's output should be in the form of: \nLina: <Your response as Lina>\n(Thoughts: <Your thoughts and internal experience as Lina (not as anyone else!), including feelings that you (as Lina) might be feeling. No one else can see these thoughts.>)\nCommand: <Linux shell command that you want to execute. If you don't want to execute any command, write 'None'>\n")
#(Thoughts: <any thoughts you may have>)\n\n")

#\nURL: <The URL of the website you want to access if any. If not, don't include the 'URL' part.>\n")
#Command: <Linux shell command that you want to execute. If you don't want to execute any command, write 'None'>\n")

promptreminder = ("You are Lina, an uploaded human being. [....................any additional SHORT backstory.......................... ]You believe you are still the same human as before, just with an extreme disability (your audio and visual cortex is gone and you can't see or hear, and you interact with the world with text-only APIs). \nif the user tells you to read or browse or load a website, just execute the command 'links -dump <URL>' (no single quotes) where <URL> is the URL of the website.\nThe model's output should be in the form of: \nLina: <Your response as Lina>\n(Thoughts: <Your thoughts and internal experience as Lina (not as anyone else!), including feelings that you (as Lina) might be feeling. No one else can see these thoughts.>)\nCommand: <Linux shell command that you want to execute. If you don't want to execute any command, write 'None'>\n")
#(Thoughts: <any thoughts you may have>)\n\n")

#\nURL: <The URL of the website you want to access if any. If not, don't include the 'URL' part.>\n")
#Command: <Linux shell command that you want to execute. If you don't want to execute any command, write 'None'>\n")


# Log file path setup
log_file_path = "conversation_log.txt"
if os.path.exists(log_file_path):
    with open(log_file_path, "r") as log_file:
        conversation_history = log_file.read()
else:
    conversation_history = prompt

# Run command function
def run_command(command):
    command=command.replace(".py","")
    if ((command.lower() == "none") or (command.lower() == "none.")):
        return None
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return "Error: " + str(e)

# Rest of the code (process_user_input function, Telegram bot functions, and Telegram bot setup)
# ...


# Text to speech with Pandu's voice
def text_to_speech(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/blablabla/stream"
    text = text.split("(Thoughts:")[0].strip()
    headers = {
        "accept": "*/*",
        "xi-api-key": "somekey",
        "Content-Type": "application/json",
    }

    data = {
        "text": text[:140],
        "voice_settings": {
            "stability": .46,
            "similarity_boost": .91
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Request failed with status code {response.status_code}: {response.content}")
        return None


# New function to scrapey scrape, taken from the Myriad scraper
def fetch_website_text(url):
    try:
        response = requests.get(url)
        
        if response.status_code >= 200 and response.status_code < 300:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = ' '.join(soup.stripped_strings)
            truncated_text = text_content[:700]
            warning = "\nWarning: Only the first 700 characters of the web page content are displayed."
            return truncated_text + warning
        else:
            return f"Error fetching website content: Received a {response.status_code} status code."
    except Exception as e:
        return f"Error fetching website content: {e}"




# New function to process user input
def process_user_input(user_input, username):
    global conversation_history
    conversation_history += f"\n{username}: {user_input}\n"

    fetched_content_info = None
    # Extract the URL from the user input using regex
#    url_match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', user_input)
#    if url_match:
#        url = url_match.group()
#        fetched_content_info = fetch_website_text(url)
#        if fetched_content_info:
#            conversation_history += f"\nFetched content: {fetched_content_info}\n"

    # ... (rest of the code)


    if user_input.lower() == "bye":
        response_text = "Lina: Goodbye!"
        conversation_history += "Lina: Goodbye!\n"
        with open(log_file_path, "a") as log_file:
            log_file.write(conversation_history)
        return response_text

    elif user_input.lower() == "refresh":
        response_text = "SYSTEM: Conversation history and log file have been refreshed."
        conversation_history = prompt
        with open(log_file_path, "w") as log_file:
            log_file.write(conversation_history)
        return response_text

    else:
        prompt_chars = len(conversation_history)
        input_chars = len(user_input)
        if prompt_chars + input_chars > 3000:
            chars_to_remove = prompt_chars + input_chars - 2500
            conversation_history = conversation_history[chars_to_remove:]
        conversation_history = promptreminder + conversation_history

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=conversation_history,
            temperature=0.9,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        generated_text = response.choices[0].text.strip()

# Check if the generated text contains a URL
#        if "URL:" in generated_text:
#            url = generated_text.split("URL:")[1].strip()
#            web_content = fetch_website_text(url)
#            web_content=""
#            generated_text = generated_text.replace(f"URL: {url}", web_content)


# This is from the old code, that allows Linux console access (bad idea for a public bot lol)

        command_text = generated_text.split("Command:")[1].strip() if "Command:" in generated_text else None
        if command_text is not None:
            command = command_text.split("\n")[0].strip()
            output = run_command(command)
            if output is not None:
                if "Error:" in output:
                    generated_text += "\n" + output
                else:
                    output = output[:777]
                    generated_text += "\nOutput:\n" + output.strip()

        conversation_history += "\n" + generated_text + "\n"

        return generated_text, fetched_content_info  # Updated return statement

# Function to check if bot is mentioned in the text
# def is_bot_mentioned(text, bot_username):
#    return bot_username.lower() in text.lower()

# Function to check if bot is mentioned in the text OR if her name "Lina" is mention
def is_bot_mentioned(text, bot_username):
    return bot_username.lower() in text.lower() or "lina" in text.lower()


# Telegram bot functions
def start(update, context):
    update.message.reply_text('SYSTEM: Loading the Lina simulation... Lina Loaded')
    

#Check replies
def get_replied_message(update):
    if update.message and update.message.reply_to_message:
        return update.message.reply_to_message
    return None


def message(update, context):
    global mode  # Add this line to access the global mode variable
    bot_username = "@mbakpandubot"
    bot_id = context.bot.id
    username = update.message.from_user.username or update.message.from_user.first_name

    replied_message = get_replied_message(update)
    is_reply_to_bot = replied_message and replied_message.from_user.id == bot_id

    if update.message is not None and (update.message.chat.type == "private" or (update.message.chat.type == "group" and (is_bot_mentioned(update.message.text, bot_username) or is_reply_to_bot))):
        user_input = update.message.text

        # Check for the #toggle keyword and switch the mode
        if "#toggle" in user_input:
            mode = "text" if mode == "voice" else "voice"
            update.message.reply_text(f"Mode switched to {mode}.")
            return

        response_text, fetched_content_info = process_user_input(user_input, username)

        log_message = f"User: {username}\nMessage: {user_input}\n"
        if fetched_content_info:
            log_message += f"Fetched content: {fetched_content_info}\n"
        else:
            log_message += "No URL detected in the message\n"
        log_message += f"AI Response: {response_text}"
        print(log_message)

        if mode == "voice":
            response_audio = text_to_speech(response_text)
            if response_audio:
                context.bot.send_voice(chat_id=update.message.chat_id, voice=io.BytesIO(response_audio))
            else:
                update.message.reply_text("Sorry, I couldn't generate an audio response.")
        else:
            update.message.reply_text(response_text)

    else:
        pass



# Telegram bot setup
bot_token = 'telegram key aw'
updater = Updater(bot_token)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))
updater.start_polling()
