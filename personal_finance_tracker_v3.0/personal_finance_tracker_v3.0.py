# Name: Ambagahage Shan Emalka Fernando
# Student_number: 20233126 / w2082285

import view_transactions_gui
import json
from datetime import datetime# Used specifically for the "read_bulk_transactions_from_file()" function.
#Note: Why is this not used in the prompt function? 
# Because in the prompt function the day and month are individually validated and if wrong reprompts the user right away. If the datetime function is used the user has to input from the beginning everytime user gets it wrong.

# Global dictionary to store transactions
transactions = {}
file_name_1 = "finance.json"
file_name_2 = "finance.txt"


# File handling functions


# Function to load transactions from "finance.json" file.
def load_transactions():
    global transactions 
    try:   
        with open(file_name_1, "r") as file:# Opens "finance.json' in read mode.
            transactions = json.load(file)
    except FileNotFoundError:# Error handling if "finance.json" does not exist
        print("\n*** File not found!. New file has been created.***")
        save_transactions()
    except json.decoder.JSONDecodeError:# Error handling if data does not exist in "finance.json"
        save_transactions()
    finally:
        read_bulk_transactions_from_file()



# Function to save transactions to "finance.json" file
def save_transactions():
    with open(file_name_1, "w") as file:# Opens "finance.json" in write mode.
        json.dump(transactions, file, indent = 4)# Overwrites existing data in "finance.json" with data in global dictionary.


# *** coursework part B additions ***
# Open and read the file, then parse each line to add to the transactions dictionary
def read_bulk_transactions_from_file(read_message = False):
    
    def message():
        print(f"1. Open \"finance.txt\" and add transactiona to it.\n     Each transaction should be one line each.\n     Format: Category, Amount, Type(income/expense), date(YYYY-MM-DD)\n\n2. Save \"finance.txt\"\n")
        input("<<<Press enter after saving to load transactions>>>")
        
    def main():
        try:# Error handling if file does not exist.
            with open(file_name_2, "r") as file:# Opens "finance.txt" file in read mode.
                lines = file.readlines()# Reads file line by line and returns a list.
                i = 0
                for line in lines:
                    i += 1
                    if not line.strip():# Check if there are empty lines without data, if so go to the next line
                        continue
                    else:
                        try:
                            
                            elements = line.split(",")
                            if len(elements) != 4:# Check if the user entered format is wrong in "finance.txt".
                                print(f"\nInvalid format in line {i}. Transaction not added!. Each line should contain [Category, Amount, Type(income/expense), date]\n")
                                continue
                            
                            if elements[1].strip().isdigit() and float(elements[1].strip()) > 0:# Check if amount is a digit and greater than zero.
                                pass
                            else:
                                print(f"Amount({elements[1].strip()}) on line {i} is not valid. Transaction not added!")
                                continue
                            
                            transaction_type = check_type(elements[2])# Check if it is an income or an expense
                            if transaction_type == "Income" or transaction_type == "Expense":
                                pass
                            elif transaction_type == "Invalid Input!":
                                print(f"Type({elements[2].strip()}) on line {i} is not valid. Transaction not added!")
                                continue

                            try:
                                date_string = elements[3].strip()# Strip elements wide space characters.
                                date_string_formatted = "-".join([unit.zfill(2) for unit in date_string.split("-")])# Add zeros to single digit numbers.
                                datetime.strptime(date_string_formatted, "%Y-%m-%d")# Validate the format using date time function.
                            except ValueError:
                                print(f"Date({elements[3].strip()}) on line {i} is not valid. Transaction not added!")
                                continue
                            
                        except:
                            continue
                        
                    temp = {}
                    
                    category, amount, t_type, date = line.split(",")# Items in list are split by the ",".
                    category = category.capitalize()
                    if transaction_type == "Income":
                        float_amount = float(amount.strip())
                    elif transaction_type == "Expense":
                        float_amount = -abs(float(amount.strip()))
                    
                    temp["amount"], temp["date"] = float_amount, date_string_formatted# Each element are trip of wide space characters and assigned to a dictionary.
                    
                    append_transaction_dictionary(temp, category.strip())       
                    
        except:
            print("\n*** File not found!. New file has been created.***")
            with open(file_name_2,"a") as file:
                pass
            
        finally:
            save_transactions()
            clear_text_file()
            
    if read_message:
        message()
    main()



