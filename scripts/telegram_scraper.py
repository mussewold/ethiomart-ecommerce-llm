from telethon.sync import TelegramClient
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
import os
from telethon import events
import json

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
# Initialize the Telegram client
client = TelegramClient('scraper_session', api_id, api_hash)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

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


async def handle_media(message, download_path):
    if message.photo:
        path = f"{download_path}/photos/{message.id}.jpg"
        await message.download_media(path)
        return path
    elif message.document:
        path = f"{download_path}/documents/{message.id}_{message.document.attributes[0].file_name}"
        await message.download_media(path)
        return path
    return None

async def process_message(message, download_path):
    media_path = await handle_media(message, download_path) if (message.photo or message.document) else None
    
    data = {
        'message_id': message.id,
        'sender': message.sender.username if message.sender else "Unknown",
        'timestamp': message.date,
        'text': message.text.replace('\n', ' ').replace(',', ' ') if message.text else "",
        'media_path': media_path if media_path else ""
    }
    
    with open('telegram_messages.csv', 'a', encoding='utf-8') as f:
        if f.tell() == 0:  # If file is empty, write header
            f.write('message_id,sender,timestamp,text,media_path\n')
        f.write(f"{data['message_id']},{data['sender']},{data['timestamp']},{data['text']},{data['media_path']}\n")
    
    if media_path:
        print_success(f"Downloaded media to {media_path}")

@client.on(events.NewMessage(chats=config['telegram_channels']))  # Modified to use JSON config
async def handle_new_message(event):
    print_info(f"New message received from {event.sender.username if event.sender else 'Unknown'}")
    download_path = 'downloads'
    os.makedirs(f"{download_path}/photos", exist_ok=True)
    os.makedirs(f"{download_path}/documents", exist_ok=True)
    await process_message(event.message, download_path)

async def main():
    print_header(f'Starting Telegram Message Monitor for {config["telegram_channels"]}')
    print_info("Waiting for new messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())