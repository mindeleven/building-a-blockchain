import asyncio
import time

async def greet(name, delay):
    await asyncio.sleep(delay)
    print(f'{name}: I waited {delay} seconds before saying "hello"')

async def main():
    # three functions with arguments get transformed into tasks
    # which can be executed concurrently
    # these tasks are called awaitables -> they'll be waited upon once called with await
    task_1 = asyncio.create_task(greet("t1 (3rd?)", 15))
    task_2 = asyncio.create_task(greet("t2 (1st?)", 5))
    task_3 = asyncio.create_task(greet("t3 (2nd?)", 10))

    start_time = time.time()

    print("0.00s: Program Start")
    
    # triggering the tasks with await
    await task_1
    await task_2
    await task_3

    print(f"{time.time() - start_time:.2f}s: Program End")

# calling main inside asyncio's run function
# tells Python that what's inside main() should be run concurrently
asyncio.run(main())