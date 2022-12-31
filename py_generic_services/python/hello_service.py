from proto.hello_world_pb2 import HelloService as _HelloServicePb2


class HelloService(_HelloServicePb2):
    def __init__(self):
        self._count = 0

    def SayHello(self, rpc_controller, request, done):
        self._count = self._count + 1
        done(self._count)
