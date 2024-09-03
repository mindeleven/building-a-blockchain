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

class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()

    # writer passed to connection pool is an instance of StreamWriter
    # StreamWriter -> an asyncio object the writes to an underlying connection
    # (underlying connection = connected user)
    def send_welcome_message(self, writer):
        """
        Sends a welcome message to a newly connected client
        """
        message = dedent(f"""
        ===
        ( Welcome {writer.nickname}!

        There are {len(self.connection_pool) -1} user(s) here beside you
        ===     
        """)
        writer.write(f"{message}\n".encode())

    def broadcast(self, writer, message):
        """
        Broadcasts a general message to the entire pool
        """
        pass

    def broadcast_user_join(self, writer):
        """
        Calls the broadcast method with a "user joining" message
        """
        pass

    def broadcast_user_quit(self, writer):
        """
        Calls the broadcast method with a "user quitting" message
        """
        pass

    def broadcast_new_message(self, writer, message):
        """
        Calls the broadcast method with a user's chat message
        """
        pass

    def list_users(self, writer):
        """
        List all the users in the pool
        """
        pass

    def add_new_user_to_pool(self, writer):
        """
        Add a new user to our existing pool
        """
        self.connection_pool.add(writer)

    def remove_user_from_pool(self, writer):
        """
        Removes an existing user from our existing pool
        """
        self.connection_pool.remove(writer)



# simple echo server functionality that sends back any message sent to it
# test echo server with telnet 127.0.0.1 8888
# telnet allows to open up socket connections to remote hosts
async def handle_connection(reader, writer):
    # get a nickname from the client
    writer.write("> Choose your nickname:\n".encode())

    response = await reader.readuntil(b"\n")
    writer.nickname = response.decode().strip()

    # writer.write("You sent: ".encode() + response)
    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)
    await writer.drain()

    # let's close the connection and clean up
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 8888)

    async with server:
        await server.serve_forever()


connection_pool = ConnectionPool()
asyncio.run(main())
