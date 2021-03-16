import os, sys
import random
filename = "./data_store/data_store1.txt"

class File_Manager:
    def __init__(self):
        pass

    def save_data(self, senior):
        with open (filename, 'a') as mfile:
            data = f'{senior.id},{senior.device.type.name}\n'
            mfile.write(data)
        pass 

    def read_data(self, count):
        with open (filename) as mfile:
            mlist = list(mfile)
            if count > len(mlist):  # Not enough elements in list
                return []
            slist = random.sample(mlist, count)
            return slist

        return [] 


file_manager = File_Manager()