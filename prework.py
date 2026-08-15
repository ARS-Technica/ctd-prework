# This script totals up the cost of admission for attending the theater.and
# First, it asks the user for their name.  Then it asks for the age of each 
# member of the party's age.  
# Finally, the script prints out the total cost of admission.

name = ""
number_of_tickets = 0
total_cost = 0.00

adult_age = 18
child_age = 4
toddler_age = 0

name = input("What is your name? ")

print("Hello!", name, "Welcome to the Kalamazoo Theater!")
number_of_tickets = int(input("How many tickets would you like to purchase today? "))

print("-" * 25)

if number_of_tickets == 0:
    print("Thank-you for visiting the Kalamazoo Theater. Please come back again!")
else:
    while number_of_tickets > 0:
        age=int(input("What is the age of the person purchasing the ticket? "))

        if age >= adult_age:
            total_cost += 10.00
        elif age >= child_age:
            total_cost += 5.00
        else:
            total_cost += 0.00

        number_of_tickets -= 1

print(f"Thank you, {name}! Your total admission today will be: ${total_cost:.2f}")
print("Thank-you for visiting the Kalamazoo Theater. Please come back again!")