def clear_text_file():
    with open(file_name_2, "w") as file:
        file.truncate(0)           
# *** coursework part B additions ***
   
   
# Feature implementations


# Function to add a new transaction
def add_transaction():
    global transactions 
    temporary = {}# Temporary Dictionary to append to list within transactions dictionary values
    while True:
        try:
            
            # *** coursework part B additions ***
            temp_list = prompt()# Returns user input as a list from prompt() function
            temporary["amount"], temporary["date"] = temp_list[1], temp_list[3] # Assign relevent element of list to its relevent key in the temporary dictionary
            append_transaction_dictionary(temporary, temp_list[0])
            # *** coursework part B additions ***    
            
            print("\nTransaction added successfully!\n")
            break
        except ValueError:# Error handling for invalid input without program crashing.
            print("\nInvalid Input\n")
            continue
        finally:
            save_transactions() # Save transactions to "finance.json"
            input("<<<Press enter to continue>>>\n")  
 
                
        
# Function to view all transactions
def view_transactions():
    if not transactions: # Check if there are transactions available.
        transaction_availability("view")
    else:
        
        # *** coursework part B additions *** 
        for key, value in transactions.items():# Loops and takes the key value pairs in the global dictionary.
            i = 0# Iterative value used for indexing transactions.
            message = "Category:"
            length = len(message)
            print(f"{message} {key}\n")
            for entry in value:# Cycles within the list which is the value of the key.
                i += 1
                # Display transaction details
                print(f"{" " * length}>>> Transaction ID: ({i}) <<<\n{(" " * length)+ (" " * 4)}Amount: {abs(entry["amount"])},\n{(" " * length)+ (" " * 4)}Date: {entry["date"]}.\n")
        # *** coursework part B additions *** 
        
        input("<<<Press enter to continue>>>\n")



# Function to update a transaction
def update_transaction():
    global transactions
    if not transactions: # Check if there are transactions available
        transaction_availability("update")
    else:
        view_transactions() # Display transactions for user to choose from
                
        # *** coursework part B additions ***  
        user_input = category_id_verification("update")
        user_input_category = user_input["category"]
        user_input_id = user_input["id"]
        temporary = {}
        while True:
            try:       
                temp_list = prompt(False, transactions[user_input_category][user_input_id - 1]["amount"])# Returns user input as a list from prompt() function
                temporary["amount"], temporary["date"] = temp_list[0], temp_list[2]# Assign relevent element of list to its relevent key in the temporary dictionary
                transactions[user_input_category][user_input_id - 1] = temporary 
        # *** coursework part B additions ***
                    
                print("\nTransaction updated successfully!\n")
                break
            except ValueError:# Error handling for invalid input.
                print("\nInvalid Input\n")
                continue
            finally:
                input("<<<Press enter to continue>>>\n")
                save_transactions() # Save transactions to "finance.json" 
            
                
        
# Function to delete a transaction
def delete_transaction():
    global transactions
    delete_keys = []
    if not transactions: # Check if there are transactions available
        transaction_availability("delete")
    else:
        view_transactions() # Display transactions for user to choose from
            
        user_input = category_id_verification("delete")
        user_input_category, user_input_id = user_input["category"], user_input["id"]
        
        del transactions[user_input_category][user_input_id - 1]# Deletes the given element within the list which is the value of the global dictionary
        
        # For loop to check for empty key-value pairs within the global dictionary and append keys to dictionary
        [delete_keys.append(key) for key, values in transactions.items() if not values]
        
        # For loop to delete said empty key-value pairs
        for item in delete_keys:
            del transactions[item]
        
        print("\nTransaction deleted successfully!\n")
        input("<<<Press enter to continue.>>>\n")
        save_transactions()



