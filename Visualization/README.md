Instructions for extracting and plotting graphs from sorted buses with module changes:

1. Run heat map .py to *create dataframe that counts number of times each module on each bus was changed*
2. Plot heat map using .py
	a. ***Here, more csv's were manually moved if heat map appeared abnormal (example: modules were changed each time, one csv did not match)
3. Extract voltage/temp data for a particular module by providing a specific module serial number along with a property of the module (cell voltages, temperature, etc.) using the swapped_mod_dataframes function in find_useful_mods.py. This outputs a list of dataframes with each dataframe representing the desired data for each CSV file ordered chronologically.
4. Need to add Sarah's function in here too for finding data for a module (specify with 1 through 16).
