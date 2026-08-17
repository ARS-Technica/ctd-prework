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

import json      # Used to create and JSON file for caching API data
import os        # Import os library to clear screen between rounds (clearing screen, file checks) 
import random    # Import random module for choosing countries for each round
import time      # To pause between response to user input and new screen
import requests  # To call the countries.dev API


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

    Caching worked better than holding the dictionary in working memory, but now I need the game logic to access the json data.
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


def prompt_user(first_choice: dict, second_choice: dict) -> bool | str:
    """
    Prompts the player to choose A, B, or Q to quit.
    """
    while True:
        guess = input("\nWhich country has a higher population? Select A or B (Q to quit): ").strip().lower()
        
        if guess == "q":
            return "q"
        elif guess in ["a", "b"]:
            return evaluate_guess(guess, first_choice, second_choice)
        else:
            print("Invalid input. Please enter 'A', 'B', or 'Q'.")


def higher_lower_game(dataset: list[dict]):
    """
    Runs the game loop using the loaded dataset.
    """
    if len(dataset) < 2:
        print("\nError: Not enough country data available to play this region.")
        time.sleep(2)
        return

    score = 0       # Display the number of correct answers
    strikes = 0     # Track the number of wrong answers
    max_strikes = 3 # Game ends after three wrong answers

    # Pick two distinct initial countries
    first, second = random.sample(dataset, 2)

    clear_screen()

    # Round Opening Screen
    print("=" * 45)
    print() # Blank line for formatting
    print("     GLOBAL POPULATION GAME")
    print() # Blank line for formatting
    print("=" * 45)
    print() # Blank line for formatting
    print(f"You have {max_strikes} strikes. Guess which nation is larger!\n")

    while strikes < max_strikes:
        # Round Logic        
        print(f"\n[Score: {score} | Strikes: {strikes}/{max_strikes}]")
        print() # Blank line for formatting
        print() # Blank line for formatting
        print(f"Compare A: {first['country']}")
        print("    vs")
        print(f"Against B: {second['country']}")
        print() # Blank line for formatting
        print() # Blank line for formatting

        result = prompt_user(first, second)

        # Handle player choosing to quit
        if result == "q":
            print() # Blank line for formatting
            print("\nExiting current game round...")
            time.sleep(2)
            break

        if result is True:
            score += 1
            print(f"\nNice job! Current Score: {score}")
            print() # Blank line for formatting
        else:
            strikes += 1
            print(f"\nStrike {strikes} of {max_strikes}!")

        # Advance slot A to slot B and pick a new slot B
        first = second
        remaining_pool = [c for c in dataset if c != first]
        if not remaining_pool:
            print("\nYou've played through all available countries in this region!")
            break

        second = random.choice(remaining_pool)
    
        # Pause between rounds
        time.sleep(3)
        clear_screen()

    # Call the Game Over screen with the final score
    end_game(final_score=score)


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
    print() # Blank line for formatting
    print("[7] End game")
    print() # Blank line for formatting
    print("=" * 45) # Visual divider

    return getValidMenuSelection()


def getValidMenuSelection() -> int:
    """Prompts and validates menu input without redundant prompts."""
    while True:
        menu_selection = input("Which region would you like to play? (1-7): ").strip()
        try:
            region_number = int(menu_selection)
            if 1 <= region_number <= 7:
                return region_number
            else:
                print("Error: Selection must be a number between 1 and 7.\n")
        except ValueError:
            print("Error: Invalid input. Please enter a valid number (1-7).\n")


# Flow Control Functions ------------------------------------------------------

def end_game(final_score: int | None = None) -> None:
    """
    Displays the game-over or exit screen.
    
    If final_score is provided, displays performance stats.
    Otherwise, displays a standard farewell message.

    # Would be replaced with a graphic in future versions
    """
    clear_screen()

    print("=" * 45)
    print() # Blank line for formatting 
    print("                 GAME OVER")
    print() # Blank line for formatting 
    print("=" * 45)
    print() # Blank line for formatting 
    
    if final_score is not None:
        print(f"\nYour final score was: {final_score}")
        if final_score >= 10:
            print("That's incredible!  Great job!")
        elif final_score >= 5:
            print("Well done. You really know your geography!")
        else:
            print("Better luck next time! Keep practicing!")
    
    print("\nThanks for playing the Global Population Game!")
    print() # Blank line for formatting 
    print("=" * 45)
    time.sleep(2)


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
            # Options 1 through 5: Specific regional play
            selected_region = region_names[region_selection - 1]
            print(f"\nFetching data for {selected_region} and saving to country_data.json...")
            populations = getRegionCountryData(selected_region)

            # Handle API failures
            if not populations:
                print(f"\nConnection Error: Unable to retrieve data for {selected_region}.")
                print("Please check your internet connection and try again.")
                time.sleep(2)
                continue # Skips file writing & game launch, returning to displayMenu()

            writeToJson(populations)

        elif region_selection == 6:
            # Option 6: Global play (all 5 continents combined)
            print("\nFetching data for all regions and saving to country_data.json...")

            # Handle API failures            
            global_data = getGlobalCountriesAndPopulations()
            if not global_data:
                print(f"\nConnection Error: Unable to retrieve global data.")
                print("Please check your internet connection and try again.")

                time.sleep(2)
                continue # Skips file writing & game launch, returning to displayMenu()

        else:
            # Option 7: Exit game
            end_game()
            break

        # Read back the newly created JSON file from disk
        current_game_data = load_country_data("country_data.json")

        # Launch the Higher/Lower game using the loaded data
        higher_lower_game(current_game_data)

        # Check if the player wants to return to the region menu or quit
        play_again = input("\nReturn to main menu to choose another region? (Y/N): ").strip().lower()
        if play_again != "y":
            print("\nThanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main() # Launch application

