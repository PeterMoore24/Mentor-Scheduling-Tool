#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# Step 1: Unzip the results
# TODO: Get the filename from the command line? Just search for a .zip file in the directory?
# Source: https://stackoverflow.com/questions/3451111/unzipping-files-in-python

# TODO: THESE LINES MUST BE UNCOMMENTED BEFORE SHIPPING - FOR TESTING
# import zipfile
# with zipfile.ZipFile("Mentor Scheduling Form.csv.zip","r") as zip_ref:
# 	zip_ref.extractall(".")


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
capacities = full_dictionary["How many hours would you like?"]

# event_dictionary contains the list of the events and the responses to each
event_dictionary = dict(full_dictionary)
del event_dictionary["Timestamp"]
del event_dictionary["Username"]
del event_dictionary["Please enter your name:"]
del event_dictionary["How many hours would you like?"]

# event_list contains just the list of events
event_list = list(event_dictionary.keys())

#print(event_dictionary[event_list[1]][1])

# Step 3.5: Organize the mentors and their responses.
# I'm going to create an object for each Mentor to keep things organized
# Source: https://stackoverflow.com/questions/15081542/python-creating-objects
class Mentor(object):
	name = ""
	email = ""
	# Capacity will store the number of events each mentor said they wanted.
	capacity = 0
	# Responses will store how each mentor responded to each event
	# 1 for yes, 0 for no
	responses = [0 for i in range(len(event_list))]

	# We need to define a function to initialize each mentor object:
	def __init__(self, name, email, capacity, responses):
		self.name = name
		self.email = email
		self.capacity = capacity
		self.responses = responses
	
	# This function controls what is printed out when we call print on a mentor object (or str())
	# Source: https://stackoverflow.com/questions/1535327/how-to-print-instances-of-a-class-using-print
	def __repr__(self):
		resp_str = ""
		for i in range(len(event_list)): 
			resp_str += str(self.responses[i])
		return "Mentor: " + str(self.name) + " Email: " + str(self.email) + " Capacity: " + str(self.capacity) + " Responses: " + resp_str

def make_mentor(name, email, capacity, responses):
	mentor = Mentor(name, email, capacity, responses)
	return mentor

print(event_dictionary)
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
print(mentor_list)


# Step 4: Assign mentors to events