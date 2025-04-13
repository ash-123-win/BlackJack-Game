# BlackJack-Game
This is a simple text-based Blackjack game written in Python where you play against a dealer. The goal is to get a total hand value of 21 without exceeding it. You can place bets, hit, stand, and track your progress.

## Requirements

- Python 3.x
- `matplotlib` for generating the dealer's win probability graph.


To install `matplotlib`, run the following command:

```bash
pip install matplotlib
```

## How to Play


### Start the Game:

When you run the game, it will ask you how many games you want to play.

You will also choose the game speed (Normal or Fast).

### Betting:

You start with 500 units of money.

For each game, you place a bet (between 1 and 20 units).

### Gameplay:

Both you and the dealer are dealt two cards.

You will be asked to choose between "Hit" (get another card) or "Stand" (keep your current hand).

If your hand total exceeds 21, you lose (bust).

The dealer will follow the rules to play their hand automatically (drawing cards until reaching at least 17).

### End of Round:

If you win, your balance is updated with your bet.

If you lose, your balance decreases by the bet amount.

A graph showing the dealer's winning chances based on their first card is generated at the end of the game.

