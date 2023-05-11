"""
Create a matrix to store probabilities
"""

import codecs
import re
import numpy as np
from tqdm import tqdm

from utils import letter_to_index

REGEX_LETTRE =re.compile('[a-z]')
REGEX_MOT_COMPOSE = re.compile('.+-.+')
ACCENT = ['̀', '̂', '́', '̧', '̈']


def create_complete_list (file_path : str) -> list :
    """
    Create a list that contains all the caracters in the language
    Count the accents and special caracters

    Parameters :
        file_path (str) : Path of a file that contains words

    Returns :
        returned_list (list) : The sorted list that contains the caracters
    """
    letters = []
    compteur_lettre = 0
    with codecs.open(file_path, 'r', 'utf-8') as file :
        for line in file :
            if not REGEX_MOT_COMPOSE.match(line) :
                for j in enumerate(line) :
                    if REGEX_LETTRE.match(j[1]) :
                        compteur_lettre += 1
                        if line[j[0]+1] in ACCENT :
                            letter = line[j[0] : j[0]+2].lower()
                        else :
                            letter = j[1].lower()

                        if letter not in letters :
                            letters.append(letter)

    letters.sort()

    returned_list = ['start'] + letters + ['end']
    return returned_list

def create_simple_list (file_path : str) -> list :
    """
    Create a list that contains all the caracters in the language.
    Doesn't count the accents or special caracters.

    Parameters :
        file_path (str) : Path of a file that contains words

    Returns :
        returned_list (list) : The sorted list that contains the caracters
    """
    letters = []
    with codecs.open(file_path, 'r', 'utf-8') as file :
        for line in file :
            if not REGEX_MOT_COMPOSE.match(line) :
                for j in enumerate(line) :
                    if REGEX_LETTRE.match(j[1]) :
                        if j[1] not in letters :
                            letters.append(j[1].lower())

    letters.sort()

    returned_list = ['start'] + letters + ['end']

    return returned_list

def handle_letter_without_accent (matrix : np.array,
                                  letters_list : list,
                                  line : str,
                                  letter : str) -> None :
    """
    Udpdate the matrix according to the new letter
    Doesn't handle accents and special caracters

    Parameters :
        matrix (np.array) : The matrix
        letters_list (list) : The list of all the letters
        line (str) : The current line in the file
        letter (str) : The current letter

    No return
    """
    index1 = letter_to_index(letters_list, letter[1].lower())
    if letter[0] == 0 :
        index2 = 0
        matrix[index1][index2] += 1

        if REGEX_LETTRE.match(line[letter[0]+1]) :
            index3= letter_to_index(letters_list, line[letter[0]+1].lower())
        else :
            index3 = letter_to_index(letters_list, line[letter[0]+2].lower())
        matrix[index3][index1] += 1

    elif letter[0] == len(line) - 2:
        index2 = len(letters_list) - 1
        matrix[index2][index1] += 1
    elif REGEX_LETTRE.match(line[letter[0]+1]) :
        index2 = letter_to_index(letters_list, line[letter[0]+1].lower())
        matrix[index2][index1] += 1
    else :
        index2 = letter_to_index(letters_list, line[letter[0]+2].lower())
        matrix[index2][index1] += 1


def handle_letter_with_accent (matrix : np.array,
                                  letters_list : list,
                                  line : str,
                                  letter : str) -> None :
    """
    Udpdate the matrix according to the new letter
    Handle accents and special caracters

    Parameters :
        matrix (np.array) : The matrix
        letters_list (list) : The list of all the letters
        line (str) : The current line in the file
        letter (str) : The current letter

    No return
    """
    step = len(letter[1])
    index1 = letter_to_index(letters_list, letter[1].lower())

    if letter[0] == len(line) - 3:
        index2 = len(letters_list) - 1
        matrix[index2][index1] += 1

    elif letter[0] == 0 :
        index2 = 0
        matrix[index1][index2] += 1

        if line[letter[0]+step] in ('\n', '\r') :
            index3 = -1

        elif REGEX_LETTRE.match(line[letter[0]+step].lower()) :
            index3= letter_to_index(letters_list, line[letter[0]+step].lower())
        else :
            index3 = letter_to_index(letters_list, line[letter[0]+step:letter[0]+step+2].lower())
        matrix[index3][index1] += 1

    elif line[letter[0]+step] in ('\n', '\r') :
        index3 = -1
    elif REGEX_LETTRE.match(line[letter[0]+step].lower()) :
        index2 = letter_to_index(letters_list, line[letter[0]+step].lower())
        matrix[index2][index1] += 1
    else :
        index2 = letter_to_index(letters_list, line[letter[0]+step:letter[0]+step+2].lower())
        matrix[index2][index1] += 1




def create_simple_matrix (file_path : str) -> np.array :
    """
    Create a matrix that contains the caracters probability
    Doesn't handle accents and special caracters

    Parameters :
        file_path (str) : Path of a file that contains words

    Returns :
        matrix (np.array) : An array that contains the probabilities
    """
    letters_list = create_simple_list(file_path)
    dimension = len(letters_list)

    matrix = np.array([[0.0]*dimension]*dimension)

    with codecs.open(file_path, 'r', 'utf-8') as file :
        for line in file :
            if not REGEX_MOT_COMPOSE.match(line) :
                for letter in enumerate(line) :
                    if REGEX_LETTRE.match(letter[1].lower()) :
                        handle_letter_without_accent(matrix, letters_list, line, letter)

    for col in enumerate(matrix.T) :
        total = sum(col[1])
        if total == 0 :
            total = 1
        for item in enumerate(matrix[:,col[0]]) :
            frequency = round(item[1]/total*10000)/100
            matrix[item[0], col[0]] = frequency

    return matrix

def create_complete_matrix (file_path : str) -> np.array :
    """
    Create a matrix that contains the caracters probability
    Handle accent and special caracters

    Parameters :
        file_path (str) : Path of a file that contains words

    Returns :
        matrix (np.array) : An array that contains the probabilities
    """
    letters_list = create_complete_list(file_path)
    dimension = len(letters_list)

    matrix = np.array([[0]*dimension]*dimension)

    with codecs.open(file_path, 'r', 'utf-8') as file :
        p_bar = tqdm(total=336531)
        for line in file :
            p_bar.update(1)
            if not REGEX_MOT_COMPOSE.match(line) :
                for letter in enumerate(line) :
                    if REGEX_LETTRE.match(letter[1].lower()) :
                        if line[letter[0]+1] in ACCENT :
                            special_letter = (letter[0], line[letter[0]:letter[0]+2])
                        else :
                            special_letter = letter
                        handle_letter_with_accent(matrix, letters_list, line, special_letter)
        p_bar.close()

    for col in enumerate(matrix.T) :
        total = float(sum(col[1]))
        if total == 0 :
            total = 1
        for item in enumerate(matrix[:,col[0]]) :
            frequency = round(item[1]/total*10000)/100
            matrix[item[0], col[0]] = frequency

    return matrix

def create_matrix (file_path : str, complete : bool = True) -> np.array :
    """
    Create the wanted matrix

    Parameters :
        file_path (str) : Path of a file that contains words
        complete (bool, default True) : Do you want a complete matrix or not ?

    Returns :
        matrix (np.array) : An array that contains the probabilities
    """
    if complete :
        return create_complete_matrix(file_path)
    return create_simple_matrix(file_path)
