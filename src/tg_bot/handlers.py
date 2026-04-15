from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.tg_bot.services import Services

router = Router()
service = Services()


@router.message(Command("start"))
async def start(message):
    text = f"""
        HSE MOEX Диплом telegram-бот.
        Доступные команды:
        1. /instrument_search name - поиск secid инструмента по ilike имени;
        2. /index_search name - поиск secid индекса по ilike имени;
        3. /instrument_current_price secid - текущая цена инструмента по secid;
        4. /index_current_price secid - текущая цена индекса по secid;
    """
    await message.answer(text)


@router.message(Command("instrument_search"))
async def instrument_search(message):
    name = message.text.split()[1]
    data = service.get_instrument_secid_by_name(name)
    text = "\n\n".join(f"<b>{row[0]}</b> - {row[1]}\n<i>{row[2]}</i>" for row in data)
    await message.answer(text, parse_mode="HTML")


@router.message(Command("index_search"))
async def index_search(message):
    name = message.text.split()[1]
    data = service.get_index_secid_by_name(name)
    text = "\n\n".join(f"<b>{row[0]}</b> - {row[1]}" for row in data)
    await message.answer(text, parse_mode="HTML")

@router.message(Command("instrument_current_price"))
async def instrument_current_price(message):
    secid = message.text.split()[1]
    data = service.get_instrument_current_price(secid)
    data = data[0] # TODO
    text = f"""
secid: <b>{data[0]}</b>
price: <b>{data[1]}</b>
volume: {data[2]}
change: {data[3]}
trading_status: {data[4]}
    """
    await message.answer(text, parse_mode="HTML")


@router.message(Command("index_current_price"))
async def index_current_price(message):
    secid = message.text.split()[1]
    data = service.get_index_current_price(secid)
    data = data[0] # TODO
    text = f"""
secid: <b>{data[0]}</b>
board: {data[1]}
current_value: <b>{data[2]}</b>
open_value: {data[3]}
last_value: {data[4]}
change_percent: {data[5]}
change_points: {data[6]}
high: {data[7]}
low: {data[8]}
volume: {data[9]}
capitalization: {data[10]}
    """
    await message.answer(text, parse_mode="HTML")
