import socket
import common
from proto import hello_world_pb2 as hello_pb2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((common.HOST, common.PORT))

    print("What is your name?")
    name = input()
    request = hello_pb2.HelloRequest()
    request.name = name
    common.send_message(s, request)

    reply = common.recv_message(s, hello_pb2.HelloReply)
    print(f"Client received msg: {reply.message}")
