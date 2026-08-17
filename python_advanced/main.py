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
def evaluate_guess(guess, first_choice, second_choice):
    pass

def prompt_user(first_choice, second_choice):
    pass

# Create a function with game logic
def higher_lower_game():
    pass 

# User Interface Functions ----------------------------------------------------

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

def endGame() -> None:
    # Would be replaced with a graphic in future versions
    print() # Blank line for formatting    
    print("Thanks for playing!")
    print() # Blank line for formatting   
    
    return None    

def main():
    # Flow control
    region_selection = displayMenu()
    # print(region_selection) # Debugging purposes

    region_names = ["Africa", "Americas", "Asia", "Europe", "Oceania"] 

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

    '''
    countries = getCountriesByRegion("Europe")
    print(countries)
    # ['Åland Islands', 'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'France', 'Germany', 'Gibraltar', 'Greece', 'Guernsey', 'Vatican City', 'Hungary', 'Iceland', 'Ireland', 'Isle of Man', 'Italy', 'Jersey', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'North Macedonia', 'Malta', 'Moldova (Republic of)', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Republic of Kosovo', 'Romania', 'Russian Federation', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Svalbard and Jan Mayen', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom of Great Britain and Northern Ireland']


    region_countries = getCountriesByRegion("Europe")
    populations = get_populations(region_countries)

    print(populations)
    # [{'country': 'Åland Islands', 'population': 28875}, {'country': 'Albania', 'population': 2837743}, {'country': 'Andorra', 'population': 77265}, {'country': 'Austria', 'population': 8917205}, {'country': 'Belarus', 'population': 9398861}, {'country': 'Belgium', 'population': 11555997}, {'country': 'Bosnia and Herzegovina', 'population': 3280815}, {'country': 'Bulgaria', 'population': 6927288}, {'country': 'Croatia', 'population': 4047200}, {'country': 'Cyprus', 'population': 1207361}, {'country': 'Czech Republic', 'population': 10698896}, {'country': 'Denmark', 'population': 5831404}, {'country': 'Estonia', 'population': 1331057}, {'country': 'Faroe Islands', 'population': 48865}, {'country': 'Finland', 'population': 5530719}, {'country': 'France', 'population': 67391582}, {'country': 'Germany', 'population': 83240525}, {'country': 'Gibraltar', 'population': 33691}, {'country': 'Greece', 'population': 10715549}, {'country': 'Guernsey', 'population': 62999}, {'country': 'Vatican City', 'population': 451}, {'country': 'Hungary', 'population': 9749763}, {'country': 'Iceland', 'population': 366425}, {'country': 'Ireland', 'population': 4994724}, {'country': 'Isle of Man', 'population': 85032}, {'country': 'Italy', 'population': 59554023}, {'country': 'Jersey', 'population': 100800}, {'country': 'Latvia', 'population': 1901548}, {'country': 'Liechtenstein', 'population': 38137}, {'country': 'Lithuania', 'population': 2794700}, {'country': 'Luxembourg', 'population': 632275}, {'country': 'North Macedonia', 'population': 2083380}, {'country': 'Malta', 'population': 525285}, {'country': 'Moldova (Republic of)', 'population': 2617820}, {'country': 'Monaco', 'population': 39244}, {'country': 'Montenegro', 'population': 621718}, {'country': 'Netherlands', 'population': 17441139}, {'country': 'Norway', 'population': 5379475}, {'country': 'Poland', 'population': 37950802}, {'country': 'Portugal', 'population': 10305564}, {'country': 'Republic of Kosovo', 'population': 1775378}, {'country': 'Romania', 'population': 19286123}, {'country': 'Russian Federation', 'population': 144104080}, {'country': 'San Marino', 'population': 33938}, {'country': 'Serbia', 'population': 6908224}, {'country': 'Slovakia', 'population': 5458827}, {'country': 'Slovenia', 'population': 2100126}, {'country': 'Spain', 'population': 47351567}, {'country': 'Svalbard and Jan Mayen', 'population': 2562}, {'country': 'Sweden', 'population': 10353442}, {'country': 'Switzerland', 'population': 8636896}, {'country': 'Ukraine', 'population': 44134693}, {'country': 'United Kingdom of Great Britain and Northern Ireland', 'population': 67215293}]
    '''
