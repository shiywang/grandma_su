import argparse
import multiprocessing
import os

from senior import senior_manager
import queue, time
import requests, atexit, time
from logger import Logger
from api_handler import api_handler
import sys, random, math

# Queue to hold seniors created
senior_queue = queue.Queue()

PING_TIMEOUT = 60
UPDATE_DATA_TIMEOUT = 5


# On program exit delete users from database
def exit_handler():
    print("Deleting Seniors")
    for senior in senior_queue.queue:
        senior_manager.delete_senior(senior)
    print("End")


class Test1(Logger):
    def __init__(self, nseniors):
        Logger.__init__(self, "Main")
        self.nseniors = nseniors
        self.update_percentage = math.ceil(nseniors * 0.15)
        self.debug("Test 1")
        self.last_ping_time = 0
        self.last_data_update_time = int(time.time())

        tlist = senior_manager.get_senior(nseniors)
        for senior in tlist:
            senior_queue.put(senior)

    def run(self):
        while True:
            # Ping after specified timeout
            if int(time.time()) - self.last_ping_time > PING_TIMEOUT:
                self.debug("Pinging ...")
                for senior in senior_queue.queue:
                    api_handler.onThread(api_handler.send_ping, senior)

                self.last_ping_time = int(time.time())

            # Randomly update data
            if int(time.time()) - self.last_data_update_time > UPDATE_DATA_TIMEOUT:
                self.debug("Updating data")

                # Randomly seniors to update
                update_list = random.sample(senior_queue.queue, self.update_percentage)
                for senior in update_list:
                    api_handler.onThread(api_handler.send_data, senior)

                self.last_data_update_time = int(time.time())


###
# Main Entry Point 
###
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='args.')
    parser.add_argument('-n', '--num', type=int, default=1)
    parser.add_argument('-d', '--dele', default=True)

    print("Number of cpu :", multiprocessing.cpu_count())
    args = parser.parse_args()
    input_num = args.num
    if args.dele is True:
        try:
            os.remove("./data_store/test.txt")
        except OSError:
            pass

        with open("./data_store/test.txt", 'a') as results_file:
            pass

    if len(sys.argv) < 2:
        print("Incomplete arguments")
        exit()

    atexit.register(exit_handler)
    test1 = Test1(input_num)
    api_handler.start()  # Start Thread
    test1.run()
