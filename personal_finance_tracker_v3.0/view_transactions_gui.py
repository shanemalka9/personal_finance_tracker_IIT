import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox



file_name = "finance.json"

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.config(bg="#F4F3B1")# Change background color of root window.
        self.root.minsize(780, 310)# Specify a minimum size the window can be resized to.
        self.create_widgets()
        self.transactions = self.load_transactions(file_name)# Loads transactions from "finance.json" to transactions variable.
        # Changed file name from "transactions.json" to "finance.json" to keep consistent with coursework part B.
        self.reverse = False
        self.placeholder_text = "search"
        # Styles. Used because the use of ttk.
        self.style = ttk.Style()
        self.style.configure("Search.TFrame", background="#F4F3B1")
        self.style.configure("Title.TLabel", background="#F4F3B1", foreground="#1C1C1C", font=("Deja Vu Vera", 20, "bold"))
        self.style.configure("Treeview", background="white", foreground="#1C1C1C", font=("Consolas", 10))


    def create_widgets(self):
        
        # Frame for table and scrollbar
        self.frame_table = ttk.Frame(self.root, style="Treeview")
        self.frame_table.pack(side=tk.BOTTOM, padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)# ? "fill=tk.BOTH" :fills x and y axis to match the space(can be restricted to individual axises.| expand=True" : sets expandability to True.
        
        # Frame for the search frame, title and home button.
        self.frame_search_home = ttk.Frame(self.root, style= "Search.TFrame")
        self.frame_search_home.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Frame for search bar/ button and clear button. 
        self.frame_search = ttk.Frame(self.frame_search_home, style="Search.TFrame")
        self.frame_search.pack(side="right")
        
        
        # Treeview for displaying transactions
        
        self.tree = ttk.Treeview(self.frame_table, columns=("category", "amount", "date"), show="headings")
            # Syntax to format columns.
        self.tree.column("#0", width=0)
        self.tree.column("category", width=250, minwidth=75)
        self.tree.column("amount", width=250, minwidth=75)
        self.tree.column("date", width=250, minwidth=75)
            # Syntax to create headings.
        self.tree.heading("category", text="Category", command= lambda:self.sort_by_column("category", self.reverse))
        self.tree.heading("amount", text="Amount", command= lambda:self.sort_by_column("amount",self.reverse))
        self.tree.heading("date", text="Date", command= lambda:self.sort_by_column("date", self.reverse))
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.frame_table, orient=tk.VERTICAL,command=self.tree.yview)# Adjusts tree view movenent according to the scrollbar movement.
        self.tree.configure(yscrollcommand=self.scrollbar.set)# Specified the method to call when the scrollbar is moved.
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Search bar and button
            # Search Bar.
        self.search_entry = tk.Entry(self.frame_search, justify="right",fg="#1C1C1C", bg="#EEEEEE", font=("Consolas", 10), relief="groove", borderwidth=3)# Create Search bar to enter.
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)
            # Add "search" text within entry.
        self.search_entry.insert(tk.END, "search")
        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)# Binds event "<FocusIn>" to search_entry so that 'on_entry_focus_in ' function is executed when the entry is the focus(when entry is clicked).
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)# Binds event "<FocusOut>" to search_entry so that 'on_entry_focus_out ' function is executed when the entry  loses focus(when entry is not clicked).| check clear() function
        
            # Search Button.
        self.search_button = tk.Button(self.frame_search, text="Search",fg="#1C1C1C", bg="#FFFFFF", font=("Arial", 10), relief="groove", width=8, command=self.search_transactions)
        self.search_button.grid(row=0, column=1, padx=5)
            # Clear Search Button.
        self.clear_search_button = tk.Button(self.frame_search, text = "Clear",fg="#1C1C1C", bg="#FFFFFF", font=("Arial", 10), relief="groove", width=8, command=self.clear)
        self.clear_search_button.grid(row=0, column=2, padx=5)
        
        # Extra button(Home) and Title.
        self.home_button = tk.Button(self.frame_search_home, text="Home", fg="#1C1C1C", bg="#FFFFFF", font=("Arial", 10), relief="groove", width=8, command=self.home)
        self.home_button.pack(side="left", padx=5)
        
        self.title = ttk.Label(self.frame_search_home, text = "Personal Finance Tracker", style="Title.TLabel")
        self.title.pack(padx=5)
        
    # Function to load transactions from "finance.json" file.
    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:# Opens "finance.json' in read mode.
                transactions =  json.load(file)# loads transactions to transactions variable.
                f_transactions = []
                for category, transaction in transactions.items():# Iterates through key-value pair in "transactions" dictionary.
                    for entry in transaction:# Iterates through the values in transactions dictionary which are lists.
                        f_transactions.append({"category" : category.strip(), "amount": str(abs(entry["amount"])), "date": entry["date"].strip()})
                return f_transactions
        except FileNotFoundError:
            messagebox.showwarning("File not found!", f"File {file_name} not found.")# Error message if file not found.
            return {}
        except json.decoder.JSONDecodeError:
            messagebox.showwarning("JSON DEcode Error", "Error decoding json file.")# Error message if file cannot be decoded.
            return {}

    def display_transactions(self, transactions):
        # Remove existing entries
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Add transactions to the treeview
        for entry in transactions:
            self.tree.insert('', tk.END, text="", values=(entry["category"], entry["amount"], entry["date"]))# Insert transactions to treeview.
        return

    # Function used to search transactions.
    def search_transactions(self):
        filter_transaction = []
        user_input_original = self.search_entry.get().lower().replace(" ","")# Get user input from entry.
        user_input = user_input_original# This statement is used to keep a cpoy of user the origial user input so changes can be reverted.
        
        for entry in self.transactions:# Loop throught the list with all transactions which has dictionary elements.
            if user_input in entry["category"].lower().replace(" ","") or user_input in entry["date"] or user_input in entry["date"].replace("-",""):# if the user_input equal to the value then append the whole entry to the filter_transacions list.
                filter_transaction.append(entry)
            else:
                # Try statement to check if the user input is an amount
                try:
                    user_input = str(float(user_input))
                    if user_input == str(entry["amount"]):
                        filter_transaction.append(entry)
                except:
                    pass
                finally:
                    user_input = user_input_original
                
        if not filter_transaction:# If searched term does not exist an error message is shown.
                messagebox.showwarning("Transaction does not exist!", "The term you searched does not exist.")# Error message if file not found.
                return
                        
        self.display_transactions(filter_transaction)# Displays the searched items.
        return

    # Function used to sort transactions
    def sort_by_column(self, col, reverse):
        
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]# Get items from column in treeview and add to a tuple with an id.
        if col == 'amount':# If column is amount  then sort by converting the item of the treeview in the tuple to float and sorting it as needed.
            items = sorted(items, key=lambda x: float(x[0]), reverse=reverse) # type: ignore 
        else:
            items.sort(reverse=reverse)# Sort items in the needed order.

        for index, (val, item) in enumerate(items):# This iterates over the items list and provides both the index and the value of each item in the list.
            self.tree.move(item, '', index)# This line moves the item within the self.tree widget.
        self.tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))
        
    
    # Extra function for "Home" and "Clear" Button.
    # When the home button is pressed the search bar clears and the user gets to see all the transactions again.
    def home(self):
        self.display_transactions(self.transactions)
        self.clear()
        self.search_entry.insert(tk.END, "search")
        self.root.focus_set()# Used to remove focus fom entry.

    def clear(self):
        self.search_entry.delete(0, "end")
        self.search_entry.focus_set()
        
    
    # *** functions used to add "search" text to entry ***
    def on_entry_focus_out(self, event):
        if self.search_entry.get() == '':
            self.search_entry.insert(0, self.placeholder_text)  # Insert placeholder text if entry is empty
            self.search_entry.config(fg='grey')  
    
    def on_entry_focus_in(self, event):
        if self.search_entry.get() == self.placeholder_text:# Check if entry text equal to placeholder text.
            self.search_entry.delete(0, tk.END)  # Clear the placeholder text when focused
            self.search_entry.config(fg='black')# Change text color back to black.
    # *** functions used to add "search" text to entry ***
    
            
def main():
    root = tk.Tk()# Creates the main window.
    app = FinanceTrackerGUI(root)# Creates an object called app which passes the main window "root" to the class "FinanceTrackerGUI".
    app.display_transactions(app.transactions)# Calls a method named "display_transactions" that takes "app.transactions" from class __init__ method as an argument
    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.mainloop()

if __name__ == "__main__":
    main()