# Function to display summary of transactions 
def display_summary():
    total_income = 0
    total_expense = 0
    for value in transactions.values():
        for item in value:
            if item["amount"] > 0:
                total_income += item["amount"]# All values in "Amount" key is added if transaction type is "INCOME".
            elif item["amount"] < 0:
                total_expense += item["amount"]# All values in "Amount" key is added if transaction type is "EXPENSE".
    balance = total_income + total_expense# Calculate the balance.
  
    print(f"\nYour total income is {total_income}/=\nYour total expense is {abs(total_expense)}/=\nYour net income is {balance}/=")
    input("\n<<<Press enter to continue.>>>\n")


# Helper functions
# These are used more than once within functions.


# Function to prompt user for transaction details.
# This function is called within update_transactions() and add_transactions().
def prompt(flag = True, amount_income_or_expense = 0):# These parameters are only used in update. flag is to stop asking category and amount_income_or_expense is to check if the already existing transaction before update was an income or an expense.
    temporary = []
    # Prompt to enter category of income or expense.
    if flag:
        while True:
            category = (input("\nEnter category: "))
            category = category.capitalize()
            if len(category) < 1:
                print("\nInvalid Input!\n")
            else:
                temporary.append(category)
                break
            
    while True:
        try:# Error handling for invalid inputs.
            amount = float(input("Enter amount: "))
            if amount <= 0:# Infinite loop until user enters a positive value.
                print("\nEnter amount higher than zero.\n")
                continue
            else:
               temporary.append(amount)# If value is valid it is appended to the temporary list.
               break
        except:
            print("\nInvalid Input!\n")
           
# Prompt user if the transaction was an income or an expense.
    if flag:
        while True:
            t_type = input("Enter type of transaction(Income{I} or Expense{E}): ").upper()
            if t_type == "I" or t_type == "INCOME":
                temporary.append("Income")
                break
            elif t_type == "E" or t_type == "EXPENSE":
                temporary.append("Expense")
                break
            else:
                print("\nInvalid Input!\n")
    else:
        if amount_income_or_expense < 0:# Check if the existing value before updating is an expense.
            temporary.append("Expense")
        elif amount_income_or_expense > 0:
            temporary.append("Income")# Check if the existing value before updating is an income.
        

# Prompt user for the year, month and day.           
        # Tuple with all the months(months[0] = "has 31 days", months[1] = "has 30 days", months[2] = "february - has 29 days")
    months = ((1, 3, 5, 7, 8, 10, 12), (4, 6, 9, 11), (None, 2))
    message = "Enter >>> "
    print(message,end = '')
    space = len(message)
    while True:
        try:
            year = (int(input("Year: ")))# Enter year.
            if 0 < year and len(str(year)) == 4:
                break
            else:
                print("\nInvalid Year! Please re-enter.\n")
                print(f"{space * " "}", end = "")
                continue
        except:
            print("\nEnter a number!\n")
            print(f"{space * " "}", end = "")
            
    while True:
        try:
            month = (int(input(f"{space * " "}Month: ")))# Prompt user for month.
            if 0 < month <= 12:# Check if the month is between 1 and 12
                break
            else:
                print("\nInvalid Month! Please re-enter.\n")
                continue
        except:
            print("\nEnter a number!\n")
            
    while True:
        try: 
            day = (int(input(f"{space * " "}Day: ")))# Prompt user for day.
            if month in months[0]:# Check if the month is in months[0].
                if 0 < day <= 31:# check if user input is within valid range.
                    break
                else:
                    print("\nInvalid day! Please re-enter.\n")
                    continue
            elif month in months[1]:# Check if the month is in months[1].
                if 0 < day <= 30:# check if user input is within valid range.
                    break
                else:
                    print("\nInvalid day! Please re-enter.\n")
                    continue
            elif month in months[2]:# Check if the month is in months[2].
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):# Check if the year is a leap year.
                    if 0 < day <= 29:# check if user input is within valid range.
                        break
                    else:
                        print("\nInvalid day! Please re-enter a day between 1 and 29.\n")
                        continue
                else:# If the year is not a laeap year.
                    if 0 < day <= 28:# check if user input is within valid range.
                        break
                    else:
                        print("\nInvalid day! Please re-enter a day between 1 and 28.\n")
                        continue
        except:
            print("\nEnter a number!\n")
    f_date = f"{year}-{month:02d}-{day:02d}"# This adds the date to a list in the suitable format. It also fills in "0" if the month or day is a single digit.
    temporary.append(f_date)
    if flag:
        if temporary[2] == "Expense":# If type is an expense the amount is changed to a negative value
            temporary[1] = -abs(temporary[1])
    else:
        if temporary[1] == "Expense":# If type is an expense the amount is changed to a negative value
            temporary[0] = -abs(temporary[0])
    return temporary



