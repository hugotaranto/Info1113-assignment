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



def task2(filename, letters):
    #TODO

    # Need to check through each letter pair and see if they can be performed or not

    

    try:
        f = open(filename, 'r')
        string = f.read()
    except:
        return "File Error"
    
    cap_string = string.upper()

    # sort letters alphabetically and make a list:

    letters_list = sorted(list(letters))


    # now iterate through the list and check each pair

    ret = ""

    count = 0

    for i in range(0, len(letters_list)):
        for j in range(i + 1, len(letters_list)):

            if letters_list[i] == letters_list[j]:
                continue

            if letters_list[i] not in cap_string and letters_list[j] not in cap_string:
                continue

            if count == 0:
                ret += "\n" + swap("" + letters_list[i] + letters_list[j], string)

            else:
                ret += "\n\n" + swap("" + letters_list[i] + letters_list[j], string)

            count += 1





    return str(count) + ret


if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task2 function
    print(task2('spain.txt', 'ABE'))



    # print(task2('ai.txt', 'XZ'))
    # print(task2('cabs.txt', 'ABZD'))
    
