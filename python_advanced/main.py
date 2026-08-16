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

    print("\n")
    print("-" * 25) # Visual divider
    print("\nWelcome to the global population game.  To play, select a region of" \
    "the world. Each round, you will be shown to nations.  Select the nation with" \
    "the higher population to advance to the next round!\n")
    print("-" * 25) # Visual divider
    print() # Blank line for formatting
    print("-" * 25) # Visual divider
    print("To begin the game, select a regions:")
    print("-" * 25) # Visual divider
    print("-" * 25) # Visual divider
    print("[1] Africa")
    print("[2] Americas")
    print("[3] Asia")
    print("[4] Europe")
    print("[5] Oceania")
    print("-" * 25) 
    print("\n ...Or choose to play a global round!\n")
    print("-" * 25) 
    print("[6] All nations")
    print("-" * 25) # Visual divider
    print("[7] End game")
    print("-" * 25) # Visual divider
    print() # Blank line for formatting

    return  # Returns nothing


# Validation for menu selection
# Used in * function
def getValidMenuSelection():
    # Loop until valid input is received
    while True:
        # Prompts user for region
        menuSelection = input("Which region would you like to play?: ")  

        # Check if input is valid BEFORE returning error

        # Check if input is a number
        # if menuSelection.isdigit() doesn't work.  .isdigit() is a string method.
        try:
            # Attempt to convert the value to an integer to check if it is a number.
            regionNumber = int(menuSelection)

            # Check if the input is in a valid range between 1 and 5
            if (menuSelection >= 1) and (menuSelection <= 7):
                # Valid input
                return menuSelection  # Return it, breaking the loop
            else:
                print("Sorry.  I didn't understand that.")
                # Display error if validation fails
                print(f"Error: Selection must be a number 1 through 7.")
                menuSelection = input(f"Please select a Menu Item (1-7): ")  # Prompt user again.
        except (ValueError, TypeError):
            # if menuSelection IS NOT a number
            # If execution reaches this point, the input was invalid.  Prompt user again.
            print(f"Error: Please select a menu item with a number 1 through 7.")  # Display error
            menuSelection = input(f"Please select a Menu Item (1-7): ")  # Prompt user again.


# Create a function with game logic
def higher_lower_game():
    # Main Program Execution

    pass
    

# Launch the program
if __name__ == "__main__":
    higher_lower_game()

