import random


class Character:
    def __init__(self, name, role, action_type, alignment):
        self.name = name
        self.role = role
        self.action_type = action_type
        self.alignment = alignment
        self.is_alive = True
        self.is_protected = False

    def perform_action(self, target):
        """Perform the character's action."""
        raise NotImplementedError("Subclass must implement abstract method")

    @staticmethod
    def set_random_alignment():
        """Set a random alignment for the character."""
        return "Good" if random.choice([True, False]) else "Evil"


class Captain(Character):
    def __init__(self, name):
        super().__init__(name, "Captain", "Aggressive", self.set_random_alignment())

    def perform_action(self, target):
        """Imprison a target if specified."""
        if target:
            target.is_imprisoned = True
            print(f"{self.name} has imprisoned {target.name}.")
        else:
            print(f"{self.name} chooses not to imprison anyone this turn.")


class Lookout(Character):
    def __init__(self, name):
        super().__init__(name, "Lookout", "Aggressive", self.set_random_alignment())

    def perform_action(self, target):
        """Lookout observes the target's actions."""
        if target:
            print(f"{self.name} is observing {target.name}'s actions.")
            print(f"{self.name} is detect {target.name} is {target.type} type.")
        else:
            print(f"{self.name} is keeping watch but chooses not to observe anyone specifically.")


class Navigator(Character):
    def __init__(self, name):
        super().__init__(name, "Navigator", "Strategic", self.set_random_alignment())

    def perform_action(self, game_instance):
        """Modify the storm probability based on the navigator's alignment."""
        if self.alignment == "Good":
            game_instance.storm_probability -= 0.05
            print("Navigator decrease the storms probability: ", game_instance.storm_probability)
        elif self.alignment == "Evil":
            game_instance.storm_probability += 0.05
            print("Navigator increase the storms probability: ", game_instance.storm_probability)


"""EVIL SIDE"""


class StormBringer(Character):
    def __init__(self, name):
        super().__init__(name, "StormBringer", "Strategic", "Evil")
        self.consecutive_curse = 0  # Track consecutive curse

    def perform_action(self, game_instance):
        game_instance.storm_probability += 0.03

        """Increase storm probability after 3 consecutive kills."""
        if self.consecutive_curse == 3:
            game_instance.storm_probability += 0.1
            print("Storm Bringer increase the storms probability: ", game_instance.storm_probability)
            self.consecutive_curse = 0  # Reset the counter


class PirateExecutioner(Character):
    def __init__(self, name):
        super().__init__(name, "Pirate Executioner", "Aggressive", "Evil")

    def perform_action(self, target):
        """Attempt to assassinate the chosen player unless they are protected."""
        if not target.is_protected:
            target.is_alive = False
            print(f"{self.name} has successfully assassinated {target.name}.")
        else:
            print(f"{self.name}'s assassination attempt was thwarted. {target.name} is protected.")


class Alchemist(Character):
    def __init__(self, name):
        super().__init__(name, "Alchemist", "Strategic", "Evil")
        self.consecutive_days = 0  # Track consecutive days of compass manipulation

    def perform_action(self, game_instance):
        """Extend the journey by one day if the compass has been manipulated for three consecutive days."""
        self.consecutive_days += 1  # Increment the count of consecutive days
        if self.consecutive_days >= 3:  # Check if it's been three consecutive days
            game_instance.journey_days += 1  # Extend the journey by one day
            print(f"{self.name} has extended the journey by one day.")
            self.consecutive_days = 0  # Reset the consecutive days counter
        else:
            print(f"{self.name} continues to manipulate the compass.")


"""GOOD SIDE"""


class Prayer(Character):
    def __init__(self, name):
        super().__init__(name, "Prayer", "Strategic", "Good")

    def perform_action(self, game_instance):
        game_instance.storm_probability -= 0.03


class Headhunter(Character):
    def __init__(self, name):
        super().__init__(name, "Headhunter", "Aggressive", "Good")

    def perform_action(self, target):
        """If a pirate enters the room, instantly execute them."""
        pass


class Mercenary(Character):
    def __init__(self, name):
        super().__init__(name, "Mercenary", "Aggressive", "Neutral")

    def perform_action(self, target):
        target.character.is_protected = True


class OrdinaryPassenger(Character):
    def __init__(self, name):
        super().__init__(name, "Ordinary Passenger", "Aggressive", "Good")

    def perform_action(self, target):
        pass


class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
