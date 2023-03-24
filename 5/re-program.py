import math

def task5(message_filename, is_goal):
  
    if is_goal:
       return 0

    try:
       f = open(message_filename)
       message = f.read().upper()
    except:
       return "File Error"
    

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


    # print(count)
    # print(letter_list)

    goal_letters = ['E', 'T', 'A', 'O', 'N', 'S']

    out_of_place = 0

    for i in range(0, 6):
       if goal_letters[i] != letter_list[i]:
          out_of_place += 1

    return math.ceil(out_of_place/2)
    

if __name__ == '__main__':
  # Example function calls below, you can add your own to test the task5 function
#   print(task5('freq_eg1.txt', False))
#   print(task5('freq_eg1.txt', True))
#   print(task5('freq_eg2.txt', False))
    print(task5('in.txt', False))