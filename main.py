import karelia
import sys
import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler('present.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    global message
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

present_bot = karelia.bot(["Present", "present"], "xkcd")

present_bot.stock_responses["short_help"] = "I track attendence"
present_bot.stock_responses[
    "long_help"
] = "I keep a running, accurate tally of which people are connected. (The tally converges closer to accurate with both time and activity.) Use !present to find out. Made by @PouncySilverkitten."

present_bot.connect()
present = {}

user_list = []
bot_list = []
last_nick = "Present"

while True:
    message = present_bot.parse()
    try:
        if message.type == "nick-event":
            present[message.data.id] = message.data.to
        elif message.type == "join-event":
            present[message.data.id] = message.data.name
        elif message.type == "send-event":
            present[message.data.sender.id] = message.data.sender.name
        elif message.type == "part-event":
            del present[message.data.id]
    except KeyError:
        pass

    user_list = sorted([present[key] for key in present.keys() if not key.startswith("bot:")], key = lambda x: x.lower())
    bot_list = sorted([present[key] for key in present.keys() if key.startswith("bot:")], key = lambda x: x.lower())
    
    if message.type == "send-event":
        if message.data.content == "!present":
            users = '\n'.join(user_list)
            bots = '\n'.join(bot_list)
            present_bot.reply(f"{users}\n\n--------------------\n\n{bots}")
        
        elif 
        elif message.data.content.startswith("!present @"):
            find_presence = message.data.content.split("@")[1].strip()
            if find_presence.lower() in [user.lower() for user in user_list]:
                present_bot.reply(f"{find_presence} is present.")
            else:
                present_bot.reply(f"{find_presence} is not present.")

    

    this_nick = f"Present ({len(user_list)}|{len(bot_list)+1})"
    if this_nick != last_nick:
        present_bot.change_nick(this_nick)
        last_nick = this_nick