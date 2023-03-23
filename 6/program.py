import string
import math

def swap(key, message):

    key = list(key)
    message = list(message)

    for i in range(0, len(key)):
        key.append(key[i].lower())

    for i in range(0, len(message)):

        j = 0
        for k in range(0, len(key)):

            if j >= len(key):
                break

            if message[i] == key[j]:
                if j % 2 == 0:
                    # go forward one
                    message[i] = key[j + 1]
                    j += 1


                else:
                    # go back one
                    message[i] = key[j - 1]

            j += 1
            


    return "".join(message)



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

    letter_list = ['A', 'E', 'N', 'O', 'S', 'T']
    count = [0, 0, 0, 0, 0, 0]

    message = message.upper()

    for i in range(0, len(letter_list)):
        for j in range(0, len(message)):
           
            if letter_list[i] == message[j]:
               count[i] += 1

    for i in range(0, len(count)):
       max = count[i]
       max_index = i

       for j in range(i, len(count)):
          
        if count[j] > max:
            max = count[j]
            max_index = j

        if count[j] == max:
           if ord(letter_list[j]) < ord(letter_list[max_index]):
              max = count[j]
              max_index = j

        temp = count[i]
        count[i] = count[max_index]
        count[max_index] = temp

        temp = letter_list[i]
        letter_list[i] = letter_list[max_index]
        letter_list[max_index] = temp

    goal_list = ['E', 'T', 'A', 'O', 'N', 'S']

    match_count = 0

    for i in range(0, len(goal_list)):
       
        if goal_list[i] == letter_list[i]:
           match_count += 1

    return math.ceil((6 - match_count)/2)



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



def greedy(message, dictionary, threshold, letters):
    pass


# def greedy(message, dictionary, threshold, letters):

#     # queue = [message, 0, "", get_heuristic(message, False)]

#     current_message = message
#     current_depth = 0
#     current_key = ""

#     expanded = 1
#     max_fringe = 1
#     max_depth = 0

#     expanded_states = []

#     # start looping taking the first element off of the queue

#     while(True):

        
#         print(get_heuristic(current_message, False))
#         print(current_key)

#         if check_threshold(current_message, dictionary, threshold):
#             return 1, current_message, current_key, expanded, max_fringe, current_depth, expanded_states
        

#         # now we search the node

#         children = search_node(current_message, letters)

#         # and select the best node

#         min = get_heuristic(children[0], False)
#         index = 0

#         for i in range(2, len(children), 2):

#             heuristic = get_heuristic(children[i], False)

#             if min < heuristic:
#                 min = heuristic
#                 index = i

#         if len(children) + 1 > max_fringe:
#             max_fringe = len(children) + 1

#         # then set the current node to the best child:

#         current_message = children[index]
#         current_depth += 1
#         current_key += children[i + 1]
#         expanded += 1



#     return 0, None, None, expanded, max_fringe, current_depth, expanded_states







def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):

    try:
        message_f = open(message_filename, 'r')
        dict_f = open(dictionary_filename, 'r')
        message = message_f.read()
        dictionary = dict_f.read().upper().split("\n")
    except:
        return "File Error"

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



    # elif algorithm == 'u':
    #     status = ucs()


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
    # Example function calls below, you can add your own to test the task6 function
    # print(task6('g', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'))

    print(task6('g', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'n'))
    