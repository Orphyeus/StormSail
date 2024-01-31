import random
import Game


class Character:
    def __init__(self, name, role, alignment):
        self.name = name
        self.role = role
        self.alignment = alignment
        self.is_alive = True

    def perform_action(self, target):
        raise NotImplementedError("Subclass must implement abstract method")

    @staticmethod
    def set_random_alignment():
        return "Good" if random.choice([True, False]) else "Evil"


class Captain(Character):
    def __init__(self, name):
        super().__init__(name, "Captain", self.set_random_alignment())

    def perform_action(self, target):
        target.is_imprisoned = True
        print(f"{self.name} has imprisoned {target.name}.")


class Lookout(Character):
    def __init__(self, name):
        super().__init__(name, "Lookout", self.set_random_alignment())

    def perform_action(self, target):
        print(f"{self.name} is observing {target.name}'s actions.")


class Navigator(Character):
    def __init__(self, name):
        super().__init__(name, "Navigator", self.set_random_alignment())

    def perform_action(self, target=None):
        if self.alignment == "Good":
            # Good Navigator reduces the storm probability by 5%
            Game.storm_probability -= 0.05
        elif self.alignment == "Evil":
            # Evil Navigator extends the journey from 4 to 5 days
            Game.storm_probability += 0.05
        # Placeholder for Navigator's special action
        pass


class DiplomaticEnvoy(Character):
    def __init__(self, name):
        super().__init__(name, "Diplomatic Envoy", "Good")

    def perform_action(self, target):
        # Placeholder for Diplomatic Envoy's secret mission
        pass


class EnvoysGuard(Character):
    def __init__(self, name):
        super().__init__(name, "Envoy's Guard", "Good")

    def perform_action(self, target):
        # Placeholder for Envoy's Guard's special action
        pass


class StormBringer(Character):
    def __init__(self, name):
        super().__init__(name, "StormBringer", "Evil")
        self.consecutive_kills = 0  # Track consecutive kills

    def perform_action(self, target):
        """Kill a target and possibly increase storm probability after 3 consecutive kills."""
        if target.is_alive:
            target.is_alive = False
            self.consecutive_kills += 1
            print(f"{self.name} has killed {target.name}.")

            if self.consecutive_kills == 3:
                # Increase storm probability by 20% after 3 consecutive kills
                Game.storm_probability += 0.20
                self.consecutive_kills = 0  # Reset the counter


class Alchemist(Character):
    def __init__(self, name):
        super().__init__(name, "Alchemist", "Evil")

    def perform_action(self, target=None):
        """Extend the journey by manipulating the compass."""
        Game.journey_days += 1
        print(f"{self.name} has extended the journey by one day.")


class Mercenary(Character):
    def __init__(self, name):
        super().__init__(name, "Mercenary", "Neutral")

    def perform_action(self, target):
        # Placeholder for Mercenary's special action
        pass


class Assassin(Character):
    def __init__(self, name):
        super().__init__(name, "Assassin", "Neutral")

    def perform_action(self, target):
        # Placeholder for Assassin's special action
        pass


class OrdinaryPassenger(Character):
    def __init__(self, name, alignment):
        super().__init__(name, "Ordinary Passenger", "Good")

    def perform_action(self, target):
        # Placeholder for Ordinary Passenger's special action
        pass


class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character