'''
The peers module represents the logic surrounding the sending and receiving of messages;
'''

# error class that we can use to catch for problems
class P2PError(Exception):
    pass

class P2PProtocol: 

    def __init__(self, server):
        pass

    @staticmethod
    async def send_message(writer, message):
        # sends a message to a particular peer
        pass

    async def handle_message(self, message, writer):
        # handles an incoming message passed by the server
        # most important message in this module
        # hands this message off to a more specific method:
        handle_message_specific(message)

    async def handle_message_specific(self, message):
        # temporary method for scaffolding
        pass

    async def handle_message_ping(self, message, writer):
        # handles incoming "ping" message
        pass

    async def handle_block(self, message, writer):
        # handles incoming "block" message
        pass

    async def handle_transaction(self, message, writer):
        # handles incoming "transaction" message
        pass

    async def handle_peers(self, message, writer):
        # handles incoming "peers" message
        pass

'''
basis form of a message that's received by handle_message()

{
    "meta": {
        "address": {
            "ip": <external ip: str>,
            "port": <external port: int>,
        },
        "client": "funcoin 0.1"
    },
    "message": {
        "name": <message name: str>,
        "payload": <message payload: obj>
    }
}

'''
