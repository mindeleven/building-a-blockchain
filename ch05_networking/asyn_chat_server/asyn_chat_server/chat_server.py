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

class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()
    
    def send_welcome_message(self, writer):
        """
        Sends a welcome message to a newly connected client
        """
        pass

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
