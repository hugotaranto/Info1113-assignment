import string

def task3(message_filename, dictionary_filename, threshold):
    
    try:
        message_f = open(message_filename, 'r')
        dict_f = open(dictionary_filename, 'r')
        message = message_f.read().upper()
        dictionary = dict_f.read().upper().split("\n")
    except:
        return "File Error"

    # we need to remove punctuation, and need to split anywhere there is a line break

    message = message.translate(str.maketrans('', '', string.punctuation))
    message = message.replace("\n", " ")

    message = message.split(" ")

    count = 0

    for i in range(0, len(message)):
        if message[i] in dictionary:
            count += 1

    
    percentage = count * 100 / len(message)
    percentage = round(percentage, 2)

    ret = percentage >= threshold

    return "{}\n{:.2f}".format(ret, percentage)

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task3 function
    print(task3('jingle_bells.txt', 'dict_xmas.txt', 90))
    print(task3('fruit_ode.txt', 'dict_fruit.txt', 80))
    # print(task3('amazing_poetry.txt', 'common_words.txt', 95))
    