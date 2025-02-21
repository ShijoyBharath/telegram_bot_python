import os
from dotenv import load_dotenv
import telebot
import requests

def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()


def main():
    print("Bot running...")
    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    bot = telebot.TeleBot(TOKEN)

    def fetch_horoscope(message, sign):
        day = message.text
        horoscope = get_daily_horoscope(sign, day)
        data = horoscope["data"]
        horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
        bot.send_message(message.chat.id, "Here's your horoscope!")
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

    def day_handler(message):
        sign = message.text
        text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
        sent_msg = bot.send_message(
            message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(
            sent_msg, fetch_horoscope, sign.capitalize())

    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "Horobot is ready to go!")

    @bot.message_handler(commands=['horoscope'])
    def sign_handler(message):
        text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, day_handler)

    bot.infinity_polling()


if __name__ == "__main__":
    main()
