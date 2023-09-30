#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# defs.py defines the event and mentor objects
import defs

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
capacities = full_dictionary["How many shifts would you like?"]

# event_dictionary contains the list of the events and the responses to each
event_dictionary = dict(full_dictionary)
del event_dictionary["Timestamp"]
del event_dictionary["Username"]
del event_dictionary["Please enter your name:"]
del event_dictionary["How many shifts would you like?"]

simple_event_list = list(event_dictionary.keys())
# event_list should contain a list of all the event objects
event_list = [0 for i in range(len(simple_event_list))]
for index in range(len(event_dictionary)):
	event_name = simple_event_list[index].split("Event: ", 1)[1]
	event_name = event_name.split("Time: ", 1)[0]

	event_time = simple_event_list[index].split("Time: ", 1)[1]
	event_time = event_time.split("Location: ", 1)[0]

	event_location = simple_event_list[index].split("Location: ", 1)[1]
	event_location = event_location.split("Mentors needed: ", 1)[0]

	event_need = int(simple_event_list[index].split("Mentors needed: ", 1)[1])

	blank_assigned = [0 for i in range(event_need)]
	event_list[index] = make_event(event_name, event_time, event_location, event_need, blank_assigned)
	print(event_list[index])


# Step 3.5: Organize the mentors and their responses.

# Next, we need an array of those mentors so we can iterate through them
# This mentors should be in the same order in this array as in the form - first come, first assigned
mentor_list = [0 for i in range(len(names))]
for mentor_index in range(len(names)):

	mentor_response = [0 for i in range(len(event_list))]
	for event_index in range(len(event_list)):

		if (event_dictionary[event_list[event_index]][mentor_index] == "Yes"):
			mentor_response[event_index] = 1
	
	mentor_list[mentor_index] = make_mentor(names[mentor_index], emails[mentor_index], capacities[mentor_index], mentor_response)

# Now, we have an array of all of the mentors' names, emails, capacities, and responses - hooray!


# Step 4: Assign mentors to events
print(event_list)