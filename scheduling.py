#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# Step 1: Unzip the results
# TODO: Get the filename from the command line? Just search for a .zip file in the directory?
# Source: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
import zipfile
with zipfile.ZipFile("Mentor Scheduling Form.csv.zip","r") as zip_ref:
	zip_ref.extractall(".")

# Step 2: Read resulting csv file
# Source: https://realpython.com/python-csv/
import csv
from collections import defaultdict

full_dictionary = defaultdict(list)
with open("Mentor Scheduling Form.csv") as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		for (key, value) in row.items():
			full_dictionary[key].append(value)

# Step 3: Parse the csv file
emails = full_dictionary["Username"]
names = full_dictionary["Please enter your name:"]

# event_dictionary contains the list of the events and the responses to each
event_dictionary = dict(full_dictionary)
del event_dictionary["Timestamp"]
del event_dictionary["Username"]
del event_dictionary["Please enter your name:"]

# event_list contains just the list of events
event_list = list(event_dictionary.keys())
print(event_list)

