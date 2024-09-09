import asyncio

from funcoin.blockchain import Blockchain
from funcoin.connections import ConnectionPool
from funcoin.peers import P2PProtocol
from funcoin.server import Server

blockchain = Blockchain()
connectionPool = ConnectionPool()

server = Server(blockchain, connectionPool, P2PProtocol)


async def main():
    # start the server
    await Server.listen()

asyncio.run(main())