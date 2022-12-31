import asyncio
import struct
import queue
import threading

from google.protobuf import reflection
from google.protobuf.service import Service
from proto.hello_world_pb2 import HelloReply as HelloReply


class DataReceiverListener:
    def on_rpc(self, rpc):
        raise NotImplementedError()


class DataReceiver:
    def __init__(self, _socket, async_loop, listener: DataReceiverListener):
        self._socket = _socket
        self._message_size_bits = 8
        self._queue = None
        self._async_loop = async_loop
        self._listener = listener
        self._kill = True
        self._send_thread: threading.Thread = None
        self._read_thread: threading.Thread = None

    def run(self):
        self._kill = False
        self._queue = queue.Queue()
        self._read_thread = threading.Thread(target=self._read)
        self._read_thread.daemon = True
        self._read_thread.start()
        self._send_thread = threading.Thread(target=self._send)
        self._send_thread.daemon = True
        self._send_thread.start()

    def stop(self):
        self._kill = True
        self._send_thread.join()
        self._read_thread.join()

    @staticmethod
    def _receive_bits(_socket, wanted_len):
        # concatenate strings is slow, use list
        total_data = []
        while wanted_len > 0:
            data = _socket.recv(wanted_len)
            if not data:
                break
            wanted_len -= len(data)
            total_data.append(data)
        return b''.join(total_data)

    def _read(self):
        print("_read thread started")
        while True:
            if self._kill:
                break
            data = DataReceiver._receive_bits(self._socket, self._message_size_bits)
            if len(data) == self._message_size_bits:
                incoming_rpc_size, = struct.unpack("<Q", data)
                data = DataReceiver._receive_bits(self._socket, incoming_rpc_size)

                async def coro():
                    self._listener.on_rpc(data)
                asyncio.run_coroutine_threadsafe(coro(), self._async_loop)

    def _send(self):
        print("_send thread started")
        while True:
            if self._kill:
                break
            try:
                msg = self._queue.get(block=True, timeout=1)
                self._queue.task_done()
                self._socket.sendall(msg)
            except queue.Empty as e:
                continue

    def send_rpc_data(self, data):
        msg = len(data).to_bytes(self._message_size_bits, "little") + data
        self._queue.put(msg)


class HelloIncomingRpcHandler(DataReceiverListener):
    def __init__(self, ready_socket, async_loop, service):
        self._pending_requests = {}
        self._current_id = 0
        self._service = service
        self._data_receiver = DataReceiver(_socket=ready_socket, async_loop=async_loop, listener=self)
        self._data_receiver.run()

    def on_rpc(self, data):
        self._handle_rpc(data)

    def _get_service(self) -> Service:
        return self._service

    def _handle_rpc(self, data):
        service = self._get_service()
        method_descriptor = service.GetDescriptor().methods[0]
        request = reflection.ParseMessage(method_descriptor.input_type, data)

        def _prepare_response(count):
            response = HelloReply()
            response.message = f"Reply nr: {count}"
            return response

        def _rpc_response_callback(count):
            _rpc = _prepare_response(count)
            self._send_data(_rpc)
        service.CallMethod(method_descriptor, self, request, _rpc_response_callback)

    def _send_data(self, rpc):
        data = rpc.SerializeToString()
        self._data_receiver.send_rpc_data(data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._data_receiver.stop()
