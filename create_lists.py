import defs

def create_event_list(simple_event_list):
    event_list = [0 for i in range(len(simple_event_list))]

    # Each event has the event, time, location, and number of mentors needed, we just need to extract that by cutting up the string with the names.
    # This part requires that the Google Form have the exact same form every time. 
    # Maybe a future version could be more flexible.
    for index in range(len(simple_event_list)):
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
    
    return event_list


def create_mentor_list(event_dictionary, event_list, names, emails, capacities):
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
    
    return mentor_list


def check_times(event_list):
    same_time = [False for i in range(len(event_list))]
    # Check for events that are at the same time - we can't assign one mentor to two events at the same time!
    # This should be made more complete in the future - currently assumes events are in order
    for index in range(len(event_list)-1):
        if (event_list[index].time == event_list[index+1].time):
            same_time[index] = True
    
    return same_time