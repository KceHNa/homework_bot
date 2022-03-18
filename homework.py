import logging
import sys
import time
from http import HTTPStatus
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

from exceptions import DateError, NotListOrDict, ResponseNoKey, \
    EndpointNotAvailable, ResponseApiError
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, PRACTICUM_TOKEN,\
    RETRY_TIME, ENDPOINT

load_dotenv()

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    __file__ + '.log',
    maxBytes=50000000,
    backupCount=5
)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'
)
# Применяем форматер к хэндлеру
handler.setFormatter(formatter)


def send_message(bot, message):
    """Отправляет сообщение в Telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Бот отправил сообщение "{message}"')
    except Exception as error:
        logger.error(f'Бот не смог отправить сообщение "{message}"')
        raise telegram.error.TelegramError(f'Сообщение не отправлено: {error}')


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
        if response.status_code != HTTPStatus.OK:
            logger.error(f'Яндекс API {ENDPOINT} недоступен.')
            raise EndpointNotAvailable(f'Яндекс API {ENDPOINT} недоступен.')
        return response.json()
    # Ошибка при запросе
    except Exception as error:
        logger.error(f'Ошибка при запросе к Практикум API: {error}')
        raise ResponseApiError(
            f'Ошибка при запросе к Практикум API: {error}'
        )


def check_response(response):
    """Проверяет ответ API на корректность.
    Функция должна вернуть список домашних работ (он мб пустым),
    доступный в ответе API по ключу 'homeworks'.
    """
    # полученный ответ это словарь
    if not isinstance(response, (dict, list)):
        logger.error('Ответ возвращет не список')
        raise NotListOrDict('Ответ возвращет не список')
    # есть ли ключи в этом словаре
    if 'homeworks' and 'current_date' in response:
        logger.info('Ключи есть')
        checked_response = response.get('homeworks')
        if not isinstance(checked_response, list):
            raise NotListOrDict('Ответ homeworks возвращет не список')
    else:
        logger.error('В ответе отсутствуют ключи homeworks или current_date ')
        raise ResponseNoKey('В ответе отсутствуют ключи')
    return checked_response


def parse_status(homework):
    """Извлекает статус работы."""
    homework_name = homework.get('homework_name')
    if homework_name is None:
        homework_name = 'Работа без названия'
    homework_status = homework.get('status')
    if homework_status is None:
        raise KeyError('Отстутсвует статус')
    verdict = HOMEWORK_STATUSES.get(homework_status)
    if verdict is None:
        logger.error('Статус не найден в списке')
        raise KeyError('Статус не найден в списке')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Возвращает True, если все три токена cуществуют."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Проверка и отправка статуса."""
    status_homework = None
    # проверяем передались ли переменные
    if not check_tokens():
        logging.critical('Отсутствуют переменные окружения!')
        sys.exit(1)
    # класс, отвечающий за отправку
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    # Текущее время
    current_timestamp = int(time.time())

    while True:
        try:
            # отправляем время, от которого выкидывает задания
            response = get_api_answer(current_timestamp)
            # проверяем ответ от апи
            check_response(response)
            # берем работу
            homeworks = response.get('homeworks')
            if homeworks:
                homeworks = response.get('homeworks')[0]
                parse_status(homeworks)
                if status_homework != homeworks.get('status'):
                    send_message(bot, parse_status(homeworks))
                else:
                    logger.debug('Статус задания не обновлён.')
                current_date = response.get('current_date')
                if (current_date is not None
                        and int(current_date) < current_timestamp):
                    logger.error('Проверьте время на сервере')
                    raise DateError
            else:
                logger.info('Текущих работ нет')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            time.sleep(RETRY_TIME)

        else:
            logger.info(f'Следующая проверка через {RETRY_TIME}s')

        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
