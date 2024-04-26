# Name: Ambagahage Shan Emalka Fernando
# Student_number: 20233126 / w2082285

import json

# Global list to store transactions
transactions = []
file_name = "finance.json"


# File handling functions


# Function to load transactions from "finance.json" file.
def load_transactions():
    global transactions 
    try:   
        with open(file_name, "r") as file:# Opens "finance.json' in read mode.
            transactions = json.load(file)
    except FileNotFoundError:# Error handling if "finance.json" does not exist
        print("\n*** File not found!. New file has been created.***")
        save_transactions()
    except json.decoder.JSONDecodeError:# Error handling if data does not exist in "finance.json"
        save_transactions()
    finally:
        if 'file' in locals():
            file.close()


# Function to save transactions to "finance.json" file
def save_transactions():
    with open(file_name, "w") as file:# Opens "finance.json" in write mode.
        json.dump(transactions, file)# Overwrites existing data in "finance.json" with data in global list.
   
   
# Feature implementations


# Function to add a new transaction
def add_transaction():
    global transactions 
    temporary = []
    while True:
        try:
            transactions.append(prompt()) # Add transaction to global list
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
    if not transactions: # Check if there are transactions available
        transaction_availability("view")
    else:
        i = 0# Iterative value used for indexing transactions.
        for entry in transactions:# Loops and takes the elements in the global nested list and cycles through each element within the sub_list.
            i += 1
            # Display transaction details
            print(f"\n>>> Transaction ID: ({i}) <<<\nAmount: {entry[0]},\nCategory: {entry[1]},\nType: {entry[2]},\nDate: {entry[3]}.\n")
        input("<<<Press any key to continue>>>\n")


# Function to update a transaction
def update_transaction():
    global transactions
    if not transactions: # Check if there are transactions available
        transaction_availability("update")
    else:
        view_transactions() # Display transactions for user to choose from
        while True:
            try:
                user_input = int(input("Enter the ID of the transaction you would like to update: "))
                if 0 < user_input <= (len(transactions)): # Check if user input is within the valid range.
                    temporary = []
                    while True:
                        try:         
                            transactions[user_input - 1] = prompt() # Update transaction
                            print("\nTransaction updated successfully!\n")
                            break
                        except ValueError:# Error handling for invalid input.
                            print("\nInvalid Input\n")
                            continue
                        finally:
                            input("<<<Press enter to continue>>>\n")
                            save_transactions() # Save transactions to "finance.json" 
                    return
                else:
                    print("\nTransaction ID of that value does not exist! Please Input a Valid ID.\n")
            except:
                print("\nInvalid Input\n")
                continue
                    
                
        
# Function to delete a transaction
def delete_transaction():
    global transactions
    if not transactions: # Check if there are transactions available
        transaction_availability("delete")
    else:
        view_transactions() # Display transactions for user to choose from
        while True:
            try:
                user_input = int(input("Enter the ID of the transaction you would like to delete: "))
                if 0 < user_input <= (len(transactions)): # Check if user input is within the valid range.
                    transactions.pop(user_input - 1) # Remove transaction
                    print("\nTransaction deleted successfully!\n")
                    return
                else:
                    print("\nTransaction ID of that value does not exist! Please Input a Valid ID.\n")
                    continue
            except ValueError:# Error handling for invalid input.
                print("\nInvalid Input\n")
                continue
            finally:
                input("<<<Press enter to continue.>>>\n")
                save_transactions()
    

# Function to display summary of transactions
def display_summary():
    total_income = 0
    total_expense = 0
    total_income = sum(entry[0] for entry in transactions if entry[2] == "Income")# All values in "Amount" element is added if transaction type is "INCOME".
    total_expense = sum(entry[0] for entry in transactions if entry[2] == "Expense")# All values in "Amount" element is added if transaction type is "EXPENSE".
    balance = total_income - total_expense# Calculate the balance.
    print(f"\nYour total income is {total_income}!\nYour total expense is {total_expense}!\nYour financial balance is {balance}!")
    input("\n<<<Press enter to continue.>>>\n")


# Helper functions
# These are used more than once within functions.


# Function to prompt user for transaction details.
# This function is called within update_transactions() and add_transactions().
def prompt():
    temporary = []
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

# Prompt to enter category of income or expense.
    while True:
        category =(input("Enter category: "))
        if len(category) < 1:
            print("\nInvalid Input!\n")
        else:
            temporary.append(category)
            break
           
# Prompt user if the transaction was an income or an expense.
    while True:
        type = input("Enter type of transaction(Income{I} or Expense{E}): ").upper()
        if type == "I" or type == "INCOME":
            temporary.append("Income")
            break
        elif type == "E" or type == "EXPENSE":
            temporary.append("Expense")
            break
        else:
            print("\nInvalid Input!\n")

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
    
    
# Main Function    


def main_menu():
    load_transactions()  # Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("========================\n")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")
        print("\n")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            print("Exiting program.")
            save_transactions()
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

# if you are paid to do this assignment please delete this line of comment 