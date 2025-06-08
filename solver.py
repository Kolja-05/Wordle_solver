from collections import defaultdict
import math
import re
import copy

#collect all words from answers.txt
WORDS = []
with open('answers.txt', 'r') as file:
    for line in file:
        word = line.strip()
        WORDS.append(word)

# compare guess to true_word and get a color pattern
def compare_words_to_colors(true_word, guess):
    color_feedback = ''
    for idx, letter in enumerate(guess):
        true_letter = true_word[idx]
        if letter == true_letter:
            color_feedback += "G"
        elif letter in true_word:
            color_feedback += "Y"
        else:
            color_feedback += "B"
    return color_feedback

#calculate expected information gain for each word in set of all 5 letter words
def calculate_expected_information_gain(possible_solutions):
    expected_information_gain = defaultdict(float)

    for possible_guess in WORDS:
        pattern_count = defaultdict(int)
        for possible_word in possible_solutions:
            pattern = compare_words_to_colors(possible_word, possible_guess) 
            pattern_count[pattern] += 1
        
        pattern_probability = {pattern: count / len(possible_solutions)
            for pattern, count in pattern_count.items()
        }
        for p in pattern_probability.values():
            expected_information_gain[possible_guess] -= p * math.log2(p)
    return expected_information_gain

def calculate_best_guess(possible_solutions):
    expected_information_gain = calculate_expected_information_gain(possible_solutions)
    if len(possible_solutions)>0:
        best_guess = possible_solutions[0]
    else:
        best_guess = None
    best_score = 0
    for word in WORDS:
        if expected_information_gain[word] > best_score:
            best_guess = word
            best_score = expected_information_gain[word]
    return best_guess

#process guess and colors, remove words from list, that are not valid guesses anymore
def filter_by_feedback(possible_solutions, letter, y_pos, g_pos, b_pos):
    new_possible_solutions = []
    for word in possible_solutions:
        if len(b_pos) == 0 and word.count(letter) >= len(y_pos)+len(g_pos):
            if all(word[pos_y] != letter for pos_y in y_pos) and all(word[pos_g] == letter for pos_g in g_pos):
                new_possible_solutions.append(word)
        elif len(b_pos) > 0 and word.count(letter) == len(y_pos)+len(g_pos) and len(y_pos)+len(g_pos) > 0:
            if all(word[pos_y] != letter for pos_y in y_pos) and all(word[pos_g] == letter for pos_g in g_pos) and all(word[pos_b] != letter for pos_b in b_pos):
                new_possible_solutions.append(word)
        elif len(b_pos) > 0 and len(y_pos)+len(g_pos) == 0:
            if letter not in word:
                new_possible_solutions.append(word)
    return new_possible_solutions

def color_positions(guess, colors):
    letter_feedback = {}

    for idx, letter in enumerate(guess):
        if letter not in letter_feedback:
            letter_feedback[letter] = {"b_pos": [], "y_pos": [], "g_pos": []}
        if colors[idx] == "B":
            letter_feedback[letter]["b_pos"].append(idx)
        elif colors[idx] == "Y":
            letter_feedback[letter]["y_pos"].append(idx)
        elif colors[idx] == "G":
            letter_feedback[letter]["g_pos"].append(idx)
    return letter_feedback

def filter(possible_solutions, feedback):
    for letter, pos in feedback.items():
        possible_solutions = filter_by_feedback(
            possible_solutions, 
            letter, 
            pos["y_pos"],
            pos["g_pos"],
            pos["b_pos"]
        )
    return possible_solutions





########    SOLVER  ##################




if __name__ == "__main__":
    possible_solutions = copy.deepcopy(WORDS)

    while True:
        print("There are ", len(possible_solutions) , " possible solutions")
        if len(possible_solutions) < 50:
            print(possible_solutions)
        #start by calculateing the best guess based on all possible answers
        best_guess = calculate_best_guess(possible_solutions)
        print("The best guess is: ", best_guess)

        # let the user enter the word he chose commented out to not give the user a choice
        #guess = input("Enter a word: ")
        #assert re.fullmatch(r'^[a-z]{5}', guess)

        # or instead let the guess be the best guess
        guess = best_guess

        #the output of the game (colors of the letters)
        colors = input("Enter color output by game as string in ^[BGY]{5}, where B=black, Y=yellow, G=green:, where 0=grey, 1=yellow, 2=green:  ")
        assert re.fullmatch(r'^[BGY]{5}', colors)

        #filter words
        feedback = color_positions(guess, colors)
        possible_solutions = filter(possible_solutions, feedback)
