import openai
import os
import telebot

import botactions
from botactions.constants import AUTHORIZED_USER_MESSAGE, AVALIABLE_COMMANDS_MESSAGE


TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
openai.api_key = os.environ["OPENAI_API_KEY"]


bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


def start_bot():
    try:
        bot.infinity_polling(timeout=123)
    except Exception as exception:
        pass


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if botactions.verify_user(message.from_user.id) == True:
        bot.send_message(message.from_user.id, AUTHORIZED_USER_MESSAGE)


@bot.message_handler(commands=['actions'])
def send_avaliable_actions(message):
    if botactions.verify_user(message.from_user.id) == True:
        bot.send_message(message.from_user.id, AVALIABLE_COMMANDS_MESSAGE)


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if botactions.verify_user(message.from_user.id) == True:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{message.text}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        bot.send_message(message.from_user.id, response.choices[0].text)
    else:
        bot.send_message(message.from_user.id, "ACCESS DENIED")


if __name__ == '__main__':
    start_bot()

