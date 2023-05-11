"""
File to be executed
"""

from create_matrix import create_matrix

PATH = 'data/liste_francais.txt'
#PATH = 'data/test.txt'

matrix2 = create_matrix(PATH)
print(matrix2)
