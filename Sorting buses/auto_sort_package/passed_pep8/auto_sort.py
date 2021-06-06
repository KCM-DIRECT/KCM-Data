# ## IMPORTANT: Instructions For Use

# 1. MAKE SURE
#    master_function.py/
#    module_changes.py/
#    organize_functions.py/
#    sort_bus_by_date.py/
#    are all in the same directory as the files you want to sort
# 2. WARNING:
#    running this .py file will cause irreversible consequences
#    please make sure you have BACK UP for all the original files.

answer = input("WARNING:this script will cause irreversible consequences,"
               "please make sure you have BACK UP, continue?[y/n]")
if answer == "y":
    import master_function as mf
    directory = mf.of.find_directory()
    mf.of.group_files(directory)
    mf.fliter_false_module()
    mf.move_false_bus()
else:
    print("you type something other than 'y',so nothing happen")
