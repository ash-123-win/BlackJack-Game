import random
import time
import tkinter

import matplotlib.pyplot as plt


class Player:
    def __init__(self):
        self.hand = []
        self.score = None

        self.money = 500
        self.games = 0
        self.bet = 0
        self.score = 0
        self.earning_factor = 0

    def generate_deck(self, deck):
        """
            Generate the first decks to players and dealer
        """
        hand = []
        for i in range(2):
            random.shuffle(deck)
            card = deck.pop()
            if card == 11:
                card = "J"
            if card == 12:
                card = "Q"
            if card == 13:
                card = "K"
            if card == 1:
                card = "A"
            hand.append(card)
        self.hand = hand

    def hand_cards_sum(self):
        """
            compute the sum of cards of the hand
        """
        cards_sum = 0
        for card in self.hand:
            if card in ["J", "Q", "K"]:
                cards_sum += 10
            elif card == "A":
                if cards_sum >= 11:
                    cards_sum += 1
                else:
                    cards_sum += 11
            else:
                cards_sum += card
        return cards_sum

    def hit(self, deck):
        """
            get a new card from the deck, and add it to the hand
        """
        card = deck.pop()
        if card == 11:
            card = "J"
        if card == 12:
            card = "Q"
        if card == 13:
            card = "K"
        if card == 1:
            card = "A"
        self.hand.append(card)

    def set_score(self, deck):
        """
            compute the score of the player 0: busted, BlackJack: if player got 21,
             otherwise the sum of the player's hand
        """
        if self.hand_cards_sum() == 21:
            print("Congratulations! You got a Blackjack!\n")
            self.score = "BlackJack"
            return "BlackJack"
        while True:
            choice = input("Do you want to Hit (H), Stand (S) ? ").lower()
            if choice == "h":
                self.hit(deck)
                print(self.hand)
                print("Hand cards total: " + str(self.hand_cards_sum()))
                if self.hand_cards_sum() > 21:
                    print('You busted !')
                    self.score = 0
                    return 0
            elif choice == 's':
                self.score = self.hand_cards_sum()
                return self.hand_cards_sum()
            else:
                print("Please enter a valid choice: (H) or (S).")

    def win_or_lose(self, dealer_score):
        """
            show the final result
        """
        if self.score == "BlackJack":
            return [3, "You won with a BlackJack !!!"]
        elif self.score != "BlackJack" and dealer_score == "BlackJack":
            return [0, "You loose, the dealer got a BlackJack !"]
        elif self.score == 0 or dealer_score > self.score:
            return [0, "You lose !"]
        elif self.score == dealer_score:
            return [1, "You draw !"]
        else:
            return [2, "You won !!"]


class Dealer(Player):

    def __init__(self):
        super().__init__()
        self.stats = {}
        self.game_speed = "n"

    def set_score(self, deck):
        """
                compute the score of the dealer 0: busted, BlackJack: if dealer got 21,
                 otherwise the sum of the dealer's hand
        """
        self.pause_game(self.game_speed)

        print("  Dealer cards: " + str(self.hand) + "\n")
        i = 1
        if self.hand_cards_sum() == 21:
            self.pause_game(self.game_speed)
            print("Dealer got a Blackjack !")
            self.score = "BlackJack"
            return "BlackJack"
        while self.hand_cards_sum() < 17:
            self.pause_game(self.game_speed)
            self.hit(deck)
            i += 1
            print("    - Hit " + str(i) + ": " + str(self.hand[-1]))
            print("       Dealer new hand: " + str(self.hand) + " for a total of " + str(self.hand_cards_sum()))
            if self.hand_cards_sum() > 21:
                print('Dealer busts !')
                self.score = 0
                return 0
        self.score = self.hand_cards_sum()
        return self.hand_cards_sum()

    def win_or_lose(self, dealer_score):
        pass

    def plot_graph(self, game_number):
        gui_window = tkinter.Tk()
        gui_window.geometry("300x300")

        def graph_generator():
            # Create a histogram plot
            plt.hist(self.stats.keys(), weights=[self.stats[key] / game_number for key in self.stats])
            plt.title("Dealer probability of winning according to his first card")
            plt.xlabel("1st dealer card")
            plt.ylabel("Probability of win")
            plt.show()

        graph_button = tkinter.Button(gui_window, text="Generate graph", command=graph_generator)
        graph_button.pack(pady=30)
        gui_window.mainloop()

    def update_stats(self, player_earning_factor):
        if player_earning_factor == 0:
            if str(self.hand[0]) in self.stats:
                self.stats[str(self.hand[0])] += 1
            else:
                self.stats[str(self.hand[0])] = 1

    @staticmethod
    def pause_game(game_speed):
        if game_speed == "n":
            time.sleep(3)


