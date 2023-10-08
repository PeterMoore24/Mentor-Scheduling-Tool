# Unsorted current remaining need: 26

# Sorts the list of mentors by their capacity for shifts
# Current remaining need: 23
def capacity_sort(mentor_list):
    sorted_list = sorted(mentor_list, key=lambda x: x.capacity, reverse=True)
    return sorted_list

# Sorts the list of mentors by how many shifts they are available for
# Current remaining need: 27
def responses_sort(mentor_list):
    for mentor in mentor_list:
        for response in mentor.responses:
            if (response == 1):
                mentor.yes_responses += 1
    
    sorted_list = sorted(mentor_list, key=lambda x: x.yes_responses, reverse=True)
    return sorted_list

# Sorts the list of mentors by the average index of their yes responses
# The idea is to have mentors that said yes early but not as much late assigned to the first shifts,
# and the opposite for mentors that said the opposite.
# Current remaining need: 23
def index_sort(mentor_list):
    for mentor in mentor_list:
        yes_sum = 0
        for yes_index in range(len(mentor.responses)):
            if (mentor.responses[yes_index] == 1):
                yes_sum += yes_index
        mentor.avg_yes_index = yes_sum / len(mentor.responses)
    
    sorted_list = sorted(mentor_list, key=lambda x: x.avg_yes_index, reverse=True)
    return sorted_list