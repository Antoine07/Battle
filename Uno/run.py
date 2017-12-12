import main as game
import random as r

"""
Variables globales
"""
CARDS = list(range(1,109))


for i in range(1, 109):
    print(game.number_card(i), game.text_card(i), i)

r.shuffle(CARDS)
status = {}
# status = game.init(CARDS)

status = {'number_player_cards': 8, 
'who_plays': 0, 'direction': 1, 'number_player': 2, 
'pickaxes': [64, 47, 29, 95, 55, 11, 66, 32, 43, 25, 107, 71, 105, 1, 33, 96, 48, 39, 67, 20, 85 , 15, 23, 79, 78, 7, 86, 58, 94, 98, 14, 82, 30, 72, 22, 80, 54, 10, 36, 5, 99, 3, 106, 75, 17], 
'cards': [101, 100, 92, 93, 65, 60, 62, 59, 40, 35, 84, 91, 50, 27, 24, 41, 12, 83, 102, 2, 74, 87, 63, 77, 8, 61, 103, 81, 53, 37, 90, 89, 38, 49, 69, 16, 45, 6, 28, 108, 42, 97, 18, 56, 26, 104], 
'players': [{'nb_cards': 8, 'pos': 1, 'name': 
'Antoine', 'hand': [46, 68, 31, 52, 73, 70, 34, 21]}, {'nb_cards': 8, 'pos': 2, 'name': 'Naoudi', 'hand': [19, 51, 88, 13, 57, 4, 44, 76]}], 
'pickaxe': [84]}

count = 0
while count != 4:

    seq = status['pickaxe']

    who_plays = game.sens_rotation(seq[0], status)
    player = status['players'][who_plays] # sens et passer son tour ?
    print(" c'est le tour de ", player['name'], " à jouer, votre main :", game.display_hand(player['hand'])) # qui joue

    # on n'oublie pas de noter qui vient de jouer ?
    status['who_plays'] = who_plays

    penalities = game.penalities(seq) # y a  t il des pénalitées ?

    if penalities is 0:
        possibles_cards = game.get_possibles_cards(player['hand'], status['pickaxe'][0])
        print( "voici vos cartes possibles :", possibles_cards ) # à formater

        cards, hand = game.is_playable(player['hand'], status['pickaxe'][0])
        player['hand'] = hand
        player['nb_cards'] -= len(cards)

        print("Vous jouer :", game.display_hand(cards))

        # combien doit-il en poicher maintenant qu'il vient de jouer ?
        nb_cards = status['number_player_cards'] - player['nb_cards']
        print("Vous devez piocher :", nb_cards, " carte(s)")

        new_pic, new_pickaxes =  game.pickaxe_cards(status['pickaxes'], nb_cards )

        status['pickaxes'] = new_pickaxes
        player['hand'] += new_pic
        player['nb_cards'] = len(player['hand'])

        print("Voici votre nouvelle main :", game.display_hand(player['hand']))

    else:
        print(player['name'], "vous avez des pénalitées :" , penalities)

        player['hand'] += game.pickaxe_cards(status['pickaxes'], penalities)
        player['nb_cards'] = len(player['hand'])

    count +=1


