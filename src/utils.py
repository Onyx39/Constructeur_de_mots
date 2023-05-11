"""
File contains usefull functions
"""

def letter_to_index (letter_list : list, letter : str) -> int :
    """
    Give the index of the letter in a list

    Parameters :
        letter_list (list) : The list of the letters
        letter (str) : The letter we want

    Returns :
        The index of the letter (int)
    """
    if letter in ('\n', '\r') :
        return -1
    for i in enumerate(letter_list) :
        if i[1] == letter :
            return i[0]
    raise ValueError (f"index not found\n{letter_list}\n{letter}")
