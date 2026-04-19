from aiogram import Router
from aiogram.filters import Command

from src.tg_bot.services import Services

router = Router()
service = Services()


@router.message(Command("start"))
async def start(message):
    text = (
        f"HSE MOEX Диплом telegram-бот.\n"
        f"Доступные команды:\n\n"
        f"1. <b>/instrument_search name</b> \n\t поиск secid инструмента по ilike имени. Пример: \n\t <i>/instrument_search сбер</i>\n\n"
        f"2. <b>/index_search name</b> \n\t поиск secid индекса по ilike имени. Пример: \n\t <i>/index_search мосбиржи</i>\n\n"
        f"3. <b>/instrument_current_price secid</b> \n\t текущая цена инструмента по secid. Пример: \n\t <i>/instrument_current_price SBER</i>\n\n"
        f"4. <b>/index_current_price secid</b> \n\t текущая цена индекса по secid. Пример: \n\t <i>/index_current_price IMOEX</i>\n\n"
        f"5. <b>/trigger_get_instruments_dag</b> \n\t запускает DAG по загрузке всех инструментов.\n\n"
        f"6. <b>/trigger_get_index_dag</b> \n\t запускает DAG по загрузке всех индексов.\n\n"
        f"7. <b>/trigger_get_index_history_dag secid from till</b> \n\t загрузка истории индекса secid с from по till промежуток времени. Пример \n\t <i>/trigger_get_index_history_dag IMOEX 2025-01-01 2026-01-01</i>\n\n"
        f"8. <b>/trigger_get_dividends_dag secid</b> \n\t загрузка дивидендов по secid инструмента. Пример \n\t <i>/trigger_get_dividends_dag SBER</i>\n\n"
        f"9. <b>/trigger_get_daily_aggregates_dag secid from till</b> \n\t загрузка дневных агрегатов по secid инструмента с from по till. Пример: \n\t <i>/trigger_get_daily_aggregates_dag SBER 2025-01-01 2026-01-01</i>\n\n"
        f"10. <b>/trigger_get_candles_dag secid from till interval</b> \n\t загрузка свечей по secid инструмента с from по till с интервалом interval. Пример: \n\t <i>/trigger_get_candles_dag SBER 2025-01-01 2026-01-01 24</i>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("instrument_search"))
async def instrument_search(message):
    try:
        name = message.text.split()[1]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/instrument_search сбер</i>",
            parse_mode="HTML",
        )
    else:
        data = service.get_instrument_secid_by_name(name)

        if data:
            text = "\n\n".join(f"<b>{row[0]}</b> - {row[1]}\n<i>{row[2]}</i>" for row in data)
        else:
            text = f"Не найдено инструмента по sec_name = {name} или short_name = {name}"

        await message.answer(text, parse_mode="HTML")


@router.message(Command("index_search"))
async def index_search(message):
    try:
        name = message.text.split()[1]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/index_search мосбиржи</i>",
            parse_mode="HTML",
        )
    else:
        print(name)
        data = service.get_index_secid_by_name(name)
        print(data)

        if data:
            text = "\n\n".join(f"<b>{row[0]}</b> - {row[1]}" for row in data)
        else:
            text = f"Не найдено индекса по index_name = {name}"

        await message.answer(text, parse_mode="HTML")


@router.message(Command("instrument_current_price"))
async def instrument_current_price(message):
    try:
        secid = message.text.split()[1]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/instrument_current_price SBER</i>",
            parse_mode="HTML",
        )
    else:
        data = service.get_instrument_current_price(secid)

        if data:
            data = data[0]
            text = (
                f"secid: <b>{data[0]}</b>\n"
                f"price: <b>{data[1]}</b>\n"
                f"volume: {data[2]}\n"
                f"change: {data[3]}\n"
                f"trading_status: {data[4]}"
            )
            await message.answer(text, parse_mode="HTML")
        else:
            await message.answer(
                f"Не найдено информации по цене инструмента secid = {secid}", parse_mode="HTML"
            )


@router.message(Command("index_current_price"))
async def index_current_price(message):
    try:
        secid = message.text.split()[1]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/index_current_price IMOEX</i>",
            parse_mode="HTML",
        )
    else:
        data = service.get_index_current_price(secid)

        if data:
            data = data[0]
            text = (
                f"secid: <b>{data[0]}</b>\n"
                f"board: {data[1]}\n"
                f"current_value: <b>{data[2]}</b>\n"
                f"open_value: {data[3]}\n"
                f"last_value: {data[4]}\n"
                f"change_percent: {data[5]}\n"
                f"change_points: {data[6]}\n"
                f"high: {data[7]}\n"
                f"low: {data[8]}\n"
                f"volume: {data[9]}\n"
                f"capitalization: {data[10]}"
            )
            await message.answer(text, parse_mode="HTML")
        else:
            await message.answer(
                f"Не найдено информации по цене индекса secid = {secid}", parse_mode="HTML"
            )


