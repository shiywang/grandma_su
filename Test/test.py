import json
import queue
import atexit
import time
from logger import Logger
from apihandler import api_handler
from senior import senior_manager
import sys
import random
import math
import asyncio
import websockets
import argparse
import os


websocket_url = "ws://127.0.0.1:8000/"
senior_queue = queue.Queue()

PING_TIMEOUT = 60
UPDATE_DATA_TIMEOUT = 1


# On program exit delete users from database
def exit_handler():
    print("Deleting Seniors")
    for senior in senior_queue.queue:
        # pass
        senior_manager.delete_senior(senior)
    print("End")


class TestECG(Logger):
    def __init__(self, num_senior):
        Logger.__init__(self, "Main")
        self.num_senior = num_senior
        self.update_percentage = math.ceil(num_senior * 0.15)
        self.debug("Test ECG")
        self.last_ping_time = 0
        self.last_data_update_time = int(time.time())

        seniors = senior_manager.get_senior(num_senior)

        if len(seniors) == 0:
            print("create new seniors")
            seniors = [senior_manager.make_senior() for _ in range(num_senior)]

        for senior in seniors:
            senior_queue.put(senior)

    async def run(self):
        url = websocket_url + 'ws/sensordata/RR'
        async with websockets.connect(url) as websocket:
            while True:
                if int(time.time()) - self.last_data_update_time > UPDATE_DATA_TIMEOUT:
                    update_list = random.sample(senior_queue.queue, self.update_percentage)
                    for senior in update_list:
                        data = senior.get_data()
                        await websocket.send(json.dumps(data))
                    self.last_data_update_time = int(time.time())
                # device_type = senior.device.type.name
                # data = senior.get_data()
                # url = base_url + "sensordata/" + device_type + '/'
                # r = requests.post(url, headers=request_headers, auth=(api_user, api_password), data=json.dumps(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='args.')
    parser.add_argument('-n', '--num', type=int, default=1)
    parser.add_argument('-d', '--dele', default=True)

    args = parser.parse_args()
    input_num = args.num
    if args.dele is True:
        try:
            os.remove("./data_store/test.txt")
        except OSError:
            pass

        with open("./data_store/test.txt", 'a') as results_file:
            pass
        

    # input_num = int(sys.argv[1])
    atexit.register(exit_handler)
    test_run = TestECG(input_num)
    api_handler.start()
    asyncio.run(test_run.run())
