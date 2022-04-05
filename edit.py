import karelia
import time

editbot = karelia.bot("Editor", "xkcd")
editbot.stock_responses["short_help"] = "s/fix/typos"
editbot.stock_responses["long_help"] = """Use me to edit your messages and fix your typos. Evidence of your change will be public. 

Make a child message to your message, with the syntax s/wrong/right, where wrong is the original text and right is the correction.

[Pouncy Silverkitten] This example message has a typos.
    [Pouncy Silverkitten] s/typos/typo

This example will become:

[Pouncy Silverkitten] This example message has a typo.

As you may have inferred, this bot was built by @PouncySilverkitten and forms part of the Karelian Legion.
"""
editbot.connect()

login_command = {
    "type": "login",
    "data": {
        "namespace": "email",
        "id": "struan@duncan-wilson.co.uk",
        "password": "PwZykL^mtUtJpR6JXcwghxxr95trt6"
    }
}

edit_command = {
    "type": "edit-message",
    "data": {
        "id": "07dte1vvdxkow",
        "previous_edit_id": "",
        "content": "",
        "delete": False,
        "announce": True,
    }
}

request_parent_command = {
    "type": "get-message",
    "data": {
        "id": "",
    }
}

if not editbot.logged_in:
    editbot.send(login_command)

backoff = 1

while True:
    try:
        backoff = 1
        while True:
            message = editbot.parse()
            
            if message.type == "login-reply" and message.data.success:
                editbot.logged_in = True
                editbot.disconnect()
                editbot.connect()

            elif message.type == "send-event" and message.data.content.startswith("s/") and hasattr(message.data, "parent"):
                edit_requester = message.data.sender.id
                edit_requested_on = message.data.parent
                requested_edit = message.data.content[2:].split("/")

                request_parent_command["data"]["id"] = edit_requested_on
                editbot.send(request_parent_command)
                while message.type != "get-message-reply":
                    message = editbot.parse()

                if message.data.sender.id == edit_requester:
                    edit_command['data']["id"] = edit_requested_on
                    if hasattr(message.data, "previous_edit_id"):
                        edit_command["data"]["previous_edit_id"] = message.data.previous_edit_id
                    edit_command["data"]["content"] = message.data.content.replace(requested_edit[0], requested_edit[1])
                    edit_command["data"]["delete"] = False
                    editbot.send(edit_command)
    except:
        time.sleep(backoff)
        backoff *= 2
        editbot.connect()