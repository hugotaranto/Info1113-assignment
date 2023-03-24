import string
import math

heuristic_cache = dict()

def swap(key, message):

    new_message = ""
    key0_lower = key[0].lower()
    key1_lower = key[1].lower()
    # go through the key list and do all the changes at each index of the message

    for i in range(0, len(message)):
        
        if message[i] == key[0]:
            new_message += key[1]
        
        elif message[i] == key0_lower:
            new_message += key1_lower

        elif message[i] == key[1]:
            new_message += key[0]

        elif message[i] == key1_lower:
            new_message += key0_lower

        else:
            new_message += message[i]

    return new_message



def search_node(message, letters):

    # Need to check through each letter pair and see if they can be performed or not

    
    cap_string = message.upper()

    # sort letters alphabetically and make a list:

    letters_list = sorted(list(letters))


    # now iterate through the list and check each pair

    ret = []


    for i in range(0, len(letters_list)):
        for j in range(i + 1, len(letters_list)):

            if letters_list[i] == letters_list[j]:
                continue

            if letters_list[i] not in cap_string and letters_list[j] not in cap_string:
                continue

            ret.append(swap("" + letters_list[i] + letters_list[j], message))
            ret.append("" + letters_list[i] + letters_list[j])

    return ret # a list containing the list of strings and next to it the two letters used, i.e. ["Bcas are taxis.", "AB"] where "Bcas are taxis." would be the result after transforming A<->B



def check_threshold(message, dictionary, threshold):
    
    message = message.upper().translate(str.maketrans('', '', string.punctuation)).replace("\n", " ").split(" ")

    count = 0

    for i in range(0, len(message)):
        if message[i] in dictionary:
            count += 1

    
    percentage = count * 100 / len(message)
    percentage = round(percentage, 2)

    return percentage >= threshold


def get_heuristic(message, is_goal):
    
    if is_goal:
       return 0

    message = message.upper()
    
    result = heuristic_cache.get(message)
    if result != None:
        return result


    letter_list = ['A', 'E', 'N', 'O', 'S', 'T']
    count = [0, 0, 0, 0, 0, 0]


    # count all of the letters

    for i in range(0, len(message)):
        for j in range(0, len(letter_list)):
           if message[i] == letter_list[j]:
              count[j] += 1


    # now we need to order the letter list given the counts of each

    # sort the count by high to low

    for i in range(0, 6):
        max = count[i]
        max_i = i

        for j in range(i + 1, 6):

            # check if this is the new max
            if max < count[j]:
               max = count[j]
               max_i = j

            # if occurence is the same, check alphabetical order
            if max == count[j]:
               if ord(letter_list[i]) > ord(letter_list[j]):
                  max = count[j]
                  max_i = j
          
        # now do the swap

        # swap the letter
        temp = letter_list[i]
        letter_list[i] = letter_list[max_i]
        letter_list[max_i] = temp

        # swap the count
        temp = count[i]
        count[i] = count[max_i]
        count[max_i] = temp


    goal_letters = ['E', 'T', 'A', 'O', 'N', 'S']

    out_of_place = 0

    for i in range(0, 6):
       if goal_letters[i] != letter_list[i]:
          out_of_place += 1

    result = math.ceil(out_of_place/2)

    heuristic_cache[message] = result

    return result




def xfs(type, message, dictionary, threshold, letters):

    # adding the root node onto the queue

    queue = [message, 0, ""]

    expanded = 0
    max_fringe = 1
    max_depth = 0

    expanded_states = []

    # start looping taking the first element off of the queue

    while(expanded < 1000):

        if len(queue)/3 > max_fringe:
            max_fringe = len(queue)/3

        try:

            if type == 'd':

                current_key = queue.pop(-1)
                current_depth = queue.pop(-1)
                current_message = queue.pop(-1)

            else:
                current_message = queue.pop(0)
                current_depth = queue.pop(0)
                current_key = queue.pop(0)
                
            expanded += 1
        except:
            break

        if len(expanded_states) != 10:
            expanded_states.append(current_message)

        if current_depth > max_depth:
            max_depth = current_depth

        # now check if the searched node is a match

        if check_threshold(current_message, dictionary, threshold):
            return 1, current_message, current_key, expanded, max_fringe, max_depth, expanded_states


        # otherwise expand and add children to end of queue

        children = search_node(current_message, letters)

        if type == 'd':

            for i in range(-2, len(children) * -1 -1, -2):
                queue.append(children[i])
                queue.append(current_depth + 1)
                queue.append(current_key + children[i + 1])
        else:
            for i in range(0, len(children), 2):
                queue.append(children[i])
                queue.append(current_depth + 1)
                queue.append(current_key + children[i + 1])

        if len(queue)/3 > max_fringe:
            max_fringe = len(queue)/3

    return 0, None, None, expanded, max_fringe, max_depth, expanded_states


