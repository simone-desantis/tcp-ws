
import asyncio

from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol
import time


class Broker:
    def __init__(self):
        self.ws_listeners = set()
        self.counter = 0
        self.last_time = None

    async def add_ws(self, websocket: WebSocketServerProtocol):
        self.ws_listeners.add(websocket)
        await websocket.wait_closed()
        print(f"Websocket closed: {websocket.remote_address}")
        self.ws_listeners.remove(websocket)

    async def pub_msg(self, message):
        for websocket in self.ws_listeners:
            await websocket.send(message)

    async def handle_producer(self, reader, writer):
        while True:
            data = await reader.readline()
            message = data.decode()
            addr = writer.get_extra_info('peername')

            if not message:
                print(f"Terminating connection with: {addr}")
                writer.close()
                await writer.wait_closed()
                break
            print(f"Received {message!r} from {addr!r}")
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
            print(f"Rate: {rate}")
            self.counter = 0


async def run_server():
    broker = Broker()

    hostname = '0.0.0.0'
    ws_port = 8765
    tcp_port = 8080

    server = await asyncio.start_server(broker.handle_producer, hostname, tcp_port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        async with serve(broker.add_ws, hostname, ws_port):
            await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(run_server())
