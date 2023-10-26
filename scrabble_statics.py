# The values of each tile given their letter
LETTER_VALUE = [
    1, # A
    3, # B
    3, # C
    2, # D
    1, # E
    4, # F
    2, # G
    4, # H
    1, # I
    8, # J
    5, # K
    1, # L
    3, # M
    1, # N
    1, # O
    3, # P
    10, # Q
    1, # R
    1, # S
    1, # T
    1, # U
    4, # V
    4, # W
    8, # X
    4, # Y
    10 # Z
]

# Convert from letter char into array index
def charIndex(ch):
    return ord(ch) - 65

# Get letter value given letter char
def letterValue(ch):
    return LETTER_VALUE[charIndex(ch)]

# Given a word, get the value it originally make without score modifier
def wordValue(word):
    value = 0
    for ch in word:
        value += LETTER_VALUE[charIndex(ch)]
    return value