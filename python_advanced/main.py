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


import json # For cashing country data from countries.dev API
import os # Import os library to clear screen between rounds
import random # Import random module for choosing Google Searches
import requests # Read calls to the countries.dev API
import time # To pause between response to user input and new screen

# Import dataset for comparisons


# Countries.dev Functions -----------------------------------------------------

def getRegionCountryData(region: str) -> list[dict]:
    """
    Fetch all country names and populations for a given region.
    """
    url = f"https://countries.dev/region/{region}?fields=name,population"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            countries = response.json()
            return [
                {"country": item.get("name"), "population": item.get("population")}
                for item in countries
                if item.get("population") is not None
            ]
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
    
    return []


def getGlobalCountriesAndPopulations() -> list[dict]:
    """
    Combines country data across all major regions and saves to JSON.
    """
    combined_data = []
    global_regions = ["Africa", "Americas", "Asia", "Europe", "Oceania"]
    
    for region in global_regions:
        combined_data.extend(getRegionCountryData(region))

    # Cache in JSON format (ountry_data.jso)
    writeToJson(combined_data)

    return combined_data


def load_country_data(filename: str = "country_data.json") -> list[dict]:
    """
    Loads country records from country_data.json handling the 'data =' prefix.

    Caching worked better than holding the dictionary in working memory, 
    but now I need the game logic to access the json data.
    """
    if not os.path.exists(filename):
        print(f"Error: Could not find '{filename}'.")
        return []

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content.startswith("data ="):
            content = content[len("data ="):].strip()
        dataset = json.loads(content)

    return [item for item in dataset if item.get("population") is not None]


def writeToJson(country_list: list[dict]) -> None:
    """
    Writes a list of country dictionaries to a JSON-formatted file.

    Formatted with the 'data = [...]' prefix.
    """
    # Serialize the list of dictionaries to a JSON-formatted string    
    formatted_json = json.dumps(country_list, indent=4, ensure_ascii=False)

    # Write to file
    with open("country_data.json", "w", encoding="utf-8") as f:
        f.write(f"data = {formatted_json}\n")

    # print(f"Successfully saved {len(country_list)} records to country_data.json") # Debugging purposes    

    return None  


# High or Low Game Functions --------------------------------------------------

# Create a function to evaluate player's guesses
def evaluate_guess(guess: str, first_choice: dict, second_choice: dict) -> bool:
    """
    Compares populations and evaluates the player's guess.
    """
    pop_a = first_choice["population"]
    pop_b = second_choice["population"]

    a_is_larger = pop_a >= pop_b

    if (guess == "a" and a_is_larger) or (guess == "b" and not a_is_larger):
        print(f"\nCorrect!")
        print(f"{first_choice['country']} has a population of {pop_a:,}.")
        print(f"{second_choice['country']} has a population of {pop_b:,}.")

        return True
    else:
        print(f"\nWrong!")
        print(f"{first_choice['country']} has a population of {pop_a:,}.")
        print(f"{second_choice['country']} has a population of {pop_b:,}.")

        return False


def prompt_user(first_choice: dict, second_choice: dict) -> bool:
    """
    Prompts user to select A or B.
    """
    guess = input("\nWhich country has a higher population? Select A or B: ").strip().lower()

    if guess in ["a", "b"]:
        # If the user enters a valid answer
        return evaluate_guess(guess, first_choice, second_choice)
    else:
        # Prompt the user to entry only "A" or "B"
        print("Invalid input. Please enter 'A' or 'B'.")
        prompt_user()


