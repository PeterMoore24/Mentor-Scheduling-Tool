# I'm going to create an object for each Mentor to keep things organized
# Source: https://stackoverflow.com/questions/15081542/python-creating-objects
class Mentor(object):
	name = ""
	email = ""
	# Capacity will store the number of events each mentor said they wanted.
	capacity = 0
	# Responses will store how each mentor responded to each event
	# 1 for yes, 0 for no
	#responses = [0 for i in range(len(event_list))]
	responses = 0

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

# I'm going to create an event object to store all of the data related to an event
class Event(object):
	name = ""
	time = ""
	location = ""
	need = 0
	assigned = ""
	unaltered_name = ""
	
	def __init__(self, name, time, location, need, assigned, unaltered_name):
		self.name = name
		self.time = time
		self.location = location
		self.need = need
		self.assigned = ["" for i in range(need)]
		self.unaltered_name = unaltered_name

	def __repr__(self):
		return "Event: " + str(self.name) + " Time: " + str(self.time) + " Location: " + str(self.location) + " Need: " + str(self.need) + " Assigned: " + str(self.assigned)

def make_event(name, time, location, need, assigned, unaltered_name):
    event = Event(name, time, location, need, assigned, unaltered_name)
    return event