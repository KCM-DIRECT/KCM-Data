import altair as alt
import csv
import datetime
from datetime import datetime
import matplotlib.pyplot as plti
import numpy as np
import pandas as pd
import pathlib
import re
import os
from os import listdir
from IPython.display import HTML  # For pretty printing!

def find_directory():
    '''
    Assuming your python file is in the directory containing KCM data files, returns a path to that directory with an additional
    forward slash for future concatenation processes.
    '''
    path = pathlib.Path().absolute()
    directory = str(path) + '/'
    return directory
    

def sort_bus_by_date(directory, bus_num):
    ''' input bus_num as string with number of bus desired'''
    
    # find directory of bus from sorted files
    bus_directory = directory + bus_num
    
    #make list of all files in bus folder
    csv_list = []
    for file in listdir(bus_directory):
        if file.endswith('.csv'):
            csv_list.append(file)
    
    # make a list of dates and initialize final columns for dataframe
    list_of_dates = []
    substring = 'Data retrieved'
    cols = ['Filename', 'DateRetrieved']

    for filename in csv_list:
        with open(bus_directory + filename) as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    for element in row:
                        if substring in element:
                            #print(filename, '|', element)
                            list_of_dates.append(element)
                except:
                    pass #some files have no data
    # pull out the 'Date Retrieved' and @ symbol from the date column
    for i in range(len(list_of_dates)):
        date = list_of_dates[i]
        list_of_dates[i] = date[16:].replace('@', '')
    
    # make the dataframe of filenames and dates
    list_of_tuples = list(zip(csv_list, list_of_dates))
    files_dates = pd.DataFrame(list_of_tuples, columns = cols)
    
    #sort by date
    files_dates['DateRetrieved'] = pd.to_datetime(files_dates.DateRetrieved)
    files_dates.sort_values('DateRetrieved', inplace=True)
    files_dates.reset_index(drop = True, inplace=True)
    
    return files_dates
    
def build_bus_df(directory, bus_num, keyword):
    bus_dates = sort_bus_by_date(directory, bus_num)
    if keyword == 'Current':
        row_list = list(range(19)) + list(range(20,960))
        index_range = list(range(0,18)) + list(range(19,960))
    elif keyword == 'Voltage':
        row_list = list(range(23)) + list(range(24,960))
        index_range = list(range(0,22)) + list(range(23,960))
    elif keyword == 'Power':
        row_list = list(range(27)) + list(range(28,960))
        index_range = list(range(0,26)) + list(range(27,960))
    else:
        print("Keyword entered in error. Please select from 'Current', 'Voltage', or 'Power'.")
        
    bus_parameter = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list) 
        bus_parameter = bus_parameter.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    bus_parameter.columns = df_index.columns

    bus_parameter = bus_parameter.loc[:, ~bus_parameter.columns.str.contains('^Unnamed')]
    bus_parameter.reset_index(drop = True, inplace=True)

    return bus_parameter


def build_module_df(directory, bus_num, module_num):
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47)* (module_num-1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51,960))
    
    module_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list) 
        module_df = module_df.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    module_df.columns = df_index.columns

    module_df = module_df.loc[:, ~module_df.columns.str.contains('^Unnamed')]
    module_df.reset_index(drop = True, inplace=True)

    return module_df
    
    
def build_module_average_df(directory, bus_num, module_num):
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47)* (module_num-1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51,960))
    
    module_average_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        tmp = tmp.dropna(axis=1)
        tmp = tmp.drop(0, axis=1)
        tmp_ave = tmp.mean()
        module_average_df = module_average_df.append(tmp_ave, ignore_index = True)
    
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    df_index = df_index.loc[:, ~df_index.columns.str.contains('^Unnamed')]
    module_average_df.columns = df_index.columns

    
    module_average_df.reset_index(drop = True, inplace=True)
    module_average_df_final = pd.concat([module_average_df, bus_dates['DateRetrieved'].astype(str)], axis=1)
    module_average_df_final = module_average_df_final.set_index('DateRetrieved')

    return module_average_df_final
    
    
