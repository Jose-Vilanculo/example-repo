# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        '''
        returns the cost of each shoe item
        '''
        return self.cost

    def get_quantity(self):
        '''
        returns the quantity of each shoe item
        '''
        return self.quantity

    def __str__(self):
        '''
        returns a string representation of a class
        '''
        return f'''\n{self.product}
    Country: {self.country}
    Code: {self.code}
    Product: {self.product}
    Cost: R{self.cost}
    Quantity: {self.quantity}'''


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data(shoe_list):
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list.
    '''
    # opens the file inventory.txt to read from it.
    try:
        with open("inventory.txt", "r", encoding="utf-8")as file:
            # skips the first line.
            next(file)
            for line in file:
                # removes whitespaces and commas from all lines.
                data = line.strip().split(",")
                # creates shoe objects and appends them to shoe_list.
                shoe_list.append(Shoe(data[0], data[1], data[2], int(data[3]), int(data[4])))
    except FileNotFoundError:
        print("This file can not be found")


def capture_shoes(shoe_list):
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list. Then updates
    the file inventory.txt with the data for the new object.
    '''
    # collects all the data required to create a shoe object
    # and error handles all user input.
    print("\nEnter the details of the New Shoe you want to add to the system...")
    shoe_data_1 = input("Country of Origin: ")
    while True:
        try:
            shoe_data_2 = int(input("Product Code: SKU"))
            break
        except ValueError:
            print("Invalid input. Please use integers only")
            continue
    shoe_data_3 = input("Product Name: ")
    while True:
        try:
            shoe_data_4 = int(input("Product Price: R"))
            break
        except ValueError:
            print("Invalid price. Please use integers only.")
            continue
    while True:
        try:
            shoe_data_5 = int(input("Product Quantity: "))
            break
        except ValueError:
            print("invalid quantity. Please use integers only.")
            continue

    # appends the new shoe object to the shoe_list and updates it.
    shoe_list = shoe_list.append(Shoe(shoe_data_1, "SKU" + str(shoe_data_2), shoe_data_3, shoe_data_4, shoe_data_5))

    # opens inventory.txt and writes the data for the new object to it.
    data = (shoe_data_1, "SKU" + str(shoe_data_2), shoe_data_3, str(shoe_data_4), str(shoe_data_5))
    try:
        with open("inventory.txt", "a", encoding="utf-8") as file:
            file.write("\n" + ",".join(data))
            print("Your database has been successfully updated.")
    except FileNotFoundError:
        print("The file does not exist")

    # feedback once the shoe has been successfully captured.
    print(f"\n{shoe_data_5} pairs of {shoe_data_3} has been added to the database.")


def view_all(shoe_list):
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function.
    '''
    for i in shoe_list:
        print(i)


def re_stock(shoe_list):
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    # sorts list by quantity, in order to use indexing
    # to find the shoe with the least stock.
    shoe_list = sorted(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"\n{shoe_list[0].product} is running low on stock. You have {shoe_list[0].get_quantity()} pairs left")
    # prompt user tp decide if the want to add to this stock.
    prompt = input('''\nWould you like to restock on this shoe? Enter only "Yes" or "No": ''').lower()
    while True:
        if prompt == "yes":
            try:
                # asks user how many pairs of shoes they want to restock
                re_stock_quantity = int(input("How many pairs do you want to restock? "))
                # updates the total amount of shoes by adding x pairs of shoes
                # to the stock that was low.
                shoe_list[0].quantity = shoe_list[0].quantity + re_stock_quantity
                print(f'''\n{re_stock_quantity} pairs of {shoe_list[0].product} have been added.
You now have {shoe_list[0].quantity} pairs in stock''')
                break
            except ValueError:
                print("\nInvalid input. Enter only integers.")
                continue
        elif prompt == "no":
            # exits function.
            print("No stock was added.")
            break
        else:
            print("Invalid Input.")
            break

    # get first line.
    try:
        with open("inventory.txt", "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
    except FileNotFoundError:
        print("This file does not exist")

    # rewrites the inventory.txt file with the updated stock count.
    with open("inventory.txt", "w", encoding="utf-8") as file:
        file.write(first_line)
        for shoe in shoe_list:
            file.write("\n" + f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")


def search_shoe(shoe_list):
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    # sorts shoe list by shoe code in order to use binary search.
    shoe_list = sorted(shoe_list, key=lambda shoe: shoe.code)
    # finds target code that the user wants to search
    target = input("Enter the code of the shoe you want to search: ").upper()

    # binary search for target.
    begin_index = 0
    end_index = len(shoe_list) - 1
    while begin_index <= end_index:
        midpoint = (end_index + begin_index)//2
        mid_code = shoe_list[midpoint].code

        if mid_code == target:
            return shoe_list[midpoint]
        elif target < mid_code:
            end_index = midpoint - 1

        else:
            begin_index = midpoint + 1

    return f"\nUnfortunately code {target} does not exist in the database. "


def value_per_item(shoe_list):
    '''
    This function will calculate the total value for each item.
    Then print this information on the console for all the shoes.
    '''
    print("Value of items in stock:\n")
    for item in shoe_list:
        # calculation for the value of each item.
        value = item.get_cost() * item.get_quantity()
        print(f"{item.product}: R{value}")


def highest_qty(shoe_list):
    '''
    This code will determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # sorts list by quantity, in order to use indexing
    # to find the shoe with the most stock.
    shoe_list = sorted(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"{shoe_list[-1].product} is now on Sale!!!")


# ==========Main Menu=============
'''
A Menu that executes each function above.
'''
# creates list of objects.
read_shoes_data(shoe_list)

# creates loop for the user to navigate the menu.
while True:
    # error handling to ensure the user enters an integer.
    try:
        user_choice = int(input('''\nWould you like to:

 1. Add a new shoe to the system
 2. View all shoes in stock
 3. Restock the shoe with the least stock remaining
 4. Search for a shoe
 5. See the value of stock for each shoe
 6. Put the shoe with the most stock on sale
 0. Exit program

(Enter only the number of the option you wish to carry out): '''))
    except ValueError:
        print("\nInvalid input. Please enter a number (0-6).")
        continue
    # checks if the user option is valid
    if user_choice >= 0 and user_choice <= 6:
        if user_choice == 1:
            capture_shoes(shoe_list)
        elif user_choice == 2:
            view_all(shoe_list)
        elif user_choice == 3:
            re_stock(shoe_list)
        elif user_choice == 4:
            print(search_shoe(shoe_list))
        elif user_choice == 5:
            value_per_item(shoe_list)
        elif user_choice == 6:
            highest_qty(shoe_list)
        else:
            print("\nYou've exited this program. Bye :)\n")
            exit(0)
    else:
        print("\nInvalid input. Please enter a number (0-6).")
        continue
