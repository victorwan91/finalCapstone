# =======Imports==========
# Import tabulate module from tabulate for tables.
from tabulate import tabulate


# ========The beginning of the class==========
# Create Shoe class.
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        """ Constructor method with instance variables country, code, product, cost and quantity."""
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """Define get_cost method and return the cost of the shoe."""
        return self.cost

    def get_quantity(self):
        """Define get_quantity method and return the quantity of the shoe."""
        return self.quantity

    def __str__(self):
        """Define __str__ method returns a string representation of the Shoe class."""
        return [self.country, self.code, self.product, self.cost,
                self.quantity]


# =============Shoe list===========
# Create an empty list "shoe_list" to store the data read from the file.
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    """
    This function will open the file inventory.txt and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents data to create one object of shoes. 
    You must use the try-except in this function for error handling. Remember to skip the first line using your code.
    """

    # Under try block, read inventory.txt and read the lines of the file.
    try:
        with open("inventory.txt", "r") as file:
            shoes_data = file.readlines()

            # If the file has information in it, each line is split and the information is assigned to the variables 
            # needed to then create an object of Shoe class.
            # Each object is appended to the shoe list.
            if len(shoes_data) > 0:
                for line in shoes_data:
                    if shoes_data.index(line) > 0:
                        country, code, product, cost, quantity = line.strip(). \
                            split(",")
                        line = Shoe(country, code, product, cost, quantity)
                        shoe_list.append(line)

            # Else, print no data found in the file. and exit.
            else:
                print("No data found in the file!")
                exit()

    # Except FileNotFoundError and display error message, then exit.
    except FileNotFoundError:
        print("File not found!")
        exit()


def capture_shoes():
    """
    This function will allow a user to capture data about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    """

    # Request inputs of country, code and product.
    input_country = input("\n\nEnter the country: ")
    input_code = input("Enter the code: ")
    input_product = input("Enter the product name: ")

    while True:
        # Under try block ask for the integer input of cost and quantity.
        try:
            input_cost = int(input("Enter the cost: "))
            input_quantity = int(input("Enter the quantity: "))

            # Print error message if the cost or quantity input is smaller or equal to 0 
            if input_cost <= 0 or input_quantity <= 0:
                print("Please enter values greater than 0!\n")
                continue

            # Else create a Shoe object with the input information inside and append to the shoe list.
            else:
                captured_shoes = Shoe(input_country, input_code, input_product, str(input_cost), str(input_quantity))
                shoe_list.append(captured_shoes)

                # Open inventory.txt to append and write the information into the file and break.
                with open("inventory.txt", "a") as file:
                    file.write("\n")
                    file.write(",".join(captured_shoes.__str__()))
                    print("\nShoes successfully added to the list!")
                    break

        # Except ValueError, print error message.
        except ValueError:
            print("\nPlease ensure you enter whole numbers for cost and quantity.")


def view_all():
    """
    This function will iterate over the shoes list and print the details of the shoes returned from the __str__
    function. Data will be presented in a table format by using Python's tabulate module.
    """

    # Create headings for the table and store in "head"
    # Create an empty list called shoe data list
    head = ["Country", "Code", "Product", "Cost", "Quantity"]
    shoe_data_list = []

    # Use for loop to take each object in the shoe list and call the string method for it,
    # then append this information in shoe data list and print the information in the table format.
    for shoe in shoe_list:
        shoe_data_list.append(shoe.__str__())
    print("\n\nHere are all your stock details: ")
    print(tabulate(shoe_data_list, headers=head, tablefmt="github"))


def re_stock():
    """
    This function will find the shoe object with the
    lowest quantity, which is the shoes that need to be
    re-stocked. Ask the user if they want to add this quantity of
    shoes and then update it. This quantity should be updated
    on the file for this shoe.
    """

    # Create an empty list called quantities list.
    # Use for loop to loop through the shoes in the shoe list and append the quantity to the list.
    quantities_list = []
    for shoe in shoe_list:
        quantity = shoe.get_quantity()
        quantities_list.append(int(quantity))

    # Store the smallest amount from the list to min_quantity and set "shoes_to_be_restocked" as None.
    # Loop through the shoe list, if the shoe quatity matches the min_quantity, store in "shoes_to_be_restocked".  
    min_quantity = min(quantities_list)
    shoes_to_be_restocked = None
    for shoe in shoe_list:
        if shoe.quantity == str(min_quantity):
            shoes_to_be_restocked = shoe.__str__()

    # Print the information in the table format.
    print("\nLowest stock details:")
    head = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate([shoes_to_be_restocked], headers=head, tablefmt="github"))

    while True:
        # Under try block, ask for integer input of restock quantity
        try:
            restock_quantity = int(input("\nEnter the stock to be added: "))

            # If the input is larger than 0, new stock level will be restock_quantity + min_quantity.
            if restock_quantity > 0:
                shoes_to_be_restocked[4] = str(restock_quantity + min_quantity)
                print("\nStock successfully updated!")
                break

            # If the input is lower than 0, print error message.
            else:
                print("Please ensure the stock to be added is greater than 0")

        # Except ValueError, print error message.
        except ValueError:
            print("Invalid entry! Please enter a whole number.")

    # Once the stock is modifiied, open inventory.txt to read lines 
    # and open again to overwrite the new information into the file. 
    with open("inventory.txt", "r+") as file:
        contents = file.readlines()
    with open("inventory.txt", "w") as file:
        for line in contents:
            line_list = line.strip().split(",")
            if line_list[:4] == shoes_to_be_restocked[:4]:
                file.write(",".join(shoes_to_be_restocked))
                file.write("\n")
            else:
                file.write(line)


