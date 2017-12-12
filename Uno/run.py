import main as game
import random as r

"""
Variables globales
"""

CARDS = list(range(1,109))

r.shuffle(CARDS)

# cartes possibles
print(game.get_possibles_cards([1,5,100,101,105,7, 11], 23))

for i in range(1, 109):
    print(game.number_card(i), game.text_card(i), i)

""" 
tests de pénalité(s)
"""

print(game.penalities([23, 11, 48, 105, 106, 107]))

"""
Return une carte jouable 
"""

print(game.is_playable([1,5,100,101,105,7], 32))