import csv
import os
import re
import pandas as pd
import sort_bus_by_date
from os import listdir


def compare_file_mods(directory):
    '''
    Returns a dictionary of bus numbers as keys and
    concatenated pandas dataframe comparing modules between each CSV file
    and its subsequent number. CSV files are ordered
    by date that data was retrieved.
    '''
    list_bus_nums = []
    bus_to_ordered_csvs = {}
    bus_to_modules = {}
    num_mods = 16
    mod_index = ['Module ' + str(i) for i in range(1, num_mods + 1)]
    keyword = 'Mfg Data (ASCII)'
    for file in listdir(directory):
        if file.startswith('bus'):
            list_bus_nums.append(file)
    for bus in list_bus_nums:
        df = sort_bus_by_date.sort_bus_by_date(directory, bus + '/')
        ordered_csv = df['Filename'].tolist()
        bus_to_ordered_csvs[bus] = ordered_csv
    for bus_key in bus_to_ordered_csvs:  # For each bus folder,
        column_names = []
        ordered_csvs = bus_to_ordered_csvs[bus_key]
        file_count = len(ordered_csvs)
        if file_count > 1:
            i = 0
            list_of_comp_df = []
            while(i < file_count - 1):
                og_modules = []
                comp_modules = []
                column_names.append(ordered_csvs[i] + ' vs '
                                    + ordered_csvs[i + 1])
                with open(directory + bus_key + '/'
                          + ordered_csvs[i]) as file:
                    reader = csv.reader(file)
                    for row in reader:
                        for element in row:
                            if keyword in element:
                                mod_num = re.sub(r'\W+',
                                                 '',
                                                 element[17:]).lower()
                                og_modules.append(mod_num)
                            else:
                                pass
                with open(directory
                          + bus_key
                          + '/'
                          + ordered_csvs[i + 1]) as file:
                    reader = csv.reader(file)
                    for row in reader:
                        for element in row:
                            if keyword in element:
                                mod_num = re.sub(r'\W+',
                                                 '',
                                                 element[17:]).lower()
                                comp_modules.append(mod_num)
                            else:
                                pass
                og_modules.pop(0)  # Getting rid of first overall module number
                comp_modules.pop(0)
                df_1 = pd.DataFrame(og_modules,
                                    columns=[column_names[i]],
                                    index=mod_index)
                df_2 = pd.DataFrame(comp_modules,
                                    columns=[column_names[i]],
                                    index=mod_index)
                comp = df_1.eq(df_2)
                list_of_comp_df.append(comp)
                i += 1
            concat_comp = pd.concat(list_of_comp_df, axis=1)
            bus_to_modules[bus_key] = concat_comp
        else:  # If there is only one CSV file
            mod_comp = []
            for i in range(0, 16):
                mod_comp.append(True)
            df_3 = pd.DataFrame(mod_comp, columns=[bus_key], index=mod_index)
            bus_to_modules[bus_key] = df_3
    return bus_to_modules
