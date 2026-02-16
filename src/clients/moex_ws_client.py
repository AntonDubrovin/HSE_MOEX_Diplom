import asyncio
import json
import uuid

from stomp.utils import Frame, convert_frame, parse_frame
from websockets import ConnectionClosed, connect


async def send_frame(websocket, cmd, headers):
    frame = Frame(cmd, headers=headers)
    await websocket.send(b"".join(convert_frame(frame)))


async def receive_message(websocket):
    message = await websocket.recv()
    return parse_frame(message)


async def connect_stomp(websocket, domain, login, passcode):
    await send_frame(websocket, "CONNECT", {"domain": domain, "login": login, "passcode": passcode})
    frame = await receive_message(websocket)
    if frame.cmd != "CONNECTED":
        raise ConnectionRefusedError(
            f"STOMP authentication failed; {frame.headers.get('message', 'No error message')}"
        )
    return json.loads(frame.body.decode("utf8").strip("\0"))


async def subscribe_to_topic(websocket, destination, selector):
    subscribe_header = {
        "id": str(uuid.uuid4()),
        "destination": destination,
        "selector": selector,
    }
    await send_frame(websocket, "SUBSCRIBE", subscribe_header)


async def moex_websocket(
    url, credentials, destination, selector, handler, moex_ws_mapper, postgres_dao
):
    async with connect(url, subprotocols=["STOMP"]) as websocket:
        try:
            metadata = await connect_stomp(
                websocket,
                credentials["domain"],
                credentials["login"],
                credentials["passcode"],
            )
            print("Connected:", metadata)

            await subscribe_to_topic(websocket, destination, selector)
            print(f"Subscribed: {destination}")

            while True:
                frame = await receive_message(websocket)
                if frame.cmd == "MESSAGE":
                    body = json.loads(frame.body.decode("utf8").strip("\0"))
                    handler(body, moex_ws_mapper, postgres_dao)

        except ConnectionClosed:
            print("Connection closed")
        except Exception as e:
            print(f"Error: {e}")


def get_securities(body, moex_ws_mapper, postgres_dao):
    columns = body["columns"]
    rows = body["data"]
    print(f"columns len: {len(columns)}")
    print(f"rows len: {len(rows)}")

    for row in rows:
        ws_data = dict(zip(columns, row))
        current_price = moex_ws_mapper.to_current_price(ws_data)
        if current_price:
            postgres_dao.insert_current_prices([current_price])
