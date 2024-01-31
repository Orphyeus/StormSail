from Characters import *
from Location import *


class Game:
    """This class manages the basic flow and state of the game."""

    def __init__(self):
        """Initializes the starting state of the game."""
        self.players = []  # List of players
        self.day_count = 0  # Count of days passed
        self.is_night = False  # Checks if it is night
        self.storm_chance = 0.15  # Chance of a storm occurring
        self.journey_days = 4  # Total duration of the journey
        self.cellar = Cellar()  # Creation of the cellar
        self.deck = Deck()  # Creation of the deck

    def add_player(self, player):
        """Adds a new player."""
        self.players.append(player)

    def start_day(self):
        """Starts the day and manages day-related events."""
        self.is_night = False
        self.day_count += 1
        is_storm = self.check_storm()
        self.cellar.update_conditions(self.is_night, is_storm)
        self.deck.update_conditions(self.is_night, is_storm)
        if not is_storm:
            self.vote()

    def start_night(self):
        """Starts the night and manages night-time events."""
        self.is_night = True
        print(f"Night {self.day_count} begins.")
        is_storm = self.check_storm()
        self.cellar.update_conditions(self.is_night, is_storm)
        self.deck.update_conditions(self.is_night, is_storm)
        if not is_storm:
            for player in self.players:
                if player.character.is_alive:
                    player.character.perform_action(self.players)

    def check_storm(self):
        """Checks for a storm and initiates necessary actions if there is one."""
        if random.random() < self.storm_chance:
            print("A storm has hit the ship!")
            if self.is_night:
                self.storm_at_night()
            else:
                storm_at_day()
            return True
        return False

    def storm_at_night(self):
        """Actions to be taken during a night-time storm."""
        potential_victims = [p for p in self.players if p.character.is_alive and p.character.role != "Pirate"]
        if potential_victims:
            victim = random.choice(potential_victims)
            victim.character.is_alive = False
            print(f"{victim.name} has fallen overboard and drowned!")

    def vote(self):
        """The voting process where players vote to eliminate each other."""
        print("Voting time!")
        votes = {player.name: 0 for player in self.players if player.character.is_alive}
        for player in self.players:
            if player.character.is_alive:
                voted_player_name = input(f"{player.name}, who do you vote for? ")
                votes[voted_player_name] += 1
        eliminated_player = max(votes, key=votes.get)
        for player in self.players:
            if player.name == eliminated_player:
                player.character.is_alive = False
                print(f"{eliminated_player} has been eliminated!")

    def check_win_conditions(self):
        """Checks the win conditions of the game."""
        good_alive = sum(1 for p in self.players if p.character.alignment == "Good" and p.character.is_alive)
        evil_alive = sum(1 for p in self.players if p.character.alignment == "Evil" and p.character.is_alive)
        if not evil_alive:
            print("The good side wins!")
            return True
        elif good_alive <= evil_alive:
            print("The evil side wins!")
            return True
        elif self.day_count > self.journey_days:
            print("The voyage is complete! The good side wins!")
            return True
        return False

    def setup_game(self):
        """Sets up the game with players and characters."""
        print("Setting up the game...")

        # Instantiate one of each character class
        character_instances = [
            Captain("Captain Jack"),
            Navigator("Navigator Joe"),
            StormBringer("Stormy Dan"),
            Alchemist("Alchemist Ann"),
            Lookout("Lookout Lee"),
            DiplomaticEnvoy("Envoy Eve"),
            EnvoysGuard("Guard Gabe"),
            Mercenary("Mercenary Max"),
            Assassin("Assassin Alex"),
            OrdinaryPassenger("Passenger Pat")
        ]

        # Create players for each character instance
        for index, character in enumerate(character_instances):
            player_name = f"Player {index + 1}"
            self.players.append(Player(player_name, character))

        # Optional: Create additional players if needed, potentially reusing character classes
        additional_players_count = 0  # Or however many additional players you want
        for i in range(len(character_instances), len(character_instances) + additional_players_count):
            character_class = random.choice(character_instances)
            character_name = f"{character_class.__name__} {i + 1}"
            character = character_class(character_name)
            player = Player(f"Player {i + 1}", character)
            self.add_player(player)

    def start_game(self):
        """Starts the game and manages the game loop."""
        print("Welcome to Stormy Voyage!")
        self.setup_game()
        while not self.check_win_conditions():
            self.start_day()
            self.start_night()


def storm_at_day():
    """Actions to be taken during a daytime storm."""
    print("The crew is too busy dealing with the storm to hold a vote.")
