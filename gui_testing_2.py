import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date

class TransactionEditor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Transaction Editor")
        
        # Create labels and entries for input fields
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        
        tk.Label(self, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        
        tk.Label(self, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        
        # Buttons for actions
        tk.Button(self, text="Save", command=self.save_transaction).grid(row=3, column=0, columnspan=2, pady=10)
        
    def save_transaction(self):
        # Get input values
        name = self.name_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get().strip()
        
        # Validate and convert amount
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        
        # Validate and convert date
        try:
            transaction_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        # Create or update transaction with validated data
        transaction = {
            "name": name,
            "amount": amount,
            "date": transaction_date.isoformat(),  # Convert date to ISO format string
        }
        
        # Optionally, you can save the transaction to a database or perform other actions here
        
        # Print the transaction (for demonstration purposes)
        print("Transaction Saved:")
        print(transaction)
        
        # Close the window after saving
        self.destroy()

# Example usage
if __name__ == "__main__":
    tmp = date(2024, 7, 13)
    
    root = tk.Tk()
    root.title("Transaction Manager")
    
    def open_transaction_editor():
        editor = TransactionEditor(root)
    
    tk.Button(root, text="Create Transaction", command=open_transaction_editor).pack(pady=20)
    
    root.mainloop()
