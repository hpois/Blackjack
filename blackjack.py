import random

try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter


def load_images(card_images):
    """Creates a list of card images"""
    suits = ['heart', 'spade', 'club', 'diamond']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'
    # for each suit, retrieve the image for the cards
    for suit in suits:
        # firs the number cards 1 to 10
        for card in range(1, 11):
            name = f'cards/{card}_{suit}.{extension}'
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))
        # next the face cards
        for card in face_cards:
            name = f'cards/{card}_{suit}.{extension}'
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    """pop the next card off the top of the deck and
    add the image to a Label and display the label"""
    try:
        next_card = deck.pop(0)
        tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
        return next_card
    except IndexError:
        result_text.set("No more cards. Reshuffling deck")
        shuffle_deck()
        next_card = deck.pop(0)
        tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
        return next_card


def score_hand(hand):
    """Calculate the total score of all cards from a list containing tuples.
    Only one ace can have the value of 11, and reduce it to 1 if the hand would have bust"""
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            card_value += 10
            ace = True
        score += card_value
        # if we would bust check for the ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    """Automatically hits the dealer until it cannot by house rules. (Dealer hits less than 17)."""
    global dealer_wins, player_wins, game_over
    dealer_score = score_hand(dealer_hand)
    if not game_over:
        while 0 < dealer_score < 17:
            dealer_hand.append(_deal_card(dealer_card_frame))
            dealer_score = score_hand(dealer_hand)
            dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if (player_score > 21) and not game_over:
        dealer_wins += 1
        game_over = True
        dealer_win_label.set(dealer_wins)
        result_text.set("Dealer Wins")
    elif (dealer_score > 21 or dealer_score < player_score) and not game_over:
        player_wins += 1
        game_over = True
        player_win_label.set(player_wins)
        result_text.set("Player Wins")
    elif (dealer_score > player_score) and not game_over:
        dealer_wins += 1
        game_over = True
        dealer_win_label.set(dealer_wins)
        result_text.set("Dealer Wins")
    elif dealer_score == player_score:
        game_over = True
        result_text.set("Push")


def deal_player():
    global dealer_wins
    global game_over
    """Deals the player another card, adds the value of the card to `player_score`.
    Checks for a bust or blackjack and sends that to `result_text`"""
    if not game_over:
        player_hand.append(_deal_card(player_card_frame))
        player_score = score_hand(player_hand)
        player_score_label.set(player_score)
        if player_score > 21 and not game_over:
            dealer_wins += 1
            game_over = True
            dealer_win_label.set(dealer_wins)
            dealer_hand.append(_deal_card(dealer_card_frame))
            dealer_score = score_hand(dealer_hand)
            dealer_score_label.set(dealer_score)
            result_text.set("Dealer Wins")
        if player_score == 21:
            result_text.set("Player Blackjack Poggers in the doggers")
            deal_dealer()
    else:
        result_text.set('Please start a new game')


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def play_another_game():
    """Resets the game board for a new game."""
    global player_card_frame, dealer_card_frame
    global dealer_hand, player_hand, game_over

    player_card_frame.destroy()
    dealer_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    result_text.set('')

    # Create the list to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []
    game_over = False

    initial_deal()


def shuffle_deck():
    """Reshuffles the order of the deck and fills it back up with deleted cards"""
    global cards, deck
    cards = []
    load_images(cards)

    deck = list(cards)
    random.shuffle(deck)


def play():
    # Setting up min/max size of window
    mainWindow.update()
    min_height = card_frame.winfo_height() * 2 + button_frame.winfo_height() + score_frame.winfo_height() + \
        score_frame.winfo_height()
    min_width = card_frame.winfo_width() + button_frame.winfo_width() + score_frame.winfo_width()

    mainWindow.minsize(width=min_width, height=min_height)
    mainWindow.maxsize(width=min_width + 20, height=min_height + 20)

    initial_deal()
    mainWindow.mainloop()


mainWindow = tkinter.Tk()

# Set up the screen and frames for the dealer and the player
mainWindow.title("Blackjack")
mainWindow.geometry('640x480')
mainWindow.configure(background='green')
mainWindow['padx'] = 10

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text, background='green', fg='white')
result.grid(row=0, column=0, columnspan=2)

card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)
card_frame.columnconfigure(1, weight=1000)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)

# Win counter
score_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
score_frame.grid(row=6, column=0, columnspan=1, sticky='nsew')

dealer_win_label = tkinter.IntVar()
dealer_win_frame = tkinter.Frame(score_frame, relief='sunken', borderwidth=1, background='green')
dealer_win_frame.grid(row=0, column=0, rowspan=2, sticky='ew')
tkinter.Label(dealer_win_frame, text='Dealer Wins:', background='green', fg='white').grid(row=0, column=0)
tkinter.Label(dealer_win_frame, textvariable=dealer_win_label, background='green', fg='white').grid(row=1, column=0)

player_win_label = tkinter.IntVar()
player_win_frame = tkinter.Frame(score_frame, relief='sunken', borderwidth=1, background='green')
player_win_frame.grid(row=0, column=1, rowspan=2, sticky='ew')
tkinter.Label(player_win_frame, text='Player Wins:', background='green', fg='white').grid(row=0, column=0)
tkinter.Label(player_win_frame, textvariable=player_win_label, background='green', fg='white').grid(row=1, column=0)

# embedded frame hold the dealer card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)
# embedded frame to hold the player card images
player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

# Adding the buttons
button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, rowspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text='Pass', command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text='Hit Me', command=deal_player)
player_button.grid(row=0, column=1)

retry_button = tkinter.Button(button_frame, text='Play again', command=play_another_game)
retry_button.grid(row=0, column=2)

# Initializing the tally for games won
player_wins = 0
dealer_wins = 0

# Initializing the hands and win state
dealer_hand = []
player_hand = []
game_over = False

# Creating and shuffling the deck
cards = []
load_images(cards)
deck = list(cards)
random.shuffle(deck)

if __name__ == '__main__':
    play()
