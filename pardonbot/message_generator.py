import json
import logging
import random
import re
from logging.config import dictConfig

import aiofiles
import aiohttp
from openai import RateLimitError

from config import config, log_config

dictConfig(log_config)
logger = logging.getLogger(__name__)

if not config.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# openai_async_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

FILENAME = "./logs/gpt_messages.json"
OPENAI_API_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


def parse_proxy(proxy_str: str) -> dict[str, str | int]:
    """
    Парсит прокси строку формата host:port:username:password.

    Args:
        proxy_str (str): Прокси строка для парсинга.

    Returns:
        dict: Словарь с компонентами прокси (host, port, username, password).
    """
    try:
        host, port, username, password = proxy_str.split(":")
        return {
            "PROXY_URL": host,
            "PROXY_PORT": int(port),
            "PROXY_USERNAME": username,
            "PROXY_PASSWORD": password,
        }
    except ValueError:
        raise ValueError(
            "Некорректный формат прокси строки. "
            "Ожидается формат host:port:username:password."
        )


async def add_message_to_json(
    message: str | None,
    filename: str = FILENAME
) -> None:
    """
    Добавляет сообщение в JSON файл.

    Args:
        message (str | None): Сообщение, которое нужно добавить в файл.
        filename (str): Имя файла для сохранения сообщения.

    """
    if message is None:
        return
    try:
        async with aiofiles.open(filename, "a", encoding="utf-8") as file:
            json_message = json.dumps({"message": message}, ensure_ascii=False)
            await file.write(json_message + "\n")
        logger.debug("Message added to messages.json")
    except Exception as e:
        logger.debug(
            f"An error occurred while saving the message to JSON: {e}"
        )


async def read_messages_from_json(filename: str = FILENAME) -> list[str]:
    """
    Считывает сообщения из JSON файла.

    Args:
        filename (str): Имя файла для чтения сообщений.

    Returns:
        list: Список сообщений, считанных из файла.
    """
    messages = []
    try:
        async with aiofiles.open(filename, "r", encoding="utf-8") as file:
            async for line in file:
                message = json.loads(line)
                messages.append(message['message'])
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
    except Exception as e:
        logger.error(f"An error occurred while reading the file: {e}")
    return messages


async def random_message(initial_message: str) -> str:
    logger.debug("Start")
    messages = await read_messages_from_json()
    random_message: str = initial_message
    if messages:
        # Select a random message
        random_message = random.choice(messages)
        logger.debug("Выбрано случайное сообщение")
    else:
        logger.debug("Нет сообщений в файле")
        print("Нет сообщений в файле, отправлено оригинальное сообщение")
    logger.debug("End")
    return random_message


def clean_message_from_your_name(message: str) -> str:
    """
    Очисть входяющую строку от признаков шаблона, таких как [Your Name] и
    поставь точку в конце вместо запятой.

    Args:
        message (str): Входящая строка, которую нужно очистить.

    Returns:
        str: Очищенная строка.
    """
    logger.debug("Start")
    pattern = r"\\n\[Your Name\]|\[Your Name\][^\s]|Your Name[^\s]|\[|\]"
    message = re.sub(pattern, "", message)
    message = message.strip()
    if message.endswith(','):
        message = message[:-1] + '.'
    logger.debug("End")
    return message


async def generate_message_with_proxy(
    prompt: str, initial_message: str, proxy: dict[str, str | int],
) -> str:
    """
    Генерирует сообщение похожее на initial_message на основе предоставленного
    запроса.

    Args:
        prompt (str): Запрос для генерации сообщения.
        initial_message (str): Исходное сообщение для выбора случайного ответа
        при ошибке.
        proxy (dict[str, str | int]): словарь с настройками прокси.

    Returns:
        str: Сгенерированное сообщение.
    """
    response = None

    logger.debug(f"OPENAI_PROXY: {proxy}")
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        proxy_auth = aiohttp.BasicAuth(
            login=proxy["PROXY_USERNAME"],
            password=proxy["PROXY_PASSWORD"]
        )
        async with aiohttp.ClientSession(connector=connector) as session:
            headers = {
                "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            }
            proxy_url = (
                f"http://{proxy['PROXY_URL']}:"
                f"{proxy['PROXY_PORT']}"
            )
            async with session.post(
                OPENAI_API_CHAT_COMPLETIONS_URL,
                json=payload,
                headers=headers,
                proxy=proxy_url,
                proxy_auth=proxy_auth
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    response = data['choices'][0]['message']['content']
                    if isinstance(response, str):
                        logger.debug("Начинаем чистить строку")
                        # Чистим строку от шаблона, который любит chat gpt
                        response = clean_message_from_your_name(response)
                    await add_message_to_json(response)
                    logger.debug("Сообщение сгенерировано")
                else:
                    logger.error(f"Failed to generate message: {resp.status}")
    except RateLimitError as e:
        logger.error(f"Rate limit error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    if response is None:
        response = await random_message(initial_message)
    return response


# async def generate_message(prompt: str, initial_message: str) -> str:
#    """
#    Генерирует сообщение похожее на initial_message на основе предоставленного
#    запроса.
#
#    Args:
#        prompt (str): Запрос для генерации сообщения.
#
#    Returns:
#        str: Сгенерированное сообщение.
#    """
#    response = None
#    try:
#        chat_completion = await openai_async_client.chat.completions.create(
#            messages=[
#                {
#                    "role": "user",
#                    "content": prompt,
#                }
#            ],
#            model="gpt-3.5-turbo",
#        )
#        response = chat_completion.choices[0].message.content
#        await add_message_to_json(response)
#        logger.debug("Сообщение сгенерировано")
#    except RateLimitError as e:
#        logger.error(f"Rate limit error: {e}")
#    except Exception as e:
#        logger.error(f"An error occurred: {e}")
#    if response is None:
#        response = await random_message(initial_message)
#    return response
