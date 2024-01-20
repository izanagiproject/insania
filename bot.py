import telegram
import asyncio

#token that can be generated talking with @BotFather on telegram
my_token = '5838292226:AAHSlJxlz0Aw5DNSPerP0R9yxFLNv1xePS4'

async def send(msg, chat_id, token=my_token):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=msg)


# asyncio.run(send("Integrated Smart Network Issue Alarm (InSaNIA), an early detection system that help us to monitor and report any emergency network issues in PTKP real-time, and available 24/7. This message is automated", -1001903139828, my_token))