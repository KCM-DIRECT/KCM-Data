## Use Cases

* __User: Academic Researchers__
	* Data visualization of KCM datasets to see if there are any relationships between when a battery module is replaced and operational time, where module is spatially located, bus route, features in dataset (voltage, current, power, temperature). 
	* _Component Design:_ 
		* Understanding datasets - what are the features? How is it organized right now?
		* Data cleaning - Transform into a usable dataframe.  How many individual modules? Identify repeats. Time between data collection. Segment by bus and then by module. Identify when model is taken out
		* Data visualization (numpy, matplotlib, seaborn, pandas) to observe relationships that may exist between modules and operational time, where module is spatially located, bus route, features in dataset

