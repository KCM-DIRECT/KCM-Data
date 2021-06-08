import filter_false_modules
import numpy as np
from os import listdir

directory = 'test_data/test_data_after_sorted'

def test_count_bus_file_1():
    '''
    Test to determine that returned bus folders of test data is 2.
    '''
    bus_count = filter_false_modules.count_bus_file(directory)
    assert bus_count == 2, "Number of buses in folder should be 2"
    return

directory = 'test_data/test_data_after_sorted'+'/false_file/'


def test_filter_false_module_1():
    '''
    Test the function should return an array type
    '''
    return_type = filter_false_modules.filter_false_module()
    assert isinstance(return_type,np.ndarray),'The return type is not an array'
    return


def test_filter_false_module_2():
    '''
    Test the function should return a list type and each element should be string
    '''
    return_list = filter_false_modules.filter_false_module()
    for element in return_list:
        assert isinstance(element,str),'Each element in this list should be string.'
    return


def test_move_false_bus_1():
    '''
    Test each folder that get relocated should have at least two csv files.
    '''
    cwd = filter_false_modules.get_directory()
    destination = cwd + '/test_data_after_sorted' + '/false_file/'
    for file in listdir(destination):
        each_bus = listdir(destination + file)
        assert len(each_bus) >= 2, 'Each bus file should contain at least two csv files.'
    return


def test_move_false_bus_2():
    '''
    Test each folder that get relocated should have be all csv type files.
    '''
    cwd = filter_false_modules.get_directory()
    destination = cwd +'/test_data_after_sorted' + '/false_file/'
    for file in listdir(destination):
        each_bus = listdir(destination + file)
        for element in each_bus:
            assert element.endswith('.csv'), 'There is a non csv file.'
    return
