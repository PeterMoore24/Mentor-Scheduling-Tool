def capacity_sort(mentor_list):
    sorted_list = sorted(mentor_list, key=lambda x: x.capacity, reverse=True)
    return sorted_list

def responses_sort(mentor_list):
    for mentor in mentor_list:
        for response in mentor.responses:
            if (response == 1):
                mentor.yes_responses += 1
    
    sorted_list = sorted(mentor_list, key=lambda x: x.yes_responses, reverse=True)
    print(sorted_list)
    print(mentor_list)
    return sorted_list