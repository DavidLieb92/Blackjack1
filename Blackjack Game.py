#First setting up the cards for the game
import random
card_suits = ["Clubs", "Diamonds", "Hearts","Spades"]
card_types = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
score_dict = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":10, "Queen":10, "King":10}

#First places all the cards in an organized fashion, then randomly adds cards to the game deck
def shuffle_deck():
    full_card_deck = []
    #Number below to set the number of decks used; this defualts to 5
    for i in range(5):
        for suit in card_suits:
            for number in card_types:
                full_card_deck.append([number, suit])
    shuffled_game_deck = []
    for i in range(52):
        shuffled_card = random.randint(0,len(full_card_deck)-1)
        shuffled_game_deck.append(full_card_deck.pop(shuffled_card))
    return shuffled_game_deck

#Creating Player class, which will be both the player and the Dealer
class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.deck_value = 0
    
    #Code to rest player hand and deck for new game
    def reset_hand(self):
        self.deck = []
        self.deck_value = 0
    
    #Checks if the hand has an Ace in the hand. Returns True if it does
    def has_ace(self):
        return (True in [card[0] == "Ace" for card in self.deck])

    #Checks score of current hand, and assigns value of Ace to 11 or 1 depending on player hand
    #Adding in code to account for 2 Aces
    def check_score(self):
        self.deck_value = 0
        deck_length = len(self.deck)
        for card in self.deck:
            if card[0] in score_dict.keys():
                self.deck_value += score_dict[card[0]]
                deck_length -= 1
        if self.has_ace():
            for i in range(deck_length):
                if self.deck_value > 10:
                    self.deck_value += 1
                else:
                    self.deck_value += 11
        return self.deck_value

    #Draws card and adds to deck, and takes card away from the deck. Also shows the card drawn if it is not
    #used to set up the initial hand
    def draw_card(self, selected_deck, opening_hand=False):
        self.deck.append(selected_deck.pop(0))
        if not opening_hand:
            print("\n{name} drew a {value} of {suit}".format(name=self.name, value=self.deck[-1][0], suit=self.deck[-1][1]))
    
    def display_score(self):
        print("\n{name}'s deck is worth {points}.".format(name=self.name,points=self.check_score()))
        continue_text = input("\nPress Enter to continue ")

    def is_busted(self):
        return self.check_score() > 21
    
    def has_blackjack(self):
        return self.check_score() == 21 and len(self.deck) == 2

def display_cards(player):
    print("\n{name}'s cards are as follows:".format(name=player.name))
    for card in player.deck:
        print("{value} of {suit}".format(value=card[0],suit=card[1]))

#Code for Yes/No answer checking
def yes_or_no():
    player_answer = input("Type Y/N and press Enter: ")
    while player_answer.upper() != "Y" and player_answer.upper() != "N":
        player_answer = input("Invalid response. Type Y/N and press Enter: ")
    if player_answer.upper() == "Y":
        return True
    return False

#Code to ask player for wager. If wager is a negative number, greater than the total money available,
#or a non-number, it will keep asking until it gets a valid wager
def set_wager(total_money):
    confirmed_wager = False
    is_wager_valid = False
    while not confirmed_wager:
        is_wager_valid = False
        wager = input("\nHow much do you want to wager? ")
        while not is_wager_valid:
            try:
                if float(wager) > total_money or float(wager) < 0:
                    wager = input("Invalid bet. Enter a bet amount. ")
                else:
                    is_wager_valid = True
            except ValueError:
                wager = input("Invalid bet. Enter a bet amount. ")
        print("Your bet is ${bet}. Is this correct?".format(bet=wager))
        confirmed_wager = yes_or_no()
    return round(float(wager),2)

def play_fold():
    game_status = True
    did_player_win = False
    print("You Surrender!")
    return game_status, did_player_win

#Note: in this game, if both players have a blackjack, it is a tie. The second argument can be changed to True
#when we call the function if we want the dealer to hit on soft 17s (default is to stand)
def play_stand(current_deck, hits_on_soft_17 = False):
    display_cards(my_player)
    display_cards(dealer)
    game_status = False
    did_player_win = False
    is_tie = False
    print("\nThe dealer's second card is the {value} of {suit}".format(name=dealer.name, value=dealer.deck[-1][0], suit=dealer.deck[-1][1]))
    dealer.display_score()
    while not game_status:
        if dealer.check_score() > 17:
            game_status = True
            print("\nDealer holds.")
        elif dealer.check_score() < 17 or (dealer.check_score() == 17 and hits_on_soft_17 == True):
            print("\nDealer hits.")
            dealer.draw_card(current_deck)
            display_cards(dealer)
            dealer.display_score()
            if dealer.is_busted():
                game_status = True
                did_player_win = True
                print("\nDealer busts!")
    if my_player.check_score() == 21 and dealer.has_blackjack():
        print("\nDealer has a blackjack!")    
    elif my_player.check_score() == dealer.check_score() and not dealer.has_blackjack():
        is_tie = True
    elif my_player.check_score() > dealer.check_score():
        did_player_win = True
    return game_status, did_player_win, is_tie

#Executes the hit choice
def play_hit(player, current_deck):
    player.draw_card(current_deck)
    game_status = False
    if my_player.is_busted() and not dealer.is_busted():
        print("\nYou bust!")
        game_status = True
    else:
        display_cards(my_player)
        my_player.display_score()
    return game_status

