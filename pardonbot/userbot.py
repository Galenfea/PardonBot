"""
A module for interacting with Telegram through bot accounts, which provides
automatic sending of messages, checking account status and managing dialogues.

The module contains the Usbot class, which encapsulates the logic of working with
the Telegram client, as well as functions for processing accounts.
"""
import asyncio
import logging
import random
from dataclasses import dataclass
from logging.config import dictConfig
from typing import List

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.patched import Message
from telethon.tl.types import KeyboardButton, ReplyKeyboardMarkup

from config import config, log_config
from custom_features.client_requests import async_clear_bot_history
from custom_features.safe_telegram_client import (
    SafeTelegramClient,
    make_telegram_client,
)
from inviter_exceptions.exceptions import ContinueLoop
from modules.pardonbot.message_generator import (
    generate_message_with_proxy,
    parse_proxy,
    random_message,
)
from utils import move_account

dictConfig(log_config)
logger = logging.getLogger(__name__)

MESSAGE_GET_INTERVAL: int = 3
MESSAGE_SEND_INTERVAL = (6, 15,)
START_INTERVAL = (0, config.DELAY_FOR_START_IN_PARDONBOT,)
APPEAL_FOLDER = "appeals_queue"
FREE_ACCOUNTS_FOLDER = "alive"
DEATH_FOLDER = "death"
TEMPORARY_BLOCK_FORLDER = "temporary_block"
GEO_LIMITED_FOLDER = "geo_limited"
NON_APPEAL_FOLDER = "non_appealable"
YOU_BLOCKED_USER_FOLDER = NON_APPEAL_FOLDER + "/you_blocked_user"
NOT_CONNECTED = NON_APPEAL_FOLDER + "/not_connected"
OPENAI_PROXY = parse_proxy(config.OPEN_AI_PROXY)

INITIAL_MESSAGE = (
    "\nI haven't logged into Telegram or participated in public group chats "
    "for a long time. Despite this, I found myself suspected of spamming and "
    "was likely blocked. "
    "I believe this action was unjustified as I haven't engaged in any "
    "inappropriate behavior. Therefore, I kindly request the removal of my "
    "restrictions. Thank you.\n"
)
PROMPT = (
    f"Generate a message similar to '{INITIAL_MESSAGE}' in English, which "
    "states that you haven't been on Telegram for a long time, haven't "
    "participated in group chats, and haven't done anything that violates the "
    "rules. Ask to have restrictions removed. Add emotionality and "
    "individuality to the message. Make sure the message looks like it was "
    "written by a person and does not include any placeholders like "
    "[Your Name] etc, and does not look like a formal letter. "
    "It should look like an informal chat message. And don't use 'Hey there'"
)


@dataclass
class NonAppealableCondition:
    limit: str
    destination_folder: str
    description: str