def count_mod_changes(directory):
    '''
    
    '''
    keyword = 'Mfg Data (ASCII)'
    list_bus_nums = []  # To get the name of bus number folders
    bus_to_ordered_csvs = {}  # Dictionary associating each bus folder with an chronologically ordered list of CSVs
    bus_to_ordered_dates = {}  # Dictionary associating each bus folder with dates listed chronologically
    file_serials = {}  # Dictionary with serial numbers for each CSV
    list_df = []  # List of dataframes for each bus
    column_names = ['Bus', 'Module', 'Date', 'Change']
    num_mods = 16  # Constant number of mods
    module_index = 8  # For grabbing module string indices later
    bus_single = 5
    bus_double = 6
    last_two_chars = -2  # For grabbing last two characters
    last_one_chars = -1  # For grabbing last character
    mod_index = ['Module ' + str(i) for i in range(1, num_mods + 1)]  # Creating rows for dataframe
    mod_change_count = {}  # Dictionary for number of changes, sum value for each module # as compared file to file

    
    keyword = 'Mfg Data (ASCII)'  # Keyword to search for
    for file in listdir(directory):  # Place this file in directory with False_files -> Keiton's code
        if file.startswith('bus'):
            list_bus_nums.append(file)  # Getting list of bus names
    for bus in list_bus_nums:  # For each bus
        ordered_dates = []
        df = sort_bus_by_date(directory, bus + '/')
        ordered_csv = df['Filename'].tolist()
        ordered_unclean_dates = df['DateRetrieved'].tolist()
        for unclean_date in ordered_unclean_dates:
            split_results = unclean_date.strftime('%m/%d/%Y, %H:%M:%S')
            ordered_dates.append(split_results)
        bus_to_ordered_csvs[bus] = ordered_csv  # Grabbing a sorted list of CSV's for each bus folder
        bus_to_ordered_dates[bus] = ordered_dates  # Grabbing a sorted list of dates for each folder
    for bus_key in bus_to_ordered_csvs:  # For each bus folder (key value for bus to ordered files dictionary)
        
        for mod_name in mod_index:  # Setting dictionary with all module count at 0 to start. Should be for each bus. 
            mod_change_count[mod_name] = [0]  # Add the dataframe at the end of the comparisons to the list_df
        
        ordered_dates = bus_to_ordered_dates[bus_key]  # Grab list of dates for dataframe use later
        ordered_csvs = bus_to_ordered_csvs[bus_key]  # Grab the list of ordered CSV's associated with current bus folder
        for i in range(len(ordered_csvs)):  # For each file in the list of ordered CSV's
            serial_nums = []  # Start with empty list of serial numbers for that file
            with open(directory +  bus_key + '/' + ordered_csvs[i]) as file:  # Looking through current file
                reader = csv.reader(file)
                for row in reader:
                    for element in row:
                        if keyword in element:
                            mod_num = re.sub(r'\W+', '', element[17:]).lower()
                            serial_nums.append(mod_num)  # Grabbing serial numbers for each CSV file
                        else:
                            pass
            # After you get all the serial numbers for a file
            serial_nums.pop(0)  # Getting rid of first module number
            file_serials[ordered_csvs[i]] = serial_nums  # Key: file name. Value: List of serial numbers for that file name
        
        # At this point, we have a list of serial numbers associated with each CSV file
        i = 0
        while(i < len(ordered_csvs) - 1):  # While we are not looking at the last file (can't compare last file with anything)
            first_mods = file_serials[ordered_csvs[i]]  # Gets you first list of serials
            next_mods = file_serials[ordered_csvs[i + 1]] # Get second list of serials
            for j in range(len(first_mods)):  # For each index (mod #) in the list of modules
                mod_string = "Module " + str(j + 1)  # For first iteration, "Module 1"
                if first_mods[j] != next_mods[j]:
                    mod_change_count[mod_string].append(mod_change_count[mod_string][-1] + 1)  # If different, append prev. count + 1
                else:
                    mod_change_count[mod_string].append(mod_change_count[mod_string][-1])  # If same, just append prev. count
            i += 1
        
        # Now we have dictionary with count of changes per file compared for each module (16 mods) 
        num_comps = len(ordered_csvs) - 1
        bus_num_element = ''
        if len(bus_key) == bus_single:
            bus_num_element = bus_key[-1]
        elif len(bus_key) == bus_double:
            bus_num_element = bus_key[-2:]
        else:
            bus_num_element = bus_key[-3:]
#         print(bus_num_element)
        bus_number_list = [bus_num_element for i in range((num_comps + 1) * num_mods)] # To get the bus # values
        module_labels = []
        change_labels = []
        mod_num_label = ''
        for mod_label in mod_change_count.keys():  # For each module number 1 through 16
            change_labels += mod_change_count[mod_label]
            if len(mod_label) > module_index:
                mod_num_label = mod_label[last_two_chars:]
            else:
                mod_num_label = mod_label[last_one_chars]
            for i in range(num_comps + 1):
                module_labels.append(mod_num_label)
        date_labels = ordered_dates * num_mods
#         print("Bus numbers: ", len(bus_number_list), "\n Module numbers: ", module_labels, "\n Change labels: ", len(change_labels), "\n Date labels: ", len(date_labels))
        data_lists = [bus_number_list, module_labels, date_labels, change_labels]
        df_dict = {}
        for column, data_list in zip(column_names, data_lists):
            df_dict[column] = data_list
        df_bus_changes = pd.DataFrame(data=df_dict)
        list_df.append(df_bus_changes)
    return pd.concat(list_df, axis=0)


def visualise_mod_changes(directory):
    df1 = count_mod_changes(directory)
    data = df1.melt(id_vars=['Bus', 'Module', 'Date'])
    buses = list(data['Bus'].unique())
    alt.data_transformers.disable_max_rows() 
    select_bus = alt.selection_single(
    name='Select', fields=['Bus'], init={'Bus': 1},
    bind=alt.binding_select(options=buses)
    )

    chart = alt.Chart(data).mark_rect(stroke='black').encode(
        x=alt.X('Date', title="Date", sort=None),
        y=alt.Y('Module', title="Module", sort=None),
        color=alt.Color('value', legend=None)
    ).add_selection(select_bus).transform_filter(select_bus)

    return chart
    