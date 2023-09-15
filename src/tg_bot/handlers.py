from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods import SendAnimation

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(
        "Hello meme!")

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"tag {msg.text} {msg.from_user.username}")
    urls = [
        'https://media0.giphy.com/media/puYCXadOGhphDrewiv/giphy.gif?cid=ecf05e47kbg8yf711zojp1qw8xi7t4u3pu16yv3557819zn9&ep=v1_gifs_related&rid=giphy.gif&ct=g',
        'https://media1.giphy.com/media/ICOgUNjpvO0PC/giphy.gif?cid=ecf05e47rr2wdyej6y4x47way13quaopph8byir3w6fjespg&ep=v1_gifs_search&rid=giphy.gif&ct=g',
        'https://media2.giphy.com/media/8vQSQ3cNXuDGo/giphy.gif?cid=ecf05e47kbg8yf711zojp1qw8xi7t4u3pu16yv3557819zn9&ep=v1_gifs_related&rid=giphy.gif&ct=g'
    ]
    for url in urls:
        await msg.answer_animation(url)
    


