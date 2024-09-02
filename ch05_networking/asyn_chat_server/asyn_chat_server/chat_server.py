# minimal chat server example to illustrate how to write a simple 
# asynchronous TCP server-cliept application in Python

import asyncio


# simple echo server functionality that sends back any message sent to it
# test echo server with telnet 127.0.0.1 8888
# telnet allows to open up socket connections to remote hosts
async def handle_connection(reader, writer):
    writer.write("Hello new user, type something...\n".encode())

    data = await reader.readuntil(b"\n")

    writer.write("You sent: ".encode() + data)
    await writer.drain()

    # let's close the connection and clean up
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
