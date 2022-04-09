import karelia
import pprint

present_bot = karelia.bot(["Present", "present"], "xkcd")

present_bot.stock_responses["short_help"] = "I track attendence"
present_bot.stock_responses[
    "long_help"
] = "I keep a running, accurate tally of which people are connected. (The tally converges closer to accurate with both time and activity.) Use !present to find out. Made by @PouncySilverkitten."

present_bot.connect()
present = {}

user_list = []
bot_list = ["Present"]
last_nick = "Present"

while True:
    message = present_bot.parse()
    #pprint.pprint(message.packet)
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
    
    if message.type == "send-event" and message.data.content == "!present":
        users = '\n'.join(user_list)
        bots = '\n'.join(bot_list)
        present_bot.reply(f"{users}\n\n--------------------\n\n{bots}")

    this_nick = f"Present ({len(user_list)}|{len(bot_list)})"
    if this_nick != last_nick:
        present_bot.change_nick(this_nick)
        last_nick = this_nick