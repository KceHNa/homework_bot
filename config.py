import os
import sys

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN', default='')

TELEGRAM_CHAT_ID: str = os.getenv('TELEGRAM_CHAT_ID', default='')

RETRY_TIME = int(os.getenv('RETRY_TIME', default='600'))

PRACTICUM_TOKEN: str = os.getenv('PRACTICUM_TOKEN', default='')

ENDPOINT: str = os.getenv('ENDPOINT', default='')
if len(ENDPOINT) == 0:
    print(
        'Отсутствует url ENDPOINTa практикума. Укажите ENDPOINT в .env файле',
        file=sys.stderr,
    )
    # sys.exit(1)

HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES: dict = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
