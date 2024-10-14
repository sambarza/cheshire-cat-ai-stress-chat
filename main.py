import json
import asyncio
import sys
from websockets.asyncio.client import connect
from datetime import datetime


async def cat_chat(user_id, prompt_to_send, sleep_between_chat):

    print("Starting chatting with user_id:", user_id)
    async with connect(f"ws://localhost:1865/ws/user_id={user_id}") as websocket:

        while True:

            request_at = datetime.now()

            await websocket.send(json.dumps({"text": prompt_to_send, "user_id": user_id}))

            async for message in websocket:
                cat_response = json.loads(message)

                if cat_response["type"] == "chat":
                    print(
                        f"{datetime.now()} {user_id} response, elapsed: {datetime.now() - request_at}"
                    )
                    break
            
            await asyncio.sleep(sleep_between_chat)


# Usa example:
# python main_async.py user 10 1 .st 6
# - run 10 parallels chat
# - sleep for 1 seconds between chat
# - send the ".st 6" prompt to sleep the thread for 6 secs
async def main():

    user_to_use = sys.argv[1]
    tasks_to_run = int(sys.argv[2])
    sleep_between_chat = int(sys.argv[3])
    prompt_to_send = " ".join(sys.argv[4:])

    print(f"Starting {tasks_to_run} tasks")

    tasks = []
    for i in range(tasks_to_run):
        user_id = f"{user_to_use}_{i}"
        tasks.append(cat_chat(user_id, prompt_to_send, sleep_between_chat))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
