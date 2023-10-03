#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# defs.py defines the event and mentor objects
import defs

# Step 1: Unzip the results
# TODO: Get the filename from the command line? Just search for a .zip file in the directory?
# Source: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
# TODO: Uncomment these lines
#import zipfile
#with zipfile.ZipFile("Mentor Scheduling Form.csv.zip","r") as zip_ref:
#	zip_ref.extractall(".")


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

# event_dictionary's keys are the name of the event, and its values are an array of each mentors' responses to the event
event_dictionary = dict(full_dictionary)
del event_dictionary["Timestamp"]
del event_dictionary["Username"]
del event_dictionary["Please enter your name:"]
del event_dictionary["How many shifts would you like?"]

simple_event_list = list(event_dictionary.keys())
# event_list should contain a list of all the event objects
event_list = [0 for i in range(len(simple_event_list))]

# Each event has the event, time, location, and number of mentors needed, we just need to extract that by cutting up the string with the names.
# This part requires that the Google Form have the exact same form every time. 
# Maybe a future version could be more flexible.
for index in range(len(event_dictionary)):
	unaltered_name = simple_event_list[index]
	
	event_name = simple_event_list[index].split("Event: ", 1)[1]
	event_name = event_name.split("Time: ", 1)[0]

	event_time = simple_event_list[index].split("Time: ", 1)[1]
	event_time = event_time.split("Location: ", 1)[0]

	event_location = simple_event_list[index].split("Location: ", 1)[1]
	event_location = event_location.split("Mentors needed: ", 1)[0]

	event_need = int(simple_event_list[index].split("Mentors needed: ", 1)[1])

	blank_assigned = [0 for i in range(event_need)]
	event_list[index] = defs.make_event(event_name, event_time, event_location, event_need, blank_assigned, unaltered_name)


# Step 3.5: Organize the mentors and their responses.
# Next, we need an array of those mentors so we can iterate through them
# This mentors should be in the same order in this array as in the form - first come, first assigned
mentor_list = [0 for i in range(len(names))]

# This section will loop through each mentor, and then loop through each response array, and create an array of that mentor's responses to every event.
for mentor_index in range(len(names)):

	mentor_response = [0 for i in range(len(event_list))]
	for event_index in range(len(event_list)):

		# These three lines could be (and originally were) one line but I split them up while debugging and found this format much more readable.
		current_event_name = event_list[event_index].unaltered_name
		current_event_responses = event_dictionary[current_event_name]
		if (current_event_responses[mentor_index] == "Yes"):
			mentor_response[event_index] = 1
			# response is set to 0 by default, so we don't need to check for "No"
	
	mentor_list[mentor_index] = defs.make_mentor(names[mentor_index], emails[mentor_index], int(capacities[mentor_index]), mentor_response)

# Now, we have an array of all of the mentors' names, emails, capacities, and responses - hooray!


# Step 4: Assign mentors to events
# First come first serve algorithm - iterate through the events, and assign the first mentor who is available to that event
# Continue this until the event's need is met
for event_index in range(len(event_list)):
	num_assigned = 0
	event = event_list[event_index]
	mentor_index = 0
	print("Working on assignments for event " + str(event_index))

	while (event_list[event_index].need > 0 and mentor_index < len(mentor_list)):
		print("Checking mentor " + str(mentor_index))
		mentor = mentor_list[mentor_index]

		if (mentor.responses[event_index] == 1 and mentor.capacity > 0):
			print("Assigning " + mentor.name)
			event.assigned[num_assigned] = mentor.name
			num_assigned += 1
			event.need -= 1
			mentor.capacity -= 1
		
		mentor_index += 1

print(event_list)