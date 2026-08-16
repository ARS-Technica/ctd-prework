# -*- coding: utf-8 -*-
"""
Code the Dream 
Advanced Python Prework

Project: Higher or Lower Game
    
Created on Monday August 15 2026

"A user runs the program and is prompted to select a region name. The program 
fetches all countries from the countries.dev API, filters to those in the 
matching region, and populates a dictionary with each country’s name and 
population.  The program then selects two of the countries at random and asks 
the user which one has the larger population. If the user chooses correctly, 
their score increments upward. If the user chooses incorrently three times, the 
game ends.

Try to beat your previous high score!"
"""

# Import libraries
import json # Cache data for processing
import requests # Make calls to the API


def displayMenu():
    # Display the menu
    # [1] Africa, [2] Americas, [3] Asia, [4] Europe, [5] Oceania, [6] Global, [7] End Game

    print("Global Population Game")
    # Display the menu (List the regions of the world)
    
    print("-" * 25)
    print("\nWelcome to the global population game.  To play, select a region of" \
    "the world. Each round, you will be shown to nations.  Select the nation with" \
    "the higher population to advance to the next round!\n")
    print("-" * 25)

    pass

# Create a function with game logic
def higher_lower_game():
    # Main Program Execution

    pass
    

# Launch the program
if __name__ == "__main__":
    higher_lower_game()

