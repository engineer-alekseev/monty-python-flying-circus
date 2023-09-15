import asyncio

from logging import getLogger

from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from utils import (
    generate_conf_path,
    read_conf_file,
    init_logger
)

from handlers import (
    router
)

logger = init_logger()

conf_path = generate_conf_path()
conf = read_conf_file(conf_path)

async def main():
    bot = Bot(token=conf['tg']['token'], parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())


if __name__ == "__main__":
    logger.info("starting MemesExpressBot")
    asyncio.run(main())