import socket
import common
import time
from proto import hello_world_pb2 as hello_pb2


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((common.HOST, common.PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Client connected by {addr}")
        msg = common.recv_message(conn, hello_pb2.HelloRequest)

        response = hello_pb2.HelloReply()
        response.message = f"Hello {msg.name}"
        common.send_message(conn, response)
        time.sleep(1)
