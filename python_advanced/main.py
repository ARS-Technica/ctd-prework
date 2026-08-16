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


# Countries.dev Functions -----------------------------------------------------
def getGlobalCountriesAndPopulations() -> None:
    combined_data = []
    
    # Aggregate a list of all countries and populations into one list
    global_regions = ["Africa", "Americas", "Asia", "Europe", "Oceania"]


    

    # Cache in JSON format (ountry_data.jso)
    writeToJson(combined_data)

    retun None


'''
# Returns every country in the given region (exact match, case-insensitive).

import requests
url = "https://countries.dev/region/Asia"
response = requests.request("GET", url)
print(response.text)
'''

def getCountriesByRegion(region: str) -> list[str]:
    url = f"https://countries.dev/region/{region}"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    # Extract the 'name' field from each country object
    return [country["name"] for country in data]


'''
# Retrieve the population of Israel from the country

import requests
url = "https://countries.dev/name/israel"
response = requests.request("GET", url)
print(response.text)
'''

def getPopulations(countries: list[str]) -> list[dict]:
    """
    Retrieve the name and population for a list of countries.

    Queries the countries.dev name endpoint for each country in a list, filtering out everything but 'name' and 'population'.
    """

    results = []
    for country in countries:
        # Request only name and population fields to minimize response payload
        url = f"https://countries.dev/name/{country}?fields=name,population"
        response = requests.get(url)

        # Check if the API request succeeded
        if response.status_code == 200:
            data = response.json()
            # Extract first result if returned as a list, otherwise use object
            item = data[0] if isinstance(data, list) and data else data

            results.append({
                "country": item.get("name", country),
                "population": item.get("population")
            })
        else:
            # Handle failed lookups
            results.append({"country": country, "population": None})

    return results


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

    print(f"Successfully saved {len(country_list)} records to country_data.json") # Debugging purposes

    return None
    

# User Interface Functions ----------------------------------------------------
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


# Create a function with game logic
def higher_lower_game():
    # Main Program Execution

    pass





def main():
    # Flow control
    regionSelection = displayMenu() - 1
    # print(regionSelection) # Debugging purposes

    regionNames = ["Africa", "Americas", "Asia", "Europe", "Oceania"] 

    if regionSelection < 6:
        # print(regionNames[regionSelection])

        region_countries = getCountriesByRegion(regionNames[regionSelection])
        print(region_countries)

        populations = getPopulations(region_countries)
        print(populations)

        # Write the county and population data to a JSON
        writeToJson(populations)

    elif regionSelection == 6:
        # Global
        print("Global")
    else:
        # End Game
        print("Thanks for playing!")
        return


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
