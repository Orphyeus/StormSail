from Characters import *
from Location import *


class Game:
    """This class manages the basic flow and state of the game."""

    def __init__(self):
        """Initializes the starting state of the game."""
        self.players = []  # List of players
        self.day_count = 0  # Count of days passed
        self.is_night = False  # Checks if it is night
        self.storm_probability = 0.15  # Chance of a storm occurring
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
        """Starts the night and manages nighttime events."""
        self.is_night = True
        print(f"Night {self.day_count} begins.")
        is_storm = self.check_storm()
        self.cellar.update_conditions(self.is_night, is_storm)
        self.deck.update_conditions(self.is_night, is_storm)
        if not is_storm:
            for player in self.players:
                if player.character.is_alive:
                    if player.character.action_type == "Aggressive":

                        target_name = input(f"{player.name}, who do you attack? (Leave blank for no target): ")

                        if target_name.strip():  # If input is not empty and not just whitespace
                            # Find the target player by name
                            target = next((p for p in self.players if p.name == target_name), None)

                            if target:  # If a target is found
                                player.character.perform_action(self, target)
                            else:
                                print(f"Target not found: {target_name}")
                        else:
                            print(f"{player.name} chooses not to attack anyone this turn.")
                            # Here, you can add any special action that should be taken when no target is chosen.

                    elif player.character.action_type == "Strategic":
                        player.character.perform_action(self)

    def check_storm(self):
        """Checks for a storm and initiates necessary actions if there is one."""
        if random.random() < self.storm_probability:
            print("A storm has hit the ship!")
            if self.is_night:
                self.storm_at_night()
            else:
                storm_at_day()
            return True
        return False

    def storm_at_night(self):
        """Actions to be taken during a nighttime storm."""
        potential_victims = [p for p in self.players if p.character.is_alive and p.character.role != "Pirate"]
        if potential_victims:
            victim = random.choice(potential_victims)
            victim.character.is_alive = False
            print(f"{victim.name} has fallen overboard and drowned!")

    def vote(self):
        """The voting process where players vote to eliminate each other or choose not to vote."""
        print("Voting time!")
        # Create a dictionary to hold votes, including only alive players
        votes = {player.name: 0 for player in self.players if player.character.is_alive}

        for player in self.players:
            if player.character.is_alive:
                while True:  # Stay in the loop until a valid input is received
                    voted_player_name = input(f"{player.name}, who do you vote for? (Type 'pass' to abstain): ").strip()

                    if voted_player_name.lower() == 'pass' or voted_player_name == "":
                        print(f"{player.name} chooses to abstain from voting this turn.")
                        break  # Exit the loop if the player chooses to abstain

                    elif voted_player_name in votes:
                        votes[voted_player_name] += 1
                        print(f"{player.name} has voted for {voted_player_name}.")
                        break  # Exit the loop after a valid vote

                    else:
                        print("Invalid vote or player is already eliminated. "
                              "Please vote again or type 'pass' to abstain.")

        # If there are votes cast, find the player with the most votes and eliminate them
        if any(votes.values()):
            eliminated_player = max(votes, key=votes.get)
            for player in self.players:
                if player.name == eliminated_player and player.character.is_alive:
                    player.character.is_alive = False
                    print(f"{eliminated_player} has been eliminated!")
                    break  # Exit the loop once the eliminated player is found
        else:
            print("No votes cast this turn.")

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
            Lookout("Lookout Lee"),
            Navigator("Navigator Joe"),
            StormBringer("Passenger Davy"),
            Alchemist("Passenger Ann"),
            PirateExecutioner("Passenger Goku"),
            Mercenary("Passenger Max"),
            Headhunter("Passenger John"),
            Prayer("Passenger Jeremiah"),
            OrdinaryPassenger("Passenger Charlie")
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
