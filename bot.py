import os
import requests
import telegram
import asyncio

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
WEBSITE_URL = os.getenv('WEBSITE_URL')
SERVER_IP = os.getenv('SERVER_IP')

# Telegram bot setup
bot = telegram.Bot(token=BOT_TOKEN)

async def check_website():
    try:
        response = requests.get(WEBSITE_URL)
        return f"Website is UP. Status code: {response.status_code}" if response.status_code == 200 else f"Website is DOWN. Status code: {response.status_code}"
    except requests.ConnectionError:
        return "Website is DOWN. Connection error."

async def ping_server():
    # Pinging the server using the OS ping command
    response = os.system(f"ping -c 1 {SERVER_IP}")
    
    if response == 0:
        return "Server is UP (Ping successful)."
    else:
        return "Server is DOWN (Ping failed)."

async def send_status_update():
    website_status = await check_website()
    server_status = await ping_server()
    message = f"Website Status: {website_status}\nServer Status: {server_status}"
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    while True:
        await send_status_update()
        await asyncio.sleep(60 * 60 * 5)  # Check every 5 hours

if __name__ == "__main__":
    asyncio.run(main())