@router.message(Command("trigger_get_instruments_dag"))
async def trigger_get_instruments_dag(message):
    response = service.trigger_dag(dag_id="get_instruments_dag", params={"conf": {}})

    if response.ok:
        text = "Триггер get_instruments_dag прошёл успешно"
    else:
        text = f"Ошибка при триггере get_instruments_dag. Код - {response.status_code}, ошибка - {response.text}"

    await message.answer(text, parse_mode="HTML")


@router.message(Command("trigger_get_index_dag"))
async def trigger_get_index_dag(message):
    response = service.trigger_dag(dag_id="get_index_dag", params={"conf": {}})

    if response.ok:
        text = "Триггер get_index_dag прошёл успешно"
    else:
        text = f"Ошибка при триггере get_index_dag. Код - {response.status_code}, ошибка - {response.text}"

    await message.answer(text, parse_mode="HTML")


@router.message(Command("trigger_get_index_history_dag"))
async def trigger_get_index_history_dag(message):
    try:
        secid = message.text.split()[1]
        from_ = message.text.split()[2]
        till_ = message.text.split()[3]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/trigger_get_index_history_dag IMOEX 2025-01-01 2026-01-01</i>",
            parse_mode="HTML",
        )
    else:
        response = service.trigger_dag(
            dag_id="get_index_history_dag",
            params={"conf": {"secid": secid, "from": from_, "till": till_}},
        )

        if response.ok:
            text = "Триггер get_index_history_dag прошёл успешно"
        else:
            text = f"Ошибка при триггере get_index_history_dag. Код - {response.status_code}, ошибка - {response.text}"

        await message.answer(text, parse_mode="HTML")


@router.message(Command("trigger_get_dividends_dag"))
async def trigger_get_dividends_dag(message):
    try:
        secid = message.text.split()[1]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/trigger_get_dividends_dag SBER</i>",
            parse_mode="HTML",
        )
    else:
        response = service.trigger_dag(
            dag_id="get_dividends_dag",
            params={"conf": {"secid": secid}},
        )

        if response.ok:
            text = "Триггер get_dividends_dag прошёл успешно"
        else:
            text = f"Ошибка при триггере get_dividends_dag. Код - {response.status_code}, ошибка - {response.text}"

        await message.answer(text, parse_mode="HTML")


@router.message(Command("trigger_get_daily_aggregates_dag"))
async def trigger_get_daily_aggregates_dag(message):
    try:
        secid = message.text.split()[1]
        from_ = message.text.split()[2]
        till_ = message.text.split()[3]
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>/trigger_get_daily_aggregates_dag SBER 2025-01-01 2026-01-01</i>",
            parse_mode="HTML",
        )
    else:
        response = service.trigger_dag(
            dag_id="get_daily_aggregates_dag",
            params={"conf": {"secid": secid, "from": from_, "till": till_}},
        )

        if response.ok:
            text = "Триггер get_daily_aggregates_dag прошёл успешно"
        else:
            text = f"Ошибка при триггере get_daily_aggregates_dag. Код - {response.status_code}, ошибка - {response.text}"

        await message.answer(text, parse_mode="HTML")


@router.message(Command("trigger_get_candles_dag"))
async def trigger_get_candles_dag(message):
    try:
        secid = message.text.split()[1]
        from_ = message.text.split()[2]
        till_ = message.text.split()[3]
        interval = int(message.text.split()[4])
    except Exception as e:
        await message.answer(
            "Ошибка в переданных параметрах запроса, повторите запрос. Пример: \n\t <i>//trigger_get_candles_dag SBER 2025-01-01 2026-01-01 24</i>",
            parse_mode="HTML",
        )
    else:
        response = service.trigger_dag(
            dag_id="get_candles_dag",
            params={"conf": {"secid": secid, "from": from_, "till": till_, "interval": interval}},
        )

        if response.ok:
            text = "Триггер get_candles_dag прошёл успешно"
        else:
            text = f"Ошибка при триггере get_candles_dag. Код - {response.status_code}, ошибка - {response.text}"

        await message.answer(text, parse_mode="HTML")
