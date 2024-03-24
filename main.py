from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import requests
import os
from systemd import daemon
from UsersFilter import UsersFilter

# Telegram Bot Token
load_dotenv()
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
USER_IDS = [int(user_id) for user_id in os.environ['USER_IDS'].split(';')]

# API Endpoint to send POST requests
API_ENDPOINT = 'https://co.wuk.sh/api/json'

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received message from {update.message.from_user.id} with text {update.message.text}")
    message = update.message.text
    api_response = send_to_api(message)
    print(f"API response: {api_response}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=api_response)

# Function to send message contents to API using POST request
def send_to_api(message):
    data = {'url': message}  # Assuming the API expects 'text' field
    try:
        response = requests.post(
            API_ENDPOINT,
            json=data,
            headers={"Accept": "application/json", "Content-Type": "application/json"}
        )
        response_data = response.json()  # Assuming API response is JSON
        if ("url" in response_data):
            return response_data["url"]  # Return API response
        raise requests.exceptions.RequestException(f"API response {response_data} does not contain 'url' key")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")
        return None

if __name__ == '__main__':
    print('Bot starting up...')
    application = ApplicationBuilder().token(TOKEN).build()
    users_filter = UsersFilter(USER_IDS)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND) & users_filter, echo)
    application.add_handler(echo_handler)
    print('Bot startup complete.')
    daemon.notify('READY=1')
    application.run_polling()
