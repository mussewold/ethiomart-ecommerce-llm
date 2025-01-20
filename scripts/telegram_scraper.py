from telethon.sync import TelegramClient
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
import os

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
# Initialize the Telegram client
client = TelegramClient('scraper_session', api_id, api_hash)


PURPLE_BLUE = '\033[38;2;100;100;255m'
LIGHT_PURPLE = '\033[38;2;200;180;255m'
BOLD_WHITE = '\033[1;37m'

def print_info(message):
    print(f"{PURPLE_BLUE}ℹ {BOLD_WHITE}{message}")

def print_success(message):
    print(f"{LIGHT_PURPLE}✔ {BOLD_WHITE}{message}")

def print_warning(message):
    print(f"{Fore.YELLOW}{Style.BRIGHT}⚠ {BOLD_WHITE}{message}")

def print_error(message):
    print(f"{Fore.RED}✘ {message}")

def print_header(message):
    print(f"\n{PURPLE_BLUE}{Style.BRIGHT}{message}")
    print(f"{PURPLE_BLUE}{'-' * len(message)}{Style.RESET_ALL}")

def print_subheader(message):
    print(f"\n{LIGHT_PURPLE}{Style.BRIGHT}{message}")
    print(f"{LIGHT_PURPLE}{'-' * len(message)}{Style.RESET_ALL}")


async def scrape_messages(client, channel, limit=100):
    async for message in client.iter_messages(channel, limit=limit):
        if(message.text):
            # Replace newlines with spaces to keep one message per row
            cleaned_text = message.text.replace('\n', ' ').replace(',', ' ')
            data = {
            'message_id': message.id,
            'sender': message.sender.username if message.sender else "Unknown",
            'timestamp': message.date,
            'text': message.text.replace('\n', ' ').replace(',', ' ') if message.text else "",
            }
            with open('telegram_messages.csv', 'a', encoding='utf-8') as f:
                if f.tell() == 0:  # If file is empty, write header
                    f.write('message_id,sender,timestamp,text\n')
                f.write(f"{data['message_id']},{data['sender']},{data['timestamp']},{data['text']}\n")
    


async def main():
    channel = '@MerttEka'
    await scrape_messages(client, channel)
with client:
    client.loop.run_until_complete(main())