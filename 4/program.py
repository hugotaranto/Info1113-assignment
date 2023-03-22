import string

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





def ids():
    pass


def ucs():
    pass




def task4(algorithm, message_filename, dictionary_filename, threshold, letters, debug):

    try:
        message_f = open(message_filename, 'r')
        dict_f = open(dictionary_filename, 'r')
        message = message_f.read()
        dictionary = dict_f.read().upper().split("\n")
    except:
        return "File Error"

    # we have the message as a string


    # stop the search if 1000 nodes have been searched
    # ret is set to 0 if the solution was not found

    status = -1

    # these functions will return: return type, solution, key_found, num_expanded, max_fringe, max_depth


    if algorithm == 'd':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = xfs('d', message, dictionary, threshold, letters)
    elif algorithm == 'b':
        status, solution, key_found, num_expanded, max_fringe, max_depth, expanded_states = xfs('b', message, dictionary, threshold, letters)
    elif algorithm == 'i':
        status = ids()
    elif algorithm == 'u':
        status = ucs()


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
    # Example function calls below, you can add your own to test the task4 function
    # print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    # print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    