class UserBot:

    START = "/start"
    TARGET_BUTTONS_MESSAGES: tuple[str, ...] = (
        "This is a mistake",
        "Yes",
        "No! Never did that!",
        "Это ошибка",
        "Да",
        "Нет, ничего подобного не было.",
    )
    NO_LIMITS = (
        "Ваш аккаунт свободен от каких-либо ограничений",
        "no limits are currently applied to your account",
    )
    TEMPORARY_BLOCK = (
        "ave confirmed the report and your account is now limited until",
        "Ограничения будут автоматически сняты",
    )
    GEO_LIMITED = (
        "излишне сурово реагирует на некоторые номера телефонов",
    )
    BOT_FINAL_WORD = (
        "Пожалуйста, расскажите подробнее о Вашей ситуации",
        "Please write me some details about your case",

    )
    ALREADY_SUBMITED = (
        "You've already submitted a complaint recently.",
    )
    CONDITIONS = (
        NonAppealableCondition(
            NO_LIMITS,
            FREE_ACCOUNTS_FOLDER,
            "уже свободен от ограничений"
        ),
        NonAppealableCondition(
            TEMPORARY_BLOCK,
            TEMPORARY_BLOCK_FORLDER,
            "будет освобождён от ограничений автоматически"
        ),
        NonAppealableCondition(
            GEO_LIMITED,
            GEO_LIMITED_FOLDER,
            "ограничен по территориальному признаку"
        ),
    )
    APPEAL_SENT = NonAppealableCondition(
        ALREADY_SUBMITED,
        APPEAL_FOLDER,
        "уже подал аппеляцию и ожидает решения"
    )

    def __init__(
        self,
        account: str,
        source_folder: str,
        interlocutors_name: str,
        prompt: str = PROMPT,
        initial_message: str = INITIAL_MESSAGE,
    ):
        self.account_needs_moving: bool = False
        self.destination_folder: str = ""
        self.account = account
        logger.debug(f"self.account: {self.account}")
        self.source_folder = source_folder
        logger.debug(
            f"{self.account} | self.source_folder: {self.source_folder}"
        )
        self.interlocutors_name = interlocutors_name
        self.initial_message: str = initial_message
        self.prompt: str = prompt
        try:
            # Клиент для аккаунта
            self.client = make_telegram_client(
                account=self.account,
                source_folder=self.source_folder,
            )
            self.me = None
            logger.debug(f"{self.account} | self.me: {self.me}")
        except Exception as e:
            logger.debug(f"{self.account} | " f"Client create error: {e}")

    async def disconnect_move_account(self):
        await self.client.disconnect()
        if self.account_needs_moving:
            move_account(
                self.source_folder, self.destination_folder, self.account
            )

    async def wait_in_interval(self, start: int, end: int):
        await asyncio.sleep(random.randint(start, end))

    async def chek_is_connected(self) -> bool:
        """
        Проверяет, подключен ли клиент к Telegram.

        Returns:
            bool: True если клиент подключен, False в противном случае.
        """
        try:
            is_connected = self.client.is_connected()
            logger.debug(
                f"{self.account} | "
                f"Клиент подключён? {is_connected}"
            )
        except ContinueLoop as e:
            logger.error(
                f"{self.account} | "
                f"Аккаунт вышел из сессии {e}"
            )
            is_connected = False
        return is_connected

    async def chek_account(self) -> bool:
        """
        Проверяет, авторизован ли пользователь в Telegram.

        Returns:
            bool: True если пользователь авторизован, False в противном случае.
        """
        if await self.chek_is_connected():
            logger.debug(f"{self.account} | is_user_authorized?")
            return await self.client.is_user_authorized()
        return False

    async def connect_and_get_me(self) -> bool:
        """
        Подключается к клиенту и получает информацию о текущем пользователе.
        """
        logger.debug(f"{self.account} | Start")
        try:
            await self.client.connect()
            logger.debug(
                f"{self.account} | "
                f"Подключение"
            )
        except (*SafeTelegramClient.HANDLED_ERRORS, ContinueLoop) as e:
            logger.error(
                f"{self.account} | "
                f"Ошибка сессии: {e}"
            )
            self.account_needs_moving = True
            self.destination_folder = DEATH_FOLDER
            return False
        if await self.chek_account():
            self.me = await self.client.get_me()
            logger.debug(
                f"{self.account} | self.me: {self.me}"
            )
            logger.debug(f"{self.account} | Вошли как {self.me.username}")
            return True
        else:
            logger.debug(f"{self.account} | Клиент не подключён| не залогинен")
            self.account_needs_moving = True
            self.destination_folder = NOT_CONNECTED
            return False

    async def get_keyboard_buttons(self, message: Message):
        """
        Проверяет наличие и содержание клавиатурных кнопок в сообщении.

        Args:
            message (Message): Сообщение, содержащее клавиатурные кнопки.

        Returns:
            list[str]: список текстовых значений кнопок.
        """
        keyboard_buttons_texts: list[str] = []
        if message.reply_markup and isinstance(
            message.reply_markup, ReplyKeyboardMarkup
        ):
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if isinstance(button, KeyboardButton):
                        keyboard_buttons_texts.append(button.text)
        logger.debug(
            f"{self.account} | "
            f"Клавиатурные кнопки: {keyboard_buttons_texts}"
        )
        return keyboard_buttons_texts

    async def _send_message_to_not_blocked_agent(self, message: str):
        """
        Отправь сообщение и жди ответа.

        Args:
            message (str): Сообщение для отправки.

        Returns:
            tuple[str | Any | None, list[str]]: Текст ответного сообщения и
            список текстов кнопок клавиатуры.

        Raises:
            YouBlockedUserError: Если бот заблокирован пользователем.
        """
        logger.debug(f"{self.account} | Start")
        await self.wait_in_interval(*MESSAGE_SEND_INTERVAL)
        try:
            await self.client.send_message(self.interlocutors_name, message)
            logger.debug(
                f"{self.account} | Отправлено сообщение: {message[:5]}"
            )
        except YouBlockedUserError as e:
            logger.error(
                f"{self.account} | Бот заблокирован: {e}"
            )
            self.account_needs_moving = True
            self.destination_folder = YOU_BLOCKED_USER_FOLDER
            raise YouBlockedUserError(e)

    async def _get_response_from_interlocutor(self):
        while True:
            await asyncio.sleep(MESSAGE_GET_INTERVAL)
            response: Message | List[Message] = await self.client.get_messages(
                self.interlocutors_name, limit=1
            )

            if isinstance(response, Message):
                logger.debug(
                    f"{self.account} | Одиночное сообщение"
                )
                reply_message = response
            elif isinstance(response, list) and response:
                logger.debug(
                    f"{self.account} | Список сообщений"
                )
                reply_message = response[0]
            else:
                continue

            # Фильтрация сообщений, отправленных ботом
            if reply_message.sender_id != self.me.id:
                # Проверка обычных клавиатурных кнопок
                keyboard_buttons_texts = await self.get_keyboard_buttons(
                    reply_message
                )
                return (reply_message.text, keyboard_buttons_texts,)

    async def send_message_and_wait_for_response(self, message: Message):
        await self._send_message_to_not_blocked_agent(message)
        return await self._get_response_from_interlocutor()

    async def generate_background_message(self):
        """
        Генерирует дополнительное сообщение.

        Returns:
            str: Дополнительное сообщение на основе текущего языка.
        """
        message = await generate_message_with_proxy(
            prompt=self.prompt,
            initial_message=self.initial_message,
            proxy=OPENAI_PROXY,
        )
        if message is None:
            message = await random_message()
        return message

    async def is_appeal_not_available(
        self,
        message: str,
        disallowed_phrases: str,
        destination_folder: str,
    ) -> bool:
        """
        Проверяет, доступна ли подача апелляции на основе ответа и помечает
        в какую папку нужно переместить аккаунт.

        Args:
            message (str): Ответное сообщение.
            disallowed_phrases (str): Недопустимые фразы.
            destination_folder (str): Папка назначения.

        Returns:
            bool: True если апелляция недоступна, False в противном случае.
        """
        if any(phrase in message for phrase in disallowed_phrases):
            await asyncio.sleep(3)
            self.account_needs_moving = True
            self.destination_folder = destination_folder
            logger.debug(
                f"{self.account} | Будет перемещён в {destination_folder}"
            )
            return True

    async def check_bot_last_word(self, message: str) -> bool:
        logger.debug(f"Последнее сообщение: {message[:5]}")
        is_final_word: bool = (
            any(phrase in message for phrase in UserBot.BOT_FINAL_WORD)
        )
        logger.debug(f"is_final_word: {is_final_word}")
        return is_final_word

    async def choose_button_to_answer(self, answer_buttons: list[str]) -> str:
        """
        Возвращает кнопку из списка допустимых ответов боту,
        если она присутствует в ответных кнопках.

        Args:
            answer_buttons (list[str]): Список кнопок в ответном сообщении.

        Returns:
            str: Кнопка из специального списка, если она найдена, иначе None.
        """
        for button in answer_buttons:
            if button in UserBot.TARGET_BUTTONS_MESSAGES:
                logger.debug(f"Выбранная кнопка: {button}")
                return button
        logger.debug("Ни одна кнопка не выбрана для ответа.")
        return ""

    async def _run_conversation(self):
        """
        Запускает основной цикл общения с ботом.
        """
        logger.debug(f"{self.account} | ->: {UserBot.START}")
        answer, answer_buttons = await self.send_message_and_wait_for_response(
            UserBot.START
        )
        for condition in UserBot.CONDITIONS:
            if await self.is_appeal_not_available(
                answer,
                condition.limit,
                condition.destination_folder
            ):
                print(f"{self.account} | {condition.description}")
                return
        logger.debug(
            f"{self.account} | <- {self.interlocutors_name}: {answer}"
        )
        # ВНИМАНИЕ while NOT
        count: int = 0
        while not await self.check_bot_last_word(answer):
            if count > 10:
                print(f"{self.account} | SpamBot не воспринимает ответы.")
                break
            count += 1
            if await self.is_appeal_not_available(
                answer,
                UserBot.APPEAL_SENT.limit,
                UserBot.APPEAL_SENT.destination_folder
            ):
                print(f"{self.account} | {UserBot.APPEAL_SENT.description}")
                return
            logger.debug(
                f"{self.account} | "
                f"Кнопки для нажатия: {answer_buttons}"
            )
            target_button = await self.choose_button_to_answer(
                answer_buttons
            )
            logger.debug(
                f"{self.account} | "
                f" -> {self.interlocutors_name}: {target_button}"
            )
            if target_button:
                answer, answer_buttons = (
                    await self.send_message_and_wait_for_response(
                        target_button
                    )
                )
                logger.debug(
                    f"{self.account} | "
                    f" <- {self.interlocutors_name}: {answer}"
                )
        else:
            # Генерируем и добавляем дополнительное сообщение с помощью ИИ
            last_message = await self.generate_background_message()
            answer, answer_buttons = (
                await self.send_message_and_wait_for_response(
                    last_message
                )
            )
            logger.debug(
                f"{self.account} | "
                f" <- {self.interlocutors_name}: {answer}"
            )
            self.account_needs_moving = True
            self.destination_folder = APPEAL_FOLDER
            print(
                f"{self.account} "
                f"Подал аппеляцию и будет перемещён в папку {APPEAL_FOLDER}"
            )
            logger.debug(
                f"{self.account} "
                f"Подал аппеляцию и будет перемещён в папку {APPEAL_FOLDER}"
            )

    async def get_me_and_run_conversation(self):
        """
        Запускает цикл общения с ботом с обработкой исключений.
        """
        # На случай, если админы реально вручную рассматривают заявки на вывод
        # из блока сделаем интервал между подключением к ботам подачами.
        await self.wait_in_interval(*START_INTERVAL)
        if await self.connect_and_get_me():
            try:
                logger.debug(
                    f"{self.account} | "
                    f"Запускается диалог"
                )
                await self._run_conversation()
                if config.DELETE_DIALOG_SPAMBOT.lower().startswith('y'):
                    await async_clear_bot_history(
                        self.client, self.interlocutors_name
                    )
            except YouBlockedUserError as e:
                self.account_needs_moving = True
                self.destination_folder = YOU_BLOCKED_USER_FOLDER
                logger.error(
                    f"{self.account} | Бот заблокирован: {e}"
                )
                print(
                    f"{self.account} | "
                    f"Ошибка: {self.interlocutors_name} "
                    f"заблокирован пользователем."
                )
        else:
            logger.error(
                f"{self.account} | "
                "Аккаунт вышел из сессии, не подключён, "
                "или уже запущен на другом ip."
            )
            print(
                f"{self.account} | "
                "Аккаунт вышел из сессии, не подключён, "
                "или уже запущен на другом ip."
            )
        return await self.disconnect_move_account()
