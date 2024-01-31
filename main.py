from Game import Game


def main():
    """Main function to start the game."""
    # Initialize the game instance
    storm_voyage = Game()

    # Start the game loop
    storm_voyage.start_game()

    # After the game loop ends, you can add any post-game wrap-up or display the game results
    print("Beware, calm seas never made skilled sailors. Until next time!")


if __name__ == "__main__":
    main()
