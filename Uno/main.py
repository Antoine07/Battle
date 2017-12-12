import random as r

"""
Constantes 
"""

COLORS = {'red' : [1,25], 'blue' : [26,50], 'yellow' : [51, 75], 'green' : [76, 100], 'multicolor' : [101, 108]}

SPEC = {
    0:'0',1: '1',2: '2',3 : '3',4 : '4',5 : '5',6 : '6',7 : '7' ,8 : '8', 9: '9',
    10:"+2", 
    11: "Changement de sens", 
    12: "Passe ton tour", 
    101: "Joker", 102 : "Joker", 103: "Joker", 104: "Joker",
    105: "+4", 106 : "+4", 107: "+4", 108 :"+4"
}

"""
Fonctions utiles
"""

def color_card(num):
    """ Return color la couleur de la carte """

    for color, info in COLORS.items():
        if num > (info[0]-1) and num < info[1] + 1:
            return color

def number_card(num):
    """ Return le numéro de la carte dans sa couleur ou les numéros de la carte joker """

    pos = list(range(1, 13))

    zeros = {1, 26, 51, 76}

    if num in zeros:
        return 0

    if num > 100:
        return num
    
    d = 0

    if num > 1 and num < 26:
        d = 2

    if num > 26 and num < 51:
        d = 3

    if num > 51 and num < 76:
        d = 4 

    if num > 76:
        d = 5

    return pos[((num-d) % 12)]


def text_card(num):
    """ Return un texte présentant la carte que l'on souhaite jouer ou None """

    color = color_card(num)
    number = number_card(num)


    if number in SPEC:
        return "{} {}".format(SPEC[number], color)

    return "{} {}".format(number, color)


def pickaxe_cards(pickaxes, num):
    """ Return une pioche du tas des pioches, et la pioche diminuée de ce que l'on vient de prendre """

    try:
        if not pickaxes or len(pickaxes) < num:
            raise ValueError("plus de carte dans la pioche") 

        player_pickaxes = []

        for i in range(num):
            card = pickaxes[i]
            player_pickaxes.append(card)
            pickaxes.remove(card)
        
        return player_pickaxes, pickaxes

    except ValueError:
        return None
    
def draw(pic, hand, num_card):
    """ Return la pioche avec la carte pioché en moins et la main augmentée de la carte piochée """

    for _ in range(num_card):
        p = number_card(pic)
        if p is None:
            return None

        pic.remove(p)
        hand.append(p)
    
    return pic, hand
    

def display_hand(hand):
    """ Return la main d'un joueur """

    info_hand = []
    for num in hand:
        info_hand.append(text_card(num))

    return ", ".join(info_hand)


def empty_pick(pic, cards):
    """ Return la pioche mélangée et la carte sur la pioche et si plus de carte lève une exception """
    try:
        pic = cards + pic
        
        if not pic:
            raise ValueError("Il n'y a plus de carte")

        r.shuffle(pic)
        last_card = pic.pop() # ne pas mettre la dernière carte dans la pioche la retourner

        return pic, last_card

    except ValueError as e:
        return e.args
        
def get_possibles_cards(hand, pic):
    """ Return les cartes possibles à jouer pour un joueur ou None si aucune carte n'est possible """

    possibles = {'color': [], 'number' : [], 'joker' : [], '+4' : [], '+2' : []}
    constraints = {10, 105, 106, 107, 108} # +2 ou +4
    jokers = {101,102,103,104} 

    for p in hand:

        color_p = color_card(p)
        color_pic = color_card(pic)
        num_p = number_card(p)
        num_pic = number_card(pic)

        if color_p == color_pic:
            possibles['color'].append(p)
        
        if num_p == num_pic and num_p in {10}:
            possibles['+2'].append(p)

        if num_p == num_pic and num_p not in {10}:
            possibles['number'].append(p)

        # joker 
        if num_pic not in constraints and num_p in jokers :
            possibles['joker'].append(p)

        # +4
        if num_p in {105, 106, 107, 108}:
            possibles['+4'].append(p)
    
    possTest = False
    for key, poss in possibles.items():
        if not poss:
            possTest = True
            break

    if possTest:
        return possibles

    return None

