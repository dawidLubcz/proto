import socket
import common
import time
import sys
import asyncio
from proto import hello_world_pb2 as hello_pb2
from hello_service import HelloService
from hello_incomingrpc import HelloIncomingRpcHandler


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.get_event_loop()

    s.bind((common.HOST, common.PORT))
    s.listen()
    conn, addr = s.accept()

    print(f"Client connected by {addr}")
    time.sleep(1)
    incoming_rpc_handler = HelloIncomingRpcHandler(ready_socket=conn, async_loop=loop, service=HelloService())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
