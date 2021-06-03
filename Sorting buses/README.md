Instructions for sorting raw bus folders:

Run ____.py. This package works in the following way:

1. Unzip "KCM-Raw-Data.zip"
2. Iterate through all csv's in the raw data and group them as a bus folder "bus_x" if they have a module serial number in common
3. Iterate through all bus folders and moves buses to "Cleaned buses" folder if it experienced a module swap
3. Rename bus numbers sequentially for visualization
