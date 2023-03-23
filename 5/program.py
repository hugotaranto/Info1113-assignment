import math

def task5(message_filename, is_goal):
    
    if is_goal:
       return 0

    letter_list = ['A', 'E', 'N', 'O', 'S', 'T']
    count = [0, 0, 0, 0, 0, 0]

    try:
       f = open(message_filename, 'r')
       message = f.read().upper()
    except:
       return "File Error"

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

    match_count = 6
    
    for i in range(0, len(goal_list)):
       
        if goal_list[i] == letter_list[i]:
           match_count -= 1

    return math.ceil((match_count)/2)








if __name__ == '__main__':
  # Example function calls below, you can add your own to test the task5 function
#   print(task5('freq_eg1.txt', False))
#   print(task5('freq_eg1.txt', True))
#   print(task5('freq_eg2.txt', False))
   print(task5('in.txt', False))