# Create a function with game logic
def higher_lower_game(dataset: list[dict]):
    """
    Runs the game loop using the loaded dataset.
    """
    if len(dataset) < 2:
        print("\nError: Not enough country data available to play this region.")
        time.sleep(2)
        endGame()

    # Track the progression of the game
    score = 0  # Display the number of correct answers
    strikes = 0 # Track the number of wrong answers
    max_strikes = 3 # Game ends after three wrong answers

    # Pick two distinct initial countries
    first, second = random.sample(dataset, 2)

    # Start with a clean screen to declutter interface
    clear_screen()

    # Round Opening Screen
    print("=" * 45)
    print() # Blank line for formatting
    print("     POPULATION HIGHER OR LOWER GAME")
    print() # Blank line for formatting
    print("=" * 45)
    print() # Blank line for formatting
    print(f"You have {max_strikes} strikes. Guess which nation is larger!\n")

    while strikes < max_strikes:
        # Round Logic

        # Pause between rounds
        time.sleep(2.5)
        clear_screen()

    
    # Game Over Screen
    print("=" * 45)
    print() # Blank line for formatting
    print(f"  GAME OVER!  ")
    print() # Blank line for formatting
    print("=" * 45)
    print() # Blank line for formatting
    print(f"  Final Score: {score}")
    print() # Blank line for formatting
    print("=" * 45)
    time.sleep(2)
    


# User Interface Functions ----------------------------------------------------

def clear_screen():
    """
    Cross-platform terminal clearing code.
    """
    os.system("cls" if os.name == "nt" else "clear")


def displayMenu() -> int:
    """
    Displays the main menu (Lists the regions of the world)
    and returns a validated user selection.
    """
    # [1] Africa, [2] Americas, [3] Asia, [4] Europe, [5] Oceania, [6] Global, [7] End Game

    # Display the menu (List the regions of the world)
    print("=" * 45) # Visual divider
    print() # Blank line for formatting
    print("        GLOBAL POPULATION GAME")
    print() # Blank line for formatting
    print("=" * 45) # Visual divider
    print() # Blank line for formatting
    print("Welcome to the global population game.")
    print("Select a region to fetch its countries and play!\n")
    print() # Blank line for formatting
    print("[1] Africa")
    print("[2] Americas")
    print("[3] Asia")
    print("[4] Europe")
    print("[5] Oceania")
    print("[6] All nations (Global)")
    print("-" * 45) # Visual divider    
    print("[7] End game")
    print("-" * 45) # Visual divider

    # return  # Returns nothing

    return getValidMenuSelection()


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
            if (regionNumber >= 1) and (regionNumber <= 7):
                # Valid input
                # print(regionNumber) # Debugging purposes
                return regionNumber  # Return it, breaking the loop
            else:
                print("Sorry.  I didn't understand that.")
                # Display error if validation fails
                print("Error: Selection must be a number 1 through 7.")
                menuSelection = input("Please select a Menu Item (1-7): ")  # Prompt user again.
        except (ValueError, TypeError):
            # If menuSelection IS NOT a number
            # If execution reaches this point, the input was invalid.  Prompt user again.
            print(f"Error: Please select a menu item with a number 1 through 7.")  # Display error
            menuSelection = input(f"Please select a Menu Item (1-7): ")  # Prompt user again.


# Flow Control Functions ------------------------------------------------------

def end_game(final_score: int | None = None) -> None:
    """
    Displays the game-over or exit screen.
    
    If final_score is provided, displays performance stats.
    Otherwise, displays a standard farewell message.

    # Would be replaced with a graphic in future versions
    """
    clear_screen()
    print() # Blank line for formatting    
    print("Thanks for playing!")
    print() # Blank line for formatting   

    return None    
   

def main():
    """
    Controls overall program flow: presents the region selection menu,
    triggers API data fetching and saving, and launches the game loop.
    """
    region_names = ["Africa", "Americas", "Asia", "Europe", "Oceania"] 

    while True:
        clear_screen()
        region_selection = displayMenu()
        
        if 1 <= region_selection <= 5:
            # Fetch names AND populations in 1 HTTP request
            selected_region = region_names[region_selection - 1]
            populations = getRegionCountryData(selected_region)
            # print(populations) # Debugging purposes
    
            # Write the county and population data to a JSON        
            writeToJson(populations)
    
        elif region_selection == 6:
            # Global: combines all 5 regions
            global_data = getGlobalCountriesAndPopulations()
            print(global_data)
    
        else:
            endGame()


# Launch the program
if __name__ == "__main__":
    main()

