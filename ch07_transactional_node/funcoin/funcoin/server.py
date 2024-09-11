# here's where our basic TCP Server lives
import asyncio
from asyncio import SteamReader, SteamWriter

import structlog
from marshmallow.exceptions import MarshmallowError

from funcoin.messages import BaseSchema
from funcoin.utils import get_external_ip

logger = structlog.getLogger()

class Server: 

    def __init__(self, blockchain, connection_pool, p2p_protocol):
        connection_pool = connection_pool
        pass

    async def get_external_ip(self):
        # finds our "external IP" so we can advertise it to our peers
        pass

    async def handle_connection(self, reader: SteamReader, writer: SteamWriter):
        # this function is called when we receive a new connection
        # the writer object represents the connection peer 

        # get a nickname from the client
        writer.write("> Choose your nickname:\n".encode())

        response = await reader.readuntil(b"\n")
        writer.nickname = response.decode().strip()

        # writer.write("You sent: ".encode() + response)
        self.connection_pool.add_new_user_to_pool(writer)
        self.connection_pool.send_welcome_message(writer)
        
        # announce the arrival of this new user
        self.connection_pool.broadcast_user_join(writer)

        while True:
            try:
                # handle and/or reply to the incoming data
                data = await reader.readuntil(b"\n")
            except asyncio.exceptions.IncompleteReadError:
                # an error happened, break out of the wait loop
                self.connection_pool.broadcast_user_quit(writer)
                break

            message = data.decode().strip()
            if message == "/quit":
                self.connection_pool.broadcast_user_quit(writer)
                break
            elif message == "/list":
                self.connection_pool.list_users(writer)
            else:
                self.connection_pool.broadcast_new_message(writer, message)

            await writer.drain()

            if writer.is_closing():
                break
        
        # we're now outside the message loop and the user has quit

        # let's close the connection and clean up
        writer.close()
        await writer.wait_closed()

    async def listen(self, hostname="0.0.0.0", port=8888):
        # this is the listen method which spwans our server
        server = await asyncio.start_server(self.handle_connection, hostname, port)

        logger.info(f"Server listening on {hostname}:{port}")

        async with server:
            await server.serve_forever()

