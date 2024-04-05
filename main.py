#! /usr/bin/env python3

import sys

import argparse
from datetime import datetime

from telegram.client import Telegram

def err(message):
    print("ERROR: %s" % message, file=sys.stderr)
    exit(1)

def pr_text(text):
    if not isinstance(text, str):
        err("non-string: %s" % (text))

    print(text)

def pr(message):
    if message['@type'] == "message":
        content_type = message['content']['@type']

        if content_type == "messageText":
            pr_text(message['content']['text']['text'])
        elif content_type == "messagePhoto":
            pr_text(message['content']['caption']['text'])
        elif content_type == "messageVideo":
            pr_text(message['content']['caption']['text'])
        elif content_type == "messageDocument":
            pr_text(message['content']['caption']['text'])
        elif content_type == "messageAnimatedEmoji":
            pr_text(message['content']['emoji'])
        elif content_type == "messageSticker":
            pr_text(message['content']['sticker']['emoji'])
        elif content_type == "messageCall":
            pr_text("// call")
        elif content_type == "messageVideoNote":
            pr_text("// video note")
        elif content_type == "messageContactRegistered":
            pr_text("// contact registered")
        elif message['@type'] == "sticker":
            pr_text(message['emoji'])
        elif content_type == "messageUnsupported":
            pr_text("// message unsupported")
        elif content_type == "messagePoll":
            pr_text(message['content']['poll']['question'])
        elif content_type == "messageChatJoinByRequest":
            pr_text("// chat join by request")
        elif content_type == "messageAnimation":
            pr_text("// animation")
        elif content_type == "messageChatAddMembers":
            pr_text("// chat add members")
        elif content_type == "messageChatChangePhoto":
            pr_text("// chat change photo")
        else:
            err("unknown message type: %s in %s" % (content_type, message))
    else:
        err("unknown type: %s in %s" % (message['@type'], message))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--api_id", help="API id")
    parser.add_argument("-a", "--api_hash", help="API hash")
    parser.add_argument("-p", "--phone", help="Phone")
    parser.add_argument("-c", "--chat", help="Chat name")
    parser.add_argument("-d", "--delete", help="Delete messages", default=False, action='store_true')

    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        database_encryption_key='rnd',
        phone=args.phone
    )
    # you must call login method before others
    tg.login()

    found_chat_id = None
    chats = tg.get_chats()
    chats.wait()
    for chat_id in chats.update['chat_ids']:
        chat = tg.get_chat(chat_id)
        chat.wait()
        if chat.update['title'] == args.chat:
            found_chat_id = chat_id
            break

    if found_chat_id is None:
        err("chat not found: %s" % (args.chat))

    me = tg.get_me()
    me.wait()
    me_id = me.update['id']

    chat = tg.get_chat(chat_id)
    chat.wait()

    from_message_id = 0
    while True:
        chat_history = tg.get_chat_history(chat_id, from_message_id=from_message_id)
        chat_history.wait()
        if chat_history.update['total_count'] < 1:
            break

        for message in chat_history.update['messages']:
            if ('user_id' in message['sender_id']) and (message['sender_id']['user_id'] == me_id):
                pr_text("%s" % (datetime.fromtimestamp(message['date'])))
                pr(message)
                if args.delete:
                    tg.delete_messages(chat_id, [message['id']])

            from_message_id = message['id']

    tg.stop()
