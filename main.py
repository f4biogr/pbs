import asyncio
import random
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from datetime import datetime
from os import getenv
from uuid import uuid4

timeout_list = [10, 20, 30, 40]
# groups = ["channel-test-prd-1", "channel-test-prd-2"]
groups = ["channel-test-prd-1"]


connection_string = getenv("CONNECTION_STRING")
hub_name = getenv("HUB_NAME")
client = WebPubSubServiceClient.from_connection_string(connection_string, hub_name)


async def send_message(iterations):
    print(client.get_client_access_token(groups=groups[0], minutes_to_expire=14400)["url"])
    # print(client.get_client_access_token(groups=groups[1], minutes_to_expire=14400)["url"])
    for _ in range(iterations):
        timeout = random.choice(timeout_list)
        uuid = str(uuid4())


        for group in groups:
            message = f"{group} - {uuid}"
            try:
                client.send_to_group(group=group, message=message, content_type="application/json")
                timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                print(f"[{timestamp}] - Message sent to {group}")
            except Exception:
                timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                print(f"[{timestamp}] - Error while sending message to {group}")

        await asyncio.sleep(timeout)


async def main():
    num_iterations = 30
    await send_message(num_iterations)

if __name__ == "__main__":
    asyncio.run(main())
