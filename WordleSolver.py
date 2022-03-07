import os

def generate_word_dict(input_path):
    word_dict = {}
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in alphabet:
        word_dict[letter] = []
    f = open(input_path)
    for line in f:
        if len(line.strip()) > 0:
            for letter in line.strip():
                if line.strip() not in word_dict[letter]:
                    word_dict[letter].append(line.strip())
    return word_dict

def generate_word_dict_with_array(array):
    word_dict = {}
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in alphabet:
        word_dict[letter] = []
    for word in array:
        for letter in word:
            word_dict[letter].append(word)
    return word_dict

def find_most_common_letters(word_dict,exclude_array = []):
    letter_freq_dict = {}
    for key in word_dict.keys():
        letter_freq_dict[key] = len(word_dict[key])
    for letter in exclude_array:
        letter_freq_dict.pop(letter)
    letter_freq_dict = {k: v for k, v in sorted(letter_freq_dict.items(), key=lambda item: item[1])}
    freq_dict_list = list(letter_freq_dict.keys())
    most_common = freq_dict_list[-5:]
    return most_common

def find_word_with_letters(letter_list, dict):
    letters = set(letter_list)
    word_list = dict[letter_list[4]]
    
    for word in word_list:
        if check_if_word_contains_all_letters(word, letter_list[:4]):
            print("Check with:",word,'\n')
            return
    
    for i in range(0, len(letter_list)):
        letters = letter_list[0:i] + letter_list[i+1:5]
        word_list = dict[letters[-1]]
        
        for word in word_list:
            if check_if_word_contains_all_letters(word, letters):
                print("Check with:",word,'\n')
                return

    for i in range(0, len(letter_list)):
        for j in range (i+1, len(letter_list)):
            letters = letter_list[0:i] + letter_list[i+1:j] + letter_list[j+1:5]
            word_list = dict[letters[-1]]
            for word in word_list:
                if check_if_word_contains_all_letters(word, letters):
                    print("Check with:",word,'\n')
                    return

    for i in range(0, len(letter_list)):
        for j in range(i+1, len(letter_list)):
            for k in range(j+1, len(letter_list)):
                letters = letter_list[0:i] + letter_list[i+1:j] + letter_list[j+1:k] + letter_list[k+1:5]
                word_list = dict[letters[-1]]
                for word in word_list:
                    if check_if_word_contains_all_letters(word, letters):
                        print("Check with:",word,'\n')
                        return
    return 

def check_if_word_contains_all_letters(word,letter_list):
    for letter in letter_list:
        if letter not in word:
            return False
    return True

def check_if_word_contains_some_letters(word,letter_list):
    for letter in letter_list:
        if letter in word:
            return True
    return False

def check_if_word_is_valid(word, possible_letters, bad_letters, solution_so_far):
    if check_if_word_contains_all_letters(word, possible_letters) and not check_if_word_contains_some_letters(word, bad_letters):
        index = 0
        for letter in solution_so_far:
            if letter == '_':
                pass
            else:
                if word[index] != letter:
                    return False
            index += 1
        return True
    else:
        return False

"""
# Phase 1:
    Try to find a letter to which to pull the dictionary
    if not, remove dictionaries of guessed letters, mark them as forbidden letters
    remove forbidden letter words from other dicts
    then guess again based on highest frequency letters

# Phase 2:
    When a yellow or green letter is found - pull that letter dict 
    if multiple yellows or greens are found - pull from any letter dict
    then limit to only those with all found letters
    rebuild letter dicts based on available word list

    if green letters are found, form a character array of size five, filled with '_'
    replace '_' with any green letters in correct index

    make function that accepts arguments of possible solutions, found letters, and indexed letters
    prunes the possible solutions and returns the new solution list

    if solution list is 1, return the solution
"""


def main():
    input_text_path = 'C:/Users/nguye/Desktop/WordleSolver/guesses.txt'
    
    guesses = generate_word_dict(input_text_path)
    word_dict = generate_word_dict(input_text_path)

    possible_letters = []
    bad_letters = []

    solution_so_far = ['_', '_', '_', '_', '_']

    # Phase 1
    while len(possible_letters) == 0:
        most_common = find_most_common_letters(word_dict)
        print('Most common remaining letters are now :', most_common)
        find_word_with_letters(most_common, guesses)
        
        # accepts user input
        input_word = input("Enter word input:")
        input_word = input_word.lower()
        print("\nWhite: W (Letter not present in word)\nYellow:Y (Letter present in word)\nGreen:G (Letter present in word and correct location)\n")
        input_colors = input("Input if letter was white, yellow, or green in format XXXXX:")
        input_colors = input_colors.upper()

        # parses user input
        color_index = 0
        for color in input_colors:
            letter = input_word[color_index]
            if color == 'W':
                if letter not in bad_letters:
                    bad_letters.append(letter)
                    word_dict.pop(letter)
            if color == 'Y':
                if letter not in possible_letters:
                    possible_letters.append(letter)
                
            if color == 'G':
                if letter not in possible_letters:
                    possible_letters.append(letter)
                solution_so_far[color_index] = input_word[color_index]
            color_index += 1
        
        print('Possible letters:',possible_letters)
        print('Bad letters:',bad_letters)
        print('Solution so far:',solution_so_far)


        # removes bad words from leftover dicts
        for key, values in word_dict.items():
            new_array = []
            for value in values:
                if not check_if_word_is_valid(value, possible_letters, bad_letters, solution_so_far):
                    pass
                else:
                    new_array.append(value)
            word_dict[key] = new_array
        
    # Phase 2
    possible_solutions = word_dict[possible_letters[0]]

    while len(possible_solutions) > 1:
        print("There are {} possible solutions.".format(len(possible_solutions)))
        word_dict = generate_word_dict_with_array(possible_solutions)
        if len(possible_solutions) > 5:
            most_common = find_most_common_letters(word_dict, possible_letters)
            print('Most common remaining letters are now :', most_common)
            find_word_with_letters(most_common, guesses)

        # accepts user input
        input_word = input("Enter word input:")
        input_word = input_word.lower()
        print("\nWhite: W (Letter not present in word)\nYellow: Y (Letter present in word)\nGreen: G (Letter present in word and correct location)\n")
        input_colors = input("Input if letter was white, yellow, or green in format XXXXX:")
        input_colors = input_colors.upper()

        # parses user input
        color_index = 0
        for color in input_colors:
            letter = input_word[color_index]
            if color == 'W':
                if letter not in bad_letters and letter not in possible_letters:
                    bad_letters.append(letter)
            if color == 'Y':
                if letter not in possible_letters:
                    possible_letters.append(letter)
            if color == 'G':
                if letter not in possible_letters:
                    possible_letters.append(letter)
                solution_so_far[color_index] = input_word[color_index]
            color_index += 1

        print('Possible letters:',possible_letters)
        print('Bad letters:',bad_letters)
        print('Solution so far:',solution_so_far,'\n')
        


        # removes bad words from leftover solutions
        new_array = []
        for word in possible_solutions:
            if not check_if_word_is_valid(word, possible_letters, bad_letters, solution_so_far):
                pass
            else:
                new_array.append(word)
        possible_solutions = new_array
        if len(possible_solutions) <= 5:
            print('Remaining solutions:', possible_solutions)
    print('The solution is:',possible_solutions[0])

if __name__ == '__main__':
    main()
