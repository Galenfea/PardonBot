import asyncio
import logging
from logging.config import dictConfig

from config import log_config
from modules.pardonbot.userbot import UserBot
from utils import read_accounts

dictConfig(log_config)
logger = logging.getLogger(__name__)


BOT_NAME: str = "SpamBot"
SOURCE_FOLDER: str = "spamblock"


async def handle_account(account, source_folder, interlocutors_name):
    """
    Обрабатывает аккаунт, запускает цикл общения с ботом.

    Args:
        account (str): Телефонный номер аккаунта.
        source_folder (str): Исходная папка.
        interlocutors_name (str): Имя собеседника (бота).
    """
    userbot = UserBot(account, source_folder, interlocutors_name)
    await userbot.get_me_and_run_conversation()


async def main(auto_run: bool = False):
    """
    Запускает основной поток выполнения, обрабатывает список аккаунтов.
    """
    logger.debug("============ PardonBot Version 1.0 START ============")
    print("============ PardonBot Version 1.0 ============")
    accounts = read_accounts(SOURCE_FOLDER)
    accounts_len = len(accounts)
    print(
        f"В папке {SOURCE_FOLDER} находится {accounts_len} аккаунттов.\n"
    )
    if not auto_run:
        input("Нажмите клавишу, чтобы запустить вывод из спамблока.")
    tasks = [
        handle_account(account, SOURCE_FOLDER, BOT_NAME)
        for account in accounts
    ]
    await asyncio.gather(*tasks)
    logger.debug("============ PardonBot Version 1.0 END ============")
