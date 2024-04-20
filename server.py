
import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Set

from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol
import time
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
class Broker:
    def __init__(self):
        self.ws_listeners: Set[WebSocketServerProtocol] = set()
        self.counter = 0
        self.last_time = None

    async def add_ws(self, websocket: WebSocketServerProtocol):
        self.ws_listeners.add(websocket)
        await websocket.wait_closed()
        logging.info(f"Websocket closed: {websocket.remote_address}")
        self.ws_listeners.remove(websocket)

    async def pub_msg(self, message):
        for websocket in self.ws_listeners:
            try:
                await asyncio.ensure_future(asyncio.wait_for(websocket.send(message),timeout=1))
            except asyncio.TimeoutError:
                logging.warn(f"Timeout exceeded for {websocket}")
                try:
                    await asyncio.ensure_future(asyncio.wait_for(websocket.close(),timeout=1))
                except Exception as e:
                    logging.error(f"Error while closing {websocket} , exception: {e}")

    async def handle_producer(self, reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info('peername')
        while True:
            data = await reader.readline()

            if not data or not data.decode():
                logging.info(f"Terminating connection with: {addr}")
                writer.close()
                await writer.wait_closed()
                break
            else:
                message = data.decode()
            logging.debug(f"Received {message!r} from {addr!r}")
            self.compute_rate()
            await self.pub_msg(message)

    def compute_rate(self):
        now = time.time()
        if not self.last_time:
            self.last_time = now
        self.counter += 1
        elapsed = now - self.last_time
        if elapsed >= 1:
            self.last_time = now
            rate = self.counter / elapsed
            logging.info(f"Rate: {rate}")
            self.counter = 0


async def run_server():
    broker = Broker()

    hostname = '0.0.0.0'
    ws_port = 8765
    tcp_port = 8080

    server = await asyncio.start_server(broker.handle_producer, hostname, tcp_port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.info(f'Serving on {addrs}')
    async with server:
        async with serve(broker.add_ws, hostname, ws_port, **{"timeout": 1}):
            await server.serve_forever()


if __name__ == '__main__':
    logging.info("Starting main asyncio.")
    asyncio.run(run_server())
