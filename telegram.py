from telethon import TelegramClient, events, sync
from telethon.tl.types import InputMessagesFilterPhotos
import sqlite3
from PIL import Image
from pytesseract import image_to_string
import logging
import os

# Define the folder where you want to store the images
image_folder = 'downloaded_images'

# Make sure the folder exists
os.makedirs(image_folder, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)

# Database setup
connection = sqlite3.connect('job_offers.db')
cursor = connection.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS job_offers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT UNIQUE
                )''')
connection.commit()

api_id = 22044463
api_hash = "fb0a519d38eb534d36dc5a5cc38e1dee"

client = TelegramClient('anon', api_id, api_hash)

# Function to store OCR result to database
def store_to_db(text):
    try:
        cursor.execute("INSERT INTO job_offers (text) VALUES (?)", (text,))
        connection.commit()
    except sqlite3.IntegrityError:
        # This error will happen if the text is already in the database, so just ignore it
        pass

async def ocr_and_store_photo(message):
    # Download the image
    path = await message.download_media(file=os.path.join(image_folder, message.photo.id + '.jpg'))

    # OCR the image
    text = image_to_string(Image.open(path))

    # Store the result in the database if not already present
    store_to_db(text)

async def process_chat_history(chat_id):
    # Using the client to iterate over all messages
    async for message in client.iter_messages(chat_id, filter=InputMessagesFilterPhotos):
        # Check if the message has a photo
        if message.photo:
            await ocr_and_store_photo(message)

# The main script execution starts here
with client:
    client.loop.run_until_complete(process_chat_history(-1001256733013))

# Close the database connection
connection.close()
