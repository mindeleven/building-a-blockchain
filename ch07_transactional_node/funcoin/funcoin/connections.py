# class to store all the logic that manages our ConnectionPool

import structlog
from more_itertools import take

logger = structlog.getLogger(__name__)

class ConnectionPool:

    def __init__(self):
        # using a dict now, mapping address to writer
        self.connection_pool = dict() # represents peer connection

    def broadcast(self, writer, message):
        """
        Broadcasts a general message to the entire pool
        """
        for user in self.connection_pool:
            if user != writer:
                # we don't need to also broadcast to the user sending the message
                user.write(f"{message}\n".encode())

    @staticmethod
    def get_address_string(writer):
        # get a peer's ip:port (address)
        ip = writer.address["ip"]
        port = writer.address["port"]
        return f"{ip}:{port}" # address string in mapping is simply ip:port
        # helps us to uniquely identify connections

    def add_peer(self, writer):
        # add a peer to our connection pool
        address = self.get_address_string(writer)
        self.connection_pool[address] = writer
        logger.info("Added new peer to pool", address=address)

    def remove_peer(self, writer):
        # remove a peer to our connection pool
        address = self.get_address_string(writer)
        self.connection_pool.pop(address)
        logger.info("Removed peer from pool", address=address)

    def get_alive_peers(self, count):
        # add a peer to our connection pool
        # TODO (Reader): Sort these by most active, but let's just get
        # the first *count* of them for now
        return take(count, self.connection_pool.items()) # using take() to return count number of peers

