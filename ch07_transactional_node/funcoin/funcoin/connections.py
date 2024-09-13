# class to store all the logic that manages our ConnectionPool

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
        Welcome {writer.nickname}!

        There are {len(self.connection_pool) -1} user(s) here beside you

        Help: 
         - Type anything to chat
         - /list will list all the connected users
         - /quit will disconnect you
        ===     
        """)
        writer.write(f"{message}\n".encode())

    def broadcast(self, writer, message):
        """
        Broadcasts a general message to the entire pool
        """
        for user in self.connection_pool:
            if user != writer:
                # we don't need to also broadcast to the user sending the message
                user.write(f"{message}\n".encode())

    def broadcast_user_join(self, writer):
        """
        Calls the broadcast method with a "user joining" message
        """
        self.broadcast(writer, f"{writer.nickname} just joined")

    def broadcast_user_quit(self, writer):
        """
        Calls the broadcast method with a "user quitting" message
        """
        self.broadcast(writer, f"{writer.nickname} just quit")

    def broadcast_new_message(self, writer, message):
        """
        Calls the broadcast method with a user's chat message
        """
        self.broadcast(writer, f"[{writer.nickname}] {message}")

    def list_users(self, writer):
        """
        List all the users in the pool
        """
        message = "===\n"
        message += "Currently connected users:"
        for user in self.connection_pool:
            if user == writer:
                message += f"\n - {user.nickname} (you)"
            else:
                message += f"\n - {user.nickname}"
        message += "\n==="
        writer.write(f"{message}\n".encode())

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
    
    @staticmethod
    def get_address_string(writer):
        # get a peer's ip:port (address)
        pass

    def add_peer(self, writer):
        # add a peer to our connection pool
        pass

    def remove_peer(self, writer):
        # remove a peer to our connection pool
        pass

    def get_alive_peers(self, count):
        # add a peer to our connection pool
        pass

