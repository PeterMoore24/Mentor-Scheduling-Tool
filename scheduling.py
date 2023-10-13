#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# defs.py defines the event and mentor objects
import defs
# create_lists.py defines functions to create the event_list, mentor_list, and same_time lists
import create_lists
# sort_mentors.py defines several functions to sort mentors
import sort_mentors

# Step 1: Unzip the results
# TODO: Get the filename from the command line? Just search for a .zip file in the directory?
# Source: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
# TODO: Uncomment these lines
import zipfile
with zipfile.ZipFile("ASU 101 Scheduling Form.csv.zip","r") as zip_ref:
	zip_ref.extractall(".")


# Step 2: Read resulting csv file
# Source: https://realpython.com/python-csv/
import csv
from collections import defaultdict

full_dictionary = defaultdict(list)
with open("ASU 101 Scheduling Form.csv") as csv_file:
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
event_list = create_lists.create_event_list(simple_event_list)


# Step 3.5: Organize the mentors and their responses.
# Next, we need an array of those mentors so we can iterate through them
mentor_list = create_lists.create_mentor_list(event_dictionary, event_list, names, emails, capacities)
mentor_list = sort_mentors.capacity_sort(mentor_list)


# Step 4: Assign mentors to events
same_time = create_lists.check_times(event_list)

# First come first serve algorithm - iterate through the events, and assign the first mentor who is available to that event
# Continue this until the event's need is met
mentor_index = 0
for event_index in range(len(event_list)):
	num_assigned = 0
	event = event_list[event_index]

	# If this event and the one after it occur at the same time, continue from where we left off with the mentors
	# This should be made more complete in the future - currently assumes events are in order
	# Assumes if a mentor is unavailable for an event at a certain time they will not be available for another event at the same time
	if (not same_time[event_index-1]):
		mentor_index = 0

	# Iterate through all of the mentors and assign them to the event until either the need is met or we've run out of mentors
	while (event.need > 0 and mentor_index < len(mentor_list)):
		mentor = mentor_list[mentor_index]

		if (mentor.responses[event_index] == 1 and mentor.capacity > 0):
			event.assigned[num_assigned] = mentor.name
			num_assigned += 1
			event.need -= 1
			mentor.capacity -= 1
		elif (mentor.responses[event_index] == 1):
			event.unassigned += mentor.name + "   "
		
		mentor_index += 1
	
	# Iterate through all the remaining mentors to list them as unassigned
	unassigned_mentor_index = mentor_index
	while (unassigned_mentor_index < len(mentor_list)):
		mentor = mentor_list[unassigned_mentor_index]

		if (mentor.responses[event_index] == 1):
			event.unassigned += mentor.name + "   "
		unassigned_mentor_index += 1


# Step 5: Create Google Calendar-readable output
# Google Calendar has a few fields that we can use to create an event.
# Google Calendar has two options for importing events: csv or iCalendar
# csv would definitely be easier to implement but does not support attendees
# # I will be creating this file following Google's guidance at https://support.google.com/calendar/answer/37118

# CSV required fields:
	# Subject = event.name
	# Start date = substring of event.time
# Optional fields we will use:
	# Start time = substring of event.time
	# End date = substring of event.time
	# End time = substring of event.time
	# Location = event.location
# Optional fields we won't use:
	# All day event = false
	# Description
	# Private = false

calendar_file = open("event_calendar.csv", 'w')
calendar_file.write("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Location\n")

def calendar_event(event):
	# Subject
	calendar = "\"" + event.name.replace("\n", "") + "\","
	# Start Date
	start_date = event.time.split(" ", 1)[0]
	calendar += "\"" + start_date.replace("\n", "") + "\","

	# Start Time
	full_time = event.time.split(" ", 1)[1]
	start_time = full_time.split(" - ", 1)[0]
	end_time = full_time.split(" - ", 1)[1]
	calendar += "\"" + start_time.replace("\n", "") + "\","

	# End Date
	# This assumes that every event starts and ends on the same day
	calendar += "\"" + start_date.replace("\n", "") + "\","

	# End Time
	calendar += "\"" + end_time.replace("\n", "") + "\","

	# All Day Event
	calendar += "False,\""
	calendar += event.location.replace("\n", "") + "\"\n"
	return calendar

for event in event_list:
	calendar_file.write(calendar_event(event))

mentor_file = open("assigned_mentors.csv", 'w')
# This should print out more information to be more clear in the future.
mentor_file.write("Event name,Event time,Event location,Mentors assigned,Remaining need,Unassigned available mentors\n")

def mentor_event(event):
	# Name, time, location
	mentor_string = event.name.replace("\n", "") + ","
	mentor_string += event.time.replace("\n", "") + ","
	mentor_string += event.location.replace("\n", "") + ","

	# Assigned mentors
	for name in event.assigned:
 		mentor_string += name.replace("\n", "") + "    "
	mentor_string += ","

	# Remaining need
	mentor_string += str(event.need) + ","

	# Unassigned available mentors
	# Events with remaining need >= 1 and unassigned available mentors means those mentors'
	# capacities have been met
	mentor_string += str(event.unassigned) + "\n"
	return mentor_string

for event in event_list:
	mentor_file.write(mentor_event(event))