# Function to prompt user if there are no transactions available
def transaction_availability(message):
    while True:
            user_input = input(f"\nNo transactions available to {message}. Would you like to add a transaction(Y/N): ").upper()
            print("\n")
            if user_input == "Y":
                add_transaction()# Redirect user to add_transactions().
                return
            elif user_input == "N":
                return
            else:
                print("Please enter Y or N.")
                continue



# *** coursework part B additions ***
# Function to check if user inputs are valid in context of category and ID in said category. Works with update and delete
def category_id_verification(message):
    temp = {}
    flag = True
    while flag:
        user_input_category = input(f"Enter the category of the transaction you would like to {message}: ")# Get user to input the category that needs to be changed.
        user_input_category = user_input_category.replace(" ", "").lower()
        for key in transactions.keys():
            if user_input_category in key.replace(" ", "").lower():# Check if category key exists within global dictionary
                temp["category"] = key# If category is available then add it to a temperory dictionary.
                flag = False
        if flag:
            print(f"\n{user_input_category} category does not exits. Enter valid category!\n")
            continue

    while True:
        try:
            user_input_id = int(input(f"\nEnter the ID of the transaction you would like to {message}: "))# Get user to input ID of the relevent element within the category key that needs to be changed.
            if 0 < user_input_id <= (len(transactions[key])):# Check if ID is within range of the acceptable IDs.
                temp["id"] = user_input_id# If the ID is within valid range add the ID to the temporary dictionary.
                break
            else:
                print("\nTransaction ID of that value does not exist! Please Input a Valid ID.")
            continue
        except:# Error handling for invalid inputs.
            print("\nInvalid Input")
            continue
    return temp# Return temperory dictionary.
# *** coursework part B additions ***


# *** coursework part B additions ***
# Function that appends a dictionary from the prompt as the value of the global dictionary.
def append_transaction_dictionary(dictionary, category):
    while True:
        if category in transactions.keys():# Check if key already exists in global dictionary
            transactions[category].append(dictionary)# If it exists, append the temporary dictonary to the relevent key of the global dictionary
            break 
        else:
            transactions[category] = []# If it dosen't exist, add a new key with its value as an empty list 
            continue
# *** coursework part B additions ***


# *** coursework part B additions ***
# Function used to check the type of transaction.
def check_type(t_type):
    upper_type = t_type.upper().strip()
    if upper_type == "I" or upper_type == "INCOME":
           return "Income"
    elif upper_type == "E" or upper_type == "EXPENSE":
            return "Expense"
    else:
        return "Invalid Input!"
# *** coursework part B additions ***

    
# Main Function    


def main_menu():
    load_transactions()# Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("========================\n")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Transactions in GUI")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Display Summary")
        print("7. Load bulk transactions")
        print("8. Exit")
        choice = input("Enter your choice: ")
        print("\n")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        # *** coursework part C additions ***
        elif choice == '3':
            view_transactions_gui.main()
        # *** coursework part C additions ***
        elif choice == '4':
            update_transaction()
        elif choice == '5':
            delete_transaction()
        elif choice == '6':
            display_summary()
        elif choice == '7':
            read_bulk_transactions_from_file(True)
        elif choice == '8':
            print("Exiting program.")
            save_transactions()
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

# if you are paid to do this assignment please delete this line of comment 