def ids(message, dictionary, threshold, letters):

    # start with a depth limit of 1
    # explore that node and add children to frontier
    # increment depth limit and continue

    # each time the depth limit is incremented, restart from the root node

    # traverse in dfs style

    queue = [message, 0, ""]

    depth_limit = 1


    expanded = 0
    max_fringe = 1
    max_depth = 0

    expanded_states = []

    # start looping taking the first element off of the queue

    while(expanded < 1000):

        if len(queue)/3 > max_fringe:
            max_fringe = len(queue)/3

        try:
            current_key = queue.pop(-1)
            current_depth = queue.pop(-1)
            current_message = queue.pop(-1)
                
            expanded += 1
        except:
            depth_limit += 1
            queue = [message, 0, ""]
            continue

        if len(expanded_states) != 10:
            expanded_states.append(current_message)

        if current_depth > max_depth:
            max_depth = current_depth

        # now check if the searched node is a match

        if check_threshold(current_message, dictionary, threshold):
            return 1, current_message, current_key, expanded, max_fringe, max_depth, expanded_states


        # otherwise expand and add children to end of queue if they are not out of the depth limit

        if not depth_limit == current_depth + 1:


            children = search_node(current_message, letters)


            for i in range(-2, len(children) * -1 -1, -2):
                queue.append(children[i])
                queue.append(current_depth + 1)
                queue.append(current_key + children[i + 1])

            if len(queue)/3 > max_fringe:
                max_fringe = len(queue)/3

            if len(queue) == 0:
                break

    return 0, None, None, expanded, max_fringe, max_depth, expanded_states
    

def my_print(queue):

    print("\n\n--Printing Queue--\n\nPosition  Depth    Key used    Heuristic")

    for i in range(0, len(queue)):

        print(str(i).ljust(9), str(queue[i][1]).ljust(8), str(queue[i][2]).ljust(11), queue[i][3])






def greedy(message, dictionary, threshold, letters):

    queue = [[message, 0, "", get_heuristic(message, check_threshold(message, dictionary, threshold))]] # queue contains arrays of form: [message, depth, key, heuristic]

    expanded = 0
    max_fringe = 1
    max_depth = 0

    expanded_states = []

    heursitic_order = [0, 0, 0]

    # start looping taking the first element off of the queue

    while(expanded < 1000):

        if len(queue) == 0:
            break

        if len(queue) > max_fringe: # updating the max_fringe value if the queue is longer than the current max_fringe value
            max_fringe = len(queue)


        # now we pop off the first node in queue and expand it


        node = queue.pop(0)

        current_message = node[0]
        current_depth = node[1]
        current_key = node[2]

        # increment expanded value
        expanded += 1

        # update the heuristic order:

        for j in range(0, 3):
            if heursitic_order[j] > 0:
                heursitic_order[j] -= 1


        # adding the message to the list of expanded states

        if len(expanded_states) != 10:
            expanded_states.append(current_message)

        # updating max_depth value
        if current_depth > max_depth:
            max_depth = current_depth

        # checking if the expanded node is a solution

        if check_threshold(current_message, dictionary, threshold):
            return 1, current_message, current_key, expanded, max_fringe, max_depth, expanded_states
        

        # now we search the node and put children node into a list

        children = search_node(current_message, letters)


        # now we loop through children and add them to the queue in order of heuristic value

        for i in range(0, len(children), 2):
            
            heuristic = get_heuristic(children[i], check_threshold(children[i], dictionary, threshold))

            new_node = [children[i], current_depth + 1, current_key + children[i + 1], heuristic]

            if heuristic == 3:
                queue.append(new_node)
                continue

            # loop through the queue to find where the child goes in

            queue.insert(heursitic_order[heuristic], new_node)

            for j in range(heuristic, 3):
                heursitic_order[j] += 1


    if len(queue) > max_fringe: # updating the max_fringe value if the queue is longer than the current max_fringe value
        max_fringe = len(queue)


    return 0, None, None, expanded, max_fringe, max_depth, expanded_states