def search_shoe():
    """
    This function will search for a shoe from the list
    using the shoe code and return this object so that it will be
    printed.
    """

    # Create an empty list call shoe_searched
    # Request input of the shoe code in order to search for the shoes.
    while True:
        shoe_searched = []
        search_code = input("\n Please enter the shoe code to search: ")

        # Use for loop to loop through each shoe object in the list and check if that
        # object's code attribute is the same as the code entered by the user.
        # If the code matches, the shoe will be added to the show searched list.
        for shoe in shoe_list:
            if shoe.code == search_code:
                shoe_searched.append(shoe.__str__())

        # If the shoe searched list is not empty, the information in it will be displayed in a table format and the loop will break.
        if len(shoe_searched) > 0:
            print("\nHere are the shoes you are looking for:")
            head = ["Country", "Code", "Product", "Cost", "Quantity"]
            print(tabulate(shoe_searched, headers=head, tablefmt="github"))
            break

        # Else, print error message.
        else:
            print("Product code not found! Please try again.")


def value_per_item():
    """
    This function will calculate the total valuE for each item with equation: value = cost * quantity and
    print this information on the console for all the shoes.
    """

    # Create an empty list called value list
    # For each object in the shoe list, the value is calculated as the product between the cost and the quantity of that object.
    value_list = []
    for shoe in shoe_list:
        value = int(shoe.cost) * int(shoe.quantity)
        value_list.append([shoe.product, str(value)])

    # Print all the information in a table format.
    print("\n\nHere is the total value of each item in stock: ")
    print(tabulate(value_list, headers=["Product", "Total Value"], tablefmt="github"))


def highest_qty():
    """
    This function will find the show object with the highest quantity in stock
    and display the product that's on sale.
    """

    # Create an empty list called quantities list
    # For each item in the shoe list, get the quantity and append it to the quantities list.
    # The highest quantity will be the max number in the list.
    quantities_list = []
    for shoe in shoe_list:
        quantity = shoe.get_quantity()
        quantities_list.append(int(quantity))
    highest_quantity = max(quantities_list)

    # Set shoes_on_sale as None
    # Looping through all the objects in the shoe list again, the object that is found to 
    # have the highest quantity calculated above, will be the shoe that is displayed as being on sale.
    shoes_on_sale = None
    for shoe in shoe_list:
        if shoe.quantity == str(highest_quantity):
            shoes_on_sale = shoe.__str__()

    # Print the shoes on sale in a table form.
    print("\n\nShoes ON SALE:")
    head = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate([shoes_on_sale], headers=head, tablefmt="github"))


# ==========Main Menu=============
# Clear the shoe list to ensure that data is correct on each iteration
# Read the shoes data in the file.
# And present user the user menu.
while True:
    shoe_list.clear()
    read_shoes_data()
    user_menu = input("""
              ===User Menu===
    Please choose one of the following options:
    1. View all your stock details
    2. Search an item by the product code
    3. View the total value of each item in your stock
    4. View items low on stock and re-stock 
    5. View items that are on sale (highest stock products)
    6. Capture data about an item and add this to your stock list
    0. Exit the system 
    Enter a number here => """)

    # If the input is 1, implement view_all() function.
    if user_menu == "1":
        view_all()

    # If the input is 2, implement search_shoe() function.
    elif user_menu == "2":
        search_shoe()

    # If the input is 3, implement value_per_item() function.
    elif user_menu == "3":
        value_per_item()

    # If the input is 4, implement re_stock() function.
    elif user_menu == "4":
        re_stock()

    # If the input is 5, implement highest_qty() function.
    elif user_menu == "5":
        highest_qty()

    # If the input is 6, implement capture_shoes() function.
    elif user_menu == "6":
        capture_shoes()

    # If the input is 0, print goodbye message and exit.
    elif user_menu == "0":
        print("\nGoodbye!")
        exit()

    # Else, print error message.
    else:
        print("Invalid input! Please try again!")
