import os
import shutil
import numpy as np
import module_changes as mc
import organize_functions as of
from os import listdir


def get_directory():
    directory = os.getcwd()
    print(directory)
    return directory


def count_bus_file():
    directory = get_directory()
    list = []
    for file in listdir(directory):
        substring = 'bus_'
        fullstring = 'sort_bus_by_date'
        if fullstring in file:
            pass
        else:
            if substring in file:
                list.append(file)
    return len(list)


def fliter_false_module():
    file_list = []
    get_bus = mc.compare_file_mods(get_directory()+'/')
    bus_file_num = count_bus_file()
    for i in range(1, bus_file_num):
        num = 'bus_'+str(i)
        bus = get_bus[num]
        for i in range(len(bus.columns)):
            if len(bus.columns) < 2:
                pass
            else:
                A = bus.columns[i]
                if bus[A] is False:
                    rslt_df = bus[A]
                else:
                    file_list.append(num)
    False_list = np.unique(file_list)
    return False_list


def move_false_bus():
    False_list = fliter_false_module()
    source = os.getcwd()
    destination = source + '/False_files'
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        pass
    for bus_file in False_list:
        shutil.move(bus_file, destination)
