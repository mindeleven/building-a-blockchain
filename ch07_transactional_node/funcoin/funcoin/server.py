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
        # bootstrapping our modules to the server:
        # server class will always have access to blockchain via self.blockchain
        self.blockchain = blockchain
        self.connection_pool = connection_pool
        self.p2p_protocol = p2p_protocol
        self.external_ip = None
        self.port = None

        if not(blockchain and connection_pool and p2p_protocol):
            logger.error("'blockchain', 'connection_pool' and 'gossip_protocol' must all be instantiated")
            raise Exception("Could not start")
        
    async def get_external_ip(self):
        # finds our "external IP" so we can advertise it to our peers
        self.external_ip = await get_external_ip # method responsible for finding our external IP

    async def handle_connection(self, reader: SteamReader, writer: SteamWriter):
        # this function is called when we receive a new connection
        # the writer object represents the connection peer 
        # we wait 'forever' until a message is sent to us terminated by a "\n" character
        # TODO: potential vulnerability, the server could get spammed by anyone

        while True:
            try:
                # wait forever on new data to arrive
                # handle and/or reply to the incoming data
                data = await reader.readuntil(b"\n")

                # we try to decode the message by assuming it was sent to us as UTF-8
                decoded_data = data.decode("utf-8").strip()

                try:
                    # using Marshmallow to parse and validate in incoming message
                    # from a peer
                    message = BaseSchema().loads(decoded_data)

                except MarshmallowError:
                    logger.info("Received unreadable message", peer=writer)
                    break

                # extract the adress from the message
                # and add it to the writer object
                writer.address = message["meta"]["address"]

                # let's add the peer to our connection pool
                self.connection_pool.add_peer(writer)

                # ... and handle the message
                # once the message has been parsed successfully
                # we assume that all relevant fields exist
                # and let the p2p_protocol decide what to do next
                await self.p2p_protocol.handle_message(message, writer)

                await writer.drain()

                if writer.is_closing():
                    break

            except asyncio.exceptions.IncompleteReadError:
                # an error happened, break out of the wait loop
                self.connection_pool.broadcast_user_quit(writer)
                break

        # we're now outside the message loop and the user has quit

        # let's close the connection and clean up
        writer.close()
        await writer.wait_closed()
        self.connection_pool.remove_peer(writer)

    async def listen(self, hostname="0.0.0.0", port=8888):
        # this is the listen method which spwans our server
        server = await asyncio.start_server(self.handle_connection, hostname, port)

        logger.info(f"Server listening on {hostname}:{port}")

        async with server:
            await server.serve_forever()

