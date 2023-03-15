
def swap(key, filename):

    try:
        f = open(filename, 'r')
    except:
        return 'File Error'

    message = list(f.read())
    key = list(key)

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




def task1(key, filename, indicator):

    if indicator != 'd' and indicator != 'e':
        return ''

    if indicator == 'd':
        key = key[::-1]
        
    return swap(key, filename)


if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task1 function

    print(task1('AE', 'spain.txt', 'd'))
    print(task1('VFSC', 'ai.txt', 'd'))
    print(task1('ABBC', 'cabs_plain.txt', 'e'))

