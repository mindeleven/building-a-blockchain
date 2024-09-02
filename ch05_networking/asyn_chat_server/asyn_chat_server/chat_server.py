import asyncio

async def handle_connection(reader, writer):
    pass

async def main():
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 8888)
