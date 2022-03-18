import os
import sys
from http import HTTPStatus

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN', default='')
if len(TELEGRAM_TOKEN) == 0:
    print(
        'Отсутствует токен. Укажите TELEGRAM_TOKEN в .env файле',
        file=sys.stderr,
    )
    sys.exit(1)

TELEGRAM_CHAT_ID: str = os.getenv('TELEGRAM_CHAT_ID', default='')
if len(TELEGRAM_CHAT_ID) == 0:
    print(
        'Отсутствует chat_id. Укажите TELEGRAM_CHAT_ID в .env файле',
        file=sys.stderr,
    )
    sys.exit(1)

RETRY_TIME = int(os.getenv('RETRY_TIME', default='600'))

PRACTICUM_TOKEN: str = os.getenv('PRACTICUM_TOKEN', default='')
if len(TELEGRAM_TOKEN) == 0:
    print(
        'Отсутствует токен api. Укажите PRACTICUM_TOKEN в .env файле',
        file=sys.stderr,
    )
    sys.exit(1)

ENDPOINT: str = os.getenv('ENDPOINT', default='')
if len(ENDPOINT) == 0:
    print(
        'Отсутствует url ENDPOINTa практикума. Укажите ENDPOINT в .env файле',
        file=sys.stderr,
    )
    sys.exit(1)