class Game:
    def __init__(self):
        self.number_of_games_to_play = 0
        self.game_speed = "n"

    def run(self):
        # display first screen of the game
        print("\n\nWELCOME TO BLACKJACK !!!")
        print("------------------------------\n")

        # get number of games
        self.number_of_games_to_play = \
            self.get_integer_input("Could you please enter the number of games you want to play ? ")

        # get game speed
        self.game_speed = self.get_speed_input("Could you please enter the game speed Normal (N) or Fast (F) ? ")

        # player and dealer
        player = Player()
        dealer = Dealer()

        game_number = 0
        while self.number_of_games_to_play != 0 and player.money != 0:

            # display game number
            game_number += 1
            print("\n\nGame number: " + str(game_number))
            print("---------------\n\n")

            # init deck
            deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * 4
            random.shuffle(deck)

            # reduce game number by 1
            self.number_of_games_to_play = self.number_of_games_to_play - 1

            # generate dealer hand
            dealer.generate_deck(deck)

            # player bets
            self.pause_game(self.game_speed)
            player.games += 1
            player.bet = self.get_user_bet("Player : could you please bet ? ", player.money)
            player.generate_deck(deck)

            # Show first dealer card and players cards
            self.pause_game(self.game_speed)
            print("\n\n")
            print("The first dealer card is: " + str(dealer.hand[0]))
            if player.money != 0:
                print("Player have a " + str(player.hand) + " for a total of " + str(player.hand_cards_sum()))

            # get each player score
            self.pause_game(self.game_speed)
            print("\n\n>>> Player:\n")
            player.set_score(deck)

            self.pause_game(self.game_speed)
            print("\n\n>>> Dealer: \n")
            dealer.game_speed = self.game_speed
            dealer.set_score(deck)

            # display winners and losers
            print("\n\n\n******* Results *******\n")
            self.pause_game(self.game_speed)
            player.money = player.money - player.bet
            player.earning_factor, player_1_msg_to_display = player.win_or_lose(dealer.score)
            print("Player: " + player_1_msg_to_display)
            player.money = player.money + player.bet * player.earning_factor

            # display Summary:
            print("\n\n******* Summary *******\n")
            self.pause_game(self.game_speed)
            print("- Games Played: " + str(game_number) +
                  "\n\n- Player Games: " + str(player.games) +
                  "\n- Player Account: " + str(player.money) + " Euro")

            self.pause_game(self.game_speed)

            # save dealer wining stats
            dealer.update_stats(player.earning_factor)

        dealer.plot_graph(game_number)

    @staticmethod
    def get_integer_input(qst):
        user_input = input(qst)
        while not user_input.isdigit() or user_input == '0':
            user_input = input("Could you please enter a valid input: integer and different from 0 ? ")
        return int(user_input)

    @staticmethod
    def get_speed_input(qst):
        user_input = input(qst).lower()
        while user_input not in ["n", "f"]:
            user_input = input("Could you please enter a valid input: (F) or (N) ? ")
        return user_input

    @staticmethod
    def get_user_bet(qst, player_money):
        user_input = input(qst)
        while not user_input.isdigit() or user_input == '0' \
                or int(user_input) > 20 or (player_money - int(user_input)) < 0:
            if not user_input.isdigit() or user_input == '0' or int(user_input) > 20:
                user_input = input("Could you please enter a valid bet: integer and 0 < value <= 20 ? ")
            elif (player_money - int(user_input)) < 0:
                user_input = input("Could you please enter a valid bet: not more than what you have in your account ? ")
        return int(user_input)

    @staticmethod
    def pause_game(game_speed):
        if game_speed == "n":
            time.sleep(3)


# init game and run
game = Game()
game.run()