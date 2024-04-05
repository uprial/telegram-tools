Read and delete your messages in Telegram groups.

Read my messages:

    ./main.py --api_id ??? --api_hash ??? --phone '???' --chat 'Chat' > 'Chat.txt'


Read AND DELETE my messages:

    ./main.py --api_id ??? --api_hash ??? --phone '???' --chat 'Chat' --delete > 'Chat.txt'

Get API id and hash: https://core.telegram.org/api/obtaining_api_id

Bugfix for arm64: https://github.com/alexander-akhmetov/python-telegram/issues/377
