import random


class Character:
    def __init__(self, name, role, type, alignment):
        self.name = name
        self.role = role
        self.type = type
        self.alignment = alignment
        self.is_alive = True

    def perform_action(self, target):
        raise NotImplementedError("Subclass must implement abstract method")

    @staticmethod
    def set_random_alignment():
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
        elif self.alignment == "Evil":
            game_instance.storm_probability += 0.05


class DiplomaticEnvoy(Character):
    def __init__(self, name):
        super().__init__(name, "Diplomatic Envoy", "Strategic", "Good")

    def perform_action(self, target):
        # Placeholder for Diplomatic Envoy's secret mission
        pass


class EnvoysGuard(Character):
    def __init__(self, name):
        super().__init__(name, "Envoy's Guard", "Aggressive", "Good")

    def perform_action(self, target):
        # Placeholder for Envoy's Guard's special action
        pass


class StormBringer(Character):
    def __init__(self, name):
        super().__init__(name, "StormBringer", "Strategic", "Evil")
        self.consecutive_kills = 0  # Track consecutive kills

    def perform_action(self, game_instance):
        """Increase storm probability after 3 consecutive kills."""
        if self.consecutive_kills == 3:
            game_instance.storm_probability += 0.2
            self.consecutive_kills = 0  # Reset the counter
        else:
            # Reset consecutive kills if no target or target is already dead
            self.consecutive_kills = 0
            print(f"{self.name} did not attack anyone this turn.")


class Alchemist(Character):
    def __init__(self, name):
        super().__init__(name, "Alchemist", "Strategic", "Evil")

    def perform_action(self, game_instance, target=None):
        """Extend the journey by manipulating the compass."""
        game_instance.journey_days += 1


class Mercenary(Character):
    def __init__(self, name):
        super().__init__(name, "Mercenary", "Aggressive", "Neutral")

    def perform_action(self, target):
        # Placeholder for Mercenary's special action
        pass


class Assassin(Character):
    def __init__(self, name):
        super().__init__(name, "Assassin", "Aggressive", "Neutral")

    def perform_action(self, target):
        # Placeholder for Assassin's special action
        pass


class OrdinaryPassenger(Character):
    def __init__(self, name):
        super().__init__(name, "Ordinary Passenger", "Aggressive", "Evil")

    def perform_action(self, target):
        if target and target.is_alive:
            target.is_alive = False
            self.consecutive_kills += 1
            print(f"{self.name} has killed {target.name}.")
        pass


class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
