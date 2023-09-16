from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods import SendAnimation

from minio import Minio
from minio_class import Minio_client


router = Router()
m = Minio_client('config.ini')

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(
        "Hello meme!")

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"tag {msg.text} {msg.from_user.username}")
    
    animation = m.get_url(f'images/cat1.gif')
    # for i in range(1, 9):
    #     animation = m.get_url(f'cat{i}.gif')
    #     await msg.answer_animation(animation)

    await msg.answer_animation(animation)




