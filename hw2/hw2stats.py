import re
import numpy as np

# Open the file 'dialog-babi-task5-full-dialogs-trn.txt' and read the lines
with open('D:\\alexia\\Σχολή\\Διαλογικά\\assignment2\\data\\dialog-babi-task5-full-dialogs-trn.txt') as f:
    lines = f.readlines()

# Keep only the lines that contain a tab character, ignore search results lines
lines_clean = [line for line in lines if '\t' in line]

# Remove the line <SILENCE> when it is the first word in the dialogue
lines_no_silence = [re.sub('1 <SILENCE>', '', line) for line in lines_clean]

# Create empty lists 'user' and 'system' where we will store the user and system utterances
user = []
system = []

# Loop through the lines in 'lines_no_silence' list
for i in range(len(lines_no_silence)):
    if '<SILENCE>' not in lines_no_silence[i]:        # If the line does not contain '<SILENCE>'
       split_lines = lines_no_silence[i].split('\t')  # Split the line by the tab character
       user.append(split_lines[0])                    # and add the first part to 'user'
       system.append(split_lines[1])                  # and the second part to 'system'
    # If line contains '<SILENCE>'
    else:
        split_lines = lines_no_silence[i].split('\t') # Split the line by the tab character
        split_lines.remove(split_lines[0])            # remove the first part
        system.append(split_lines[0])                 # and concatenate the remaining parts
        system[-2] += system[-1]                      
        system.remove(system[-1])                     
         
# Print the number of turns by the user and by the system
print('Number of user turns:', len(user))
print('Number of system turns:', len(system))

# Count the number of dialogues
dialog_cnt = 0
for turn in user:
    tok = turn.split()
    if tok[0] == '1':
        dialog_cnt +=1

# Create an empty list where the number of turns in each dialogue will be stored
turn_cnt_list = []

turn_cnt = 0
for turn in user:
    tok = turn.split()                    # split the turn string into tokens
    turn_cnt +=1
    if tok[0] == '1':                     # if the first token is '1'
        turn_cnt_list.append(turn_cnt*2)  # append the double of turn counter to the list
        turn_cnt = 0                      # reset the turn counter

turn_cnt_list.remove(turn_cnt_list[0])  # Remove the first element from 'turn_cnt_list'

# Print the total number of dialogues
print('Total number of dialogues:', dialog_cnt) 

# clean the user and system turns by removing numbers
user_clean = [re.sub(r'[0-9]+', '', turn) for turn in user]
system_clean = [re.sub(r'[0-9]+', '', turn) for turn in system]

# tokenize the user and system turns
user_tokens = [turn.split() for turn in user_clean]
system_tokens = [turn.split() for turn in system_clean]
total_tokens = user_tokens + system_tokens  # merge the user and system tokens
total_tokens_flat = [token for turn in total_tokens for token in turn]

turn_lengths = [len(turn) for turn in total_tokens]  # calculate the lenght of each turn

print('Total number of turns:', len(total_tokens))                  # total number of turns
print('Total number of words:', len(total_tokens_flat))             # total number of words
print('Total number of vocab words:', len(set(total_tokens_flat)))  # total number of vocabulary words




print('Mean of words in turn:', np.mean(turn_lengths))    # mean of number of words in a turn
print('STD pf words in turn:', np.std(turn_lengths))      # standard deviation of words in a turn

print('Mean of turns in dialogue:', np.mean(turn_cnt_list))   # mean of number of turns in dialogue
print('STD of turns in dialogue:', np.std(turn_cnt_list))     # standard deviation of turns in a dialogue