def a_star(message, dictionary, threshold, letters):

    queue = [[message, 0, "", get_heuristic(message, check_threshold(message, dictionary, threshold))]] # queue contains arrays of form: [message, depth, key, heuristic]

    expanded = 0
    max_fringe = 1
    max_depth = 0

    expanded_states = []

    queue_order = []




    # start looping taking the first element off of the queue

    while(expanded < 1000):

        if len(queue) == 0:
            break

        if len(queue) > max_fringe: # updating the max_fringe value if the queue is longer than the current max_fringe value
            max_fringe = len(queue)


        # now we pop off the first node in queue and expand it

        node = queue.pop(0)

        current_message = node[0]
        current_depth = node[1]
        current_key = node[2]

        # increment expanded value
        expanded += 1


        # update queue_order

        for j in range(0, len(queue_order)):
            if queue_order[j] > 0:
                queue_order[j] -= 1


        # adding the message to the list of expanded states

        if len(expanded_states) != 10:
            expanded_states.append(current_message)

        # updating max_depth value
        if current_depth > max_depth:
            max_depth = current_depth

        # checking if the expanded node is a solution

        if check_threshold(current_message, dictionary, threshold):
            return 1, current_message, current_key, expanded, max_fringe, max_depth, expanded_states
        

        # now we search the node and put children node into a list

        children = search_node(current_message, letters)


        # now we loop through children and add them to the queue in order of heuristic value

        for i in range(0, len(children), 2):
            
            score = get_heuristic(children[i], check_threshold(children[i], dictionary, threshold)) + current_depth + 1

            new_node = [children[i], current_depth + 1, current_key + children[i + 1], score]


            # add the node to the queue:


            # we are going to check if the value is bigger than any stored in the queue so far

            while score + 1 > len(queue_order):
                queue_order.append(len(queue))

            queue.insert(queue_order[score], new_node)

            # then update the queue_order

            for j in range(score, len(queue_order)):
                queue_order[j] += 1




    if len(queue) > max_fringe: # updating the max_fringe value if the queue is longer than the current max_fringe value
        max_fringe = len(queue)


    return 0, None, None, expanded, max_fringe, max_depth, expanded_states





def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):

    try:
        message_f = open(message_filename, 'r')
        dict_f = open(dictionary_filename, 'r')
        message = message_f.read()
        dictionary = dict_f.read().upper().split("\n")
    except:
        return "File Error"

    # making the dictionary a set for optimisation
    dictionary = set(dictionary)

    # we have the message as a string


    # stop the search if 1000 nodes have been searched

    status = -1

    # these functions will return: return type, solution, key_found, num_expanded, max_fringe, max_depth


    if algorithm == 'd':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = xfs('d', message, dictionary, threshold, letters)
    elif algorithm == 'b' or algorithm == 'u':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = xfs('b', message, dictionary, threshold, letters)
    elif algorithm == 'i':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = ids(message, dictionary, threshold, letters)
    elif algorithm == 'g':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = greedy(message, dictionary, threshold, letters)
    elif algorithm == 'a':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = a_star(message, dictionary, threshold, letters)


    if status == 0:
        ret = "No solution found.\n\nNum nodes expanded: {}\nMax fringe size: {:.0f}\nMax depth: {}".format(num_expanded, max_fringe, max_depth)

    elif status == 1:
        ret = "Solution: {}\n\nKey: {}\nPath Cost: {:.0f}\n\nNum nodes expanded: {}\nMax fringe size: {:.0f}\nMax depth: {}".format(
            solution, key_found, len(key_found)/2, num_expanded, max_fringe, max_depth)

    else:
        return "Incorrect inputs given"


    if debug == 'y':
        return ret + "\n\nFirst few expanded states:\n" + "\n\n".join(expanded_states)

    else:
        return ret

    
if __name__ == '__main__':

    pass
    