def penalities(seq):
    """ Return le nombre de carte à jouer en cas de carte +2 ou +4 """

    num_of_playing_cards = 0
    for num in seq:
        num = number_card(num)
        if num in {10}:
            num_of_playing_cards += 2
        if num in {105, 106, 107, 108}:
            num_of_playing_cards += 4

    return num_of_playing_cards

def is_playable(hand, pic):
    """ Return une carte ou des cartes jouable(s) ou None """ 

    cards = get_possibles_cards(hand, pic)

    # on vérifie que l'on a bien des carte à jouer sinon on retourne None
    if not cards:
        return None

    choice_damage_4 = len(cards['+4'])
    choice_damage_2 = len(cards['+2'])

    if choice_damage_4 > 0:
        if choice_damage_2 > 0:
            res = cards['+4'] + cards['+2']
            h = set(hand) - set(res)
            hand = list(h)

            return res, hand
        else:
            res = cards['+4']
            h = set(hand) - set(res)
            hand = list(h)

            return res, hand
    
    if choice_damage_2:
        res = cards['+2']
        h = set(hand) - set(res)
        hand = list(h)

        return res, hand

    # sens ou sauter un tour
    if len(cards['color']) > 0:
        for color in cards['color']:
            if number_card(color) == 11:
                hand.remove(color)

                return [color], hand

            if number_card(color) == 12:
                hand.remove(color)

                return [color], hand

    # sinon le max de nombre identiques
    if len(cards['number']) > 1:
        res = cards['number']
        h = set(hand) - set(res)
        hand = list(h)
        return res, hand
    
    # ou une couleur ou un nombre ?
    if len(cards['color']) > 0:

    return res, hand
    

def init(cards):
    """ Return un dictionnaire initialisant le jeu """

    init = {
    'cards' : [],
    'pickaxes' : [],
    'pickaxe' : [], # peut être une séquence
    'direction' : 1,
    'number_player' : 0,
    'number_player_cards' : 0,
    'players' : [],
    'who_plays' : 0    # ordre des joueurs
    }
    
    nb_player = input("Nombre de joueur \n")

    while nb_player.isdigit() == False:
        nb_player = input("Nombre de joueur, un entier svp \n")
    
    nb_player = int(nb_player)
    init['number_player'] = nb_player

    number_player_cards = input("Nombre de cartes par joueur \n")

    while number_player_cards.isdigit() == False or (nb_player * int(number_player_cards) > 108):
        number_player_cards = input("Nombre de cartes par joueur, un entier svp ou un nombre possible \n")
    
    number_player_cards = int(number_player_cards)
    init['number_player_cards'] = number_player_cards
    
    for num in range(1, nb_player + 1):
        name_player = input("Donnez le nom du joueur {} \n".format(num))
        hand = cards[0:number_player_cards]
        del cards[0:number_player_cards]

        init['players'].append({
            'name' : name_player, 
            'hand' : hand, 
            'nb_cards' : number_player_cards, 
            'pos' : num 
            })

    init['who_plays'] = 0

    middle = len(cards) // 2

    init['pickaxes'] = cards[0:middle]
    init['pickaxe'].append(init['pickaxes'].pop())

    del cards[0:middle]

    init['cards'] = cards
    
    return init


def sens_rotation(last_card, status):
    """ Return le prochain le nom du prochain joueur """
    pic = number_card(last_card)
    jump = 0

    if pic == 11:
        status['direction'] = status['direction']*(-1)

    if pic == 12:
        jump = 1

    nb_player = status['number_player']
    sens = status['direction']

    who_plays = (status['who_plays'] + (1 + jump)*sens) % nb_player

    return who_plays



    
    

