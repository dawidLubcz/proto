# Proto sandbox

### basic_file_write_read
First example from the protobuf python doc.

1. Encode and save to file.
2. Read from file and decode.

### bin
Protocol compiler.

### hello_world_socket
Client sends an encoded message to the server over tcp.
Server decodes the message and sends an encoded response.

### py_generic_services
Client / server basic app with simple proto service.
Used to measure python proto performance.

1. Client sends encoded messages to the server.
2. Server listens to incoming data on the socket end and expects to 8-bit message size first and the message itself next (DataReceiver).
3. Raw data is parsed to the protocol request and passed to the service using the protocol method descriptor (method index is hardcoded).
The response is built (HelloIncomingRpcHandler).
4. Service handles the message and call response callback (HelloService).
5. Response is sent to the client.