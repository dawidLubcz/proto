import socket
import struct
import time

import common
from google.protobuf import reflection
from proto import hello_world_pb2 as hello_pb2


def _receive_bits(_socket, wanted_len):
    # concatenate strings is slow, use list
    total_data = []
    while wanted_len > 0:
        _data = _socket.recv(wanted_len)
        if not _data:
            break
        wanted_len -= len(_data)
        total_data.append(_data)
    return b''.join(total_data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setblocking(True)
    s.settimeout(2)
    request = hello_pb2.HelloRequest()
    request.name = "Dawid"
    # request.id = 1
    s.connect((common.HOST, common.PORT))

    request_num = 10000
    start_time = time.perf_counter()
    for i in range(request_num):
        data = request.SerializeToString()
        msg = len(data).to_bytes(8, "little") + data
        s.sendall(msg)

        data = _receive_bits(s, 8)
        if len(data) == 8:
            incoming_rpc_size, = struct.unpack("<Q", data)
            data = _receive_bits(s, incoming_rpc_size)
        reply = reflection.ParseMessage(hello_pb2.HelloReply.DESCRIPTOR, data)

    end_time = time.perf_counter()
    print(f"Python3, {request_num} requests took {end_time - start_time} seconds, == {(end_time - start_time)/request_num} per request")