#Starting up code for splitting. For now, just checking if opening hand can be split. 
#We will count face cards and 10 cards as being able to split
#Returns two values: first if the player has two cards to split, and second if they are both Aces
def can_split_hand(player):
    if player.deck[0][0] == "Ace" or player.deck[1][0] == "Ace":
        return (player.deck[0][0] == player.deck[1][0]), (player.deck[0][0] == "Ace" and player.deck[1][0] == "Ace")
    else:
        return (score_dict[player.deck[0][0]] == score_dict[player.deck[1][0]]), False

#Prints the outcome of the came
def print_outcomes(did_player_win, is_tie):
    if did_player_win:
        print("You win!")
    elif is_tie:
        print("You push! It's a tie")
    elif not did_player_win and not is_tie:
        print("You lose!")

#The actual code to excecute each game round
def play_round(player_money):
    is_game_over = False
    did_player_win = False
    is_tie = False
    wager_multiplier = 1
    insurance_bet = 0
    game_deck = shuffle_deck()
    print("You have ${total_money} available.".format(total_money=player_money))
    player_wager = set_wager(player_money)
    #Setting up initial two cards
    for i in range(2):
        my_player.draw_card(game_deck,True)
        dealer.draw_card(game_deck,True)
    display_cards(my_player)
    my_player.display_score()
    print("\nThe dealer's top card is the {dealer_value} of {dealer_suit}.".format(dealer_value=dealer.deck[0][0], dealer_suit=dealer.deck[0][1]))
    if my_player.has_blackjack() and not dealer.has_blackjack():
        wager_multiplier = 1.5
        is_game_over = True
        did_player_win = True
        display_cards(dealer)
        dealer.display_score()
        print("\nYou have a blackjack!")
    elif my_player.has_blackjack() and dealer.has_blackjack():
        is_game_over = True
        is_tie = True
        display_cards(dealer)
        print("\nYou both have a blackjack!")
    else:
        #Adding in code to ask for insurance
        if dealer.deck[0][0] == "Ace":
            print("Would you like insurance?")
            player_wants_insurance = yes_or_no()
            if player_wants_insurance:
                insurance_bet = set_wager(player_wager/2)
        while is_game_over == False:
            #Code starts out with three options: Hit, stand, and surrender. Working on code to add in doubling down
            game_choices = {"A":"Hit","B":"Stand","C":"Surrender","D":"Double Down"}
            input_text = "\nWhat do you wish to do?"
            for key in game_choices.keys():
                if key == "D" and (player_wager * 2) > player_money:
                    break
                input_text += "\n{option}: {action} ".format(option=key, action = game_choices[key])
            game_choice = input(input_text)
            while not game_choice.upper() in game_choices.keys():
                is_game_over = input("\nInvalid choice. Please select one of the above choices. ")
            if game_choice.upper() == "B":
                is_game_over, did_player_win, is_tie = play_stand(game_deck,True)
            elif game_choice.upper() == "C":
                is_game_over, did_player_win = play_fold()
                wager_multiplier = 0.5
            elif game_choice.upper() == "D":
                wager_multiplier = 2
                is_game_over = play_hit(my_player,game_deck)
                if not my_player.is_busted():
                    is_game_over, did_player_win, is_tie = play_stand(game_deck,True)
            else:
                is_game_over = play_hit(my_player,game_deck)
    print_outcomes(did_player_win, is_tie)
    return did_player_win, is_tie, wager_multiplier, player_wager, insurance_bet

#Function to check if player won and to settle bets:
def settle_bets(player_win, is_tie, wager_multiplier, player_money, wager, insurance_bet):
    has_money = True
    if player_win:
        player_money += wager * wager_multiplier
        player_money -= insurance_bet
    if not player_win and not is_tie:
        player_money -= (wager * wager_multiplier)
        if dealer.has_blackjack():
            player_money += (insurance_bet * 2)
        else:
            player_money -= insurance_bet
    if player_money <= 0:
        has_money = False
    print("You currently have ${money}.".format(money=player_money))
    return has_money, player_money

#Play again will now check if player has money. If not, the game ends. If so, it will
#ask if the player wants to play again.
def play_again(has_money):
    if not has_money:
        print("\nYou're out of money! Game over.")
        return True
    else:
        play_again = input("\nWould you like to play again? (Y/N) ")
        while play_again.upper() != "Y" and play_again.upper() != "N":
            play_again = input("Invalid entry. Enter Y or N" )
    if play_again.upper() == "Y":
        return False
    else:
        print("Thanks for playing!")
        return True

#To start, this game will just do the player and the dealer. Future iterations will involve more players
my_player = Player("David")
dealer = Player("Dealer")

#Opening message, player can just start by hitting enter
print("Welcome to Blackjack!")
start_game = input("\nPress Enter to start a game!")

#Code to play a new round:
is_game_over = False
player_money = 100.00
while not is_game_over:
    player_win, is_tie, wager_multiplier, player_bet, insurance_bet = play_round(player_money)
    player_has_money, player_money = settle_bets(player_win, is_tie, wager_multiplier, player_money, player_bet, insurance_bet)
    is_game_over = play_again(player_has_money)
    my_player.reset_hand()
    dealer.reset_hand()