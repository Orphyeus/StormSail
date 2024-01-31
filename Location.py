class Location:
    """Location class. Holds and updates noise and light levels."""

    def __init__(self, noise, light):
        """Sets the initial noise and light levels."""
        self.noise = noise
        self.light = light

    def update_conditions(self, is_night, is_storm):
        """Updates conditions based on day/night and storm scenarios."""
        if is_storm:
            if is_night:
                self.noise, self.light = (1, 3) if self.__class__.__name__ == "Cellar" else (7, 3)
            else:
                self.noise, self.light = (3, 5) if self.__class__.__name__ == "Cellar" else (8, 5)
        else:
            if is_night:
                self.noise, self.light = (2, 2) if self.__class__.__name__ == "Cellar" else (5, 5)
            else:
                self.noise, self.light = (4, 4) if self.__class__.__name__ == "Cellar" else (7, 8)


class Cellar(Location):
    """Cellar class, derived from Location."""

    def __init__(self):
        """Sets initial noise and light levels for the cellar."""
        super().__init__(noise=4, light=4)


class Deck(Location):
    """Deck class, derived from Location."""

    def __init__(self):
        """Sets initial noise and light levels for the deck."""
        super().__init__(noise=7, light=8)
