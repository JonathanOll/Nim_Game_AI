from time import time
from random import randint, uniform


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.count = 12
        self.turn = bool(randint(0, 1))  # True = p1, False = p2

    def reset(self):
        self.count = 12
        self.turn = bool(randint(0, 1))

    def display(self):  # display the current state
        print("|" * self.count + "\n")

    def play(self):  # play one turn
        if not self.p1.bot or not self.p2.bot : self.display()
        if self.turn:
            self.count -= self.p1.play(self.count)
        else:
            self.count -= self.p2.play(self.count)

    def game(self):  # play a full game
        while self.count > 0:
            self.play()
            self.turn = not self.turn
        else:  # when the game is finished
            if self.turn:  # p1 won
                self.p1.train(1)
                self.p2.train(-1)
                if not self.p1.bot or not self.p2.bot : print(p1.name, "won")
            else:  # p2 won
                self.p1.train(-1)
                self.p2.train(1)
                if not self.p1.bot or not self.p2.bot : print(p2.name, "won")


class Player:
    def __init__(self, name, learn_rate, bot, training=True):
        self.name = name
        self.V = [0] * 12  # V-function
        self.history = []  # list of the states the game passed by
        self.learn_rate = learn_rate  # learning rate setting
        self.training = training  # current state, the bot is either training or not
        self.epsilon = 1.  # exploration setting
        self.bot = bot  # True: bot, False: real player

    def train(self, reward):  # updating the V-function parameters
        if not self.bot: return
        sp = reward
        for s in reversed(self.history):
            self.V[s-1] = self.V[s-1] + self.learn_rate * (sp - self.V[s-1])
            sp = self.V[s-1]
        self.history = []  # reseting the game state's history
        self.epsilon = max(self.epsilon * 0.99, 0.05)  # reducing the epsilon-parameter

    def greedy_play(self, count):  # Play smartly 
        best = None
        for a in range(1, 4):
            if count - a > 0 and (best is None or self.V[count-1-best] > self.V[count-1-a]):
                best = a
        return best if best is not None else 1

    def play(self, count):
        if self.bot:  # if the player is a bot
            self.history.append(count)
            if self.training and uniform(0, 1) < self.epsilon:  # exploration state
                return randint(1, 3)  # play randomly
            else:
                return self.greedy_play(count)
        else:  # or a real player
            while True:
                try:
                    r = int(input(">"))
                except:
                    continue
                if 1 <= r <= 3: return r

    def render(self):  # print V-function parameters
        for i, a in enumerate(self.V):
            print(i+1, ":", a)

if __name__ == "__main__":
    p1 = Player("Bot 1", 0.01, True, True)
    p2 = Player("Bot 2", 0.01, True, False)
    game = Game(p1, p2)

    # Train the AI before playing for real
    
    before = time()

    for a in range(100000):
        game.game()
        game.reset()

    p1.render()

    print("Process completed in", time() - before, ("secs" if time() - before >= 2 else "sec"))

    # Play with a real player

    while True:
        player = Player("Player", 0, False, False)
        game = Game(p1, player)
        game.game()
