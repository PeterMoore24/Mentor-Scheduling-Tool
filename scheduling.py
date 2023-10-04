#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# defs.py defines the event and mentor objects
import defs

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

same_time = [False for i in range(len(event_list))]
# Step 4a: Check for events that are at the same time - we can't assign one mentor to two events at the same time!
for alpha_i in range(len(event_list)):
	for beta_i in range(len(event_list)):
		if (event_list[alpha_i].time == event_list[beta_i].time):
			same_time[alpha_i] = True

# First come first serve algorithm - iterate through the events, and assign the first mentor who is available to that event
# Continue this until the event's need is met
mentor_index = 0
assigned = False
for event_index in range(len(event_list)):
	num_assigned = 0
	event = event_list[event_index]
	print("Checking event " + str(event_index) + " with need " + str(event.need))

	# If this event and the one after it occur at the same time, continue from where we left off with the mentors
	if (not same_time[event_index] and (not assigned)):
		mentor_index = 0
	elif (mentor_index >= len(mentor_list)):
		mentor_index = 0
		assigned = False

	print("Checking mentor " + str(mentor_index))
	print("While eval 1: " + str(event.need > 0))
	print("While eval 2: " + str(mentor_index < len(mentor_list)))
	# Iterate through all of the mentors and assign them to the event until either the need is met or we've run out of mentors
	while (event.need > 0 and mentor_index < len(mentor_list)):
		mentor = mentor_list[mentor_index]

		print("Mentor responded " + str(mentor.responses[event_index]))
		if (mentor.responses[event_index] == 1 and mentor.capacity > 0):
			print("Assigning mentor " + str(mentor_index) + " to event " + str(event_index))
			event.assigned[num_assigned] = mentor.name
			num_assigned += 1
			event.need -= 1
			mentor.capacity -= 1
			assigned = True
		
		mentor_index += 1


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
	# print("Start Date: |" + start_date.replace("\n", "") + "|")
	# Start Time
	full_time = event.time.split(" ", 1)[1]
	start_time = full_time.split(" - ", 1)[0]
	end_time = full_time.split(" - ", 1)[1]
	calendar += "\"" + start_time.replace("\n", "") + "\","
	# print("Start Time: |" + start_time.replace("\n", "") + "|")
	# End Date
	# This assumes that every event starts and ends on the same day
	calendar += "\"" + start_date.replace("\n", "") + "\","
	# print("End Date: |" + start_date.replace("\n", "") + "|")
	# End Time
	calendar += "\"" + end_time.replace("\n", "") + "\","
	# print("End Time: |" + end_time.replace("\n", "") + "|")
	# All Day Event
	calendar += "False,\""
	calendar += event.location.replace("\n", "") + "\"\n"
	return calendar

for event in event_list:
	calendar_file.write(calendar_event(event))

mentor_file = open("assigned_mentors.csv", 'w')
mentor_file.write("Event number,Event name,Mentors assigned,Remaining need\n")

def mentor_event(event, index):
	mentor_string = str(index) + ","

	mentor_string += event.name.replace("\n", "") + ","

	for name in event.assigned:
		mentor_string += name.replace("\n", "") + ";"
	mentor_string += ","

	mentor_string += str(event.need) + "\n"
	return mentor_string

for index in range(len(event_list)):
	mentor_file.write(mentor_event(event_list[index], index))





# Here you can see the beginning of my attempt to create a .ics event.
# Realizing that DTSTART requires a specific format for time made me decide to just do the .csv for the ASU101 events.
# # Along with the example given in example.ics
# file1.write("BEGIN:VCALENDAR\n"
# 		  + "PRODID:-//Google Inc//Google Calendar 70.9054//EN\n")

# def convert_event(event):
# 	converted = "BEGIN:VEVENT\n"
# 	converted += "DTSTART: "