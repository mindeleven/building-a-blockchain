class Server: 

    def __init__(self) -> None:
        pass

# minimal chat server example to illustrate how to write a simple 
# asynchronous TCP server-cliept application in Python

# building the chat server:
# (1) when user connects prompt them for their nickname
# (2) broadcast arrival of new user to every connected user (except for new user)
# (3) broadcast user message to every connected user (except the sender of the msg)
# (4) predefined messages: 4/1 /list -> show list of all connected users to requesting user
# (5) predefined messages: 4/2 /quit 
#     -> disconnect requesting user
#     -> broadcast "<nick> has quit" to all connected users
# -> to accomplish tasks we create ConnectionPool class

import asyncio
from textwrap import dedent

async def handle_connection(reader, writer):
    # get a nickname from the client
    writer.write("> Choose your nickname:\n".encode())

    response = await reader.readuntil(b"\n")
    writer.nickname = response.decode().strip()

    # writer.write("You sent: ".encode() + response)
    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)
    
    # announce the arrival of this new user
    connection_pool.broadcast_user_join(writer)

    while True:
        try:
            data = await reader.readuntil(b"\n")
        except asyncio.exceptions.IncompleteReadError:
            connection_pool.broadcast_user_quit(writer)
            break

        message = data.decode().strip()
        if message == "/quit":
            connection_pool.broadcast_user_quit(writer)
            break
        elif message == "/list":
            connection_pool.list_users(writer)
        else:
            connection_pool.broadcast_new_message(writer, message)

        await writer.drain()

        if writer.is_closing():
            break
    
    # we're now outside the message loop and the user has quit

    # let's close the connection and clean up
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 8888)

    async with server:
        await server.serve_forever()


connection_pool = ConnectionPool()
asyncio.run(main())
