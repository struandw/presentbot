import karelia
import pprint

present_bot = karelia.bot("Present", "xkcd")

present_bot.stock_responses["short_help"] = "I track attendence"
present_bot.stock_responses[
    "long_help"
] = "I keep a running, accurate tally of which people are connected. (The tally converges closer to accurate with both time and activity.) Use !present to find out."

present_bot.connect()
present = {}

user_list = []
bot_list = []
last_nick = "Present"

while True:
    message = present_bot.parse()
    #pprint.pprint(message.packet)
    try:
        if message.type == "nick-event":
            present.pop(message.packet["data"]["from"], None)
            present[message.data.to] = message.data.id.split(":")[0]
        else:
            user = (message.data.sender.name, message.data.sender.id.split(":")[0])
    except AttributeError:
        continue

    if message.type == "join-event":
        present[user[0]] = user[1]
        if user[1] == "bot":
            bot_list.append(user[0])
        else:
            user_list.append(user[0])
    elif message.type == "part-event":
        if user[1] == "bot":
            bot_list.pop(user[0], None)
        else:
            user_list.pop(user[0], None)
    
    if message.type == "send-event":
        if user[1] == "bot":
            if user[0] not in bot_list:
                bot_list.append(user[0])
        else:
            if user[0] not in user_list:
                user_list.append(user[0])
            if message.data.content == "!present":
                user_list.sort(key = lambda x: x.lower())
                bot_list.sort(key = lambda x: x.lower())
                users = '\n'.join(user_list)
                bots = '\n'.join(bot_list)
                present_bot.reply(f"{users}\n\n--------------------\n\n{bots}")

    this_nick = f"Present ({len(user_list)}|{len(bot_list)})"
    if this_nick != last_nick:
        present_bot.change_nick(this_nick)
        last_nick = this_nick