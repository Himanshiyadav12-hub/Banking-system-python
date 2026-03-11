import sqlite3
import hashlib

# Global DB connection
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    balance REAL
)
""")
conn.commit()

def get_float_input(prompt):
    """Get valid float input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter valid number!")

def get_username():
    """Get non-empty username."""
    while True:
        username = input("Username: ").strip()
        if username:
            return username
        print("Username cannot be empty!")

def hash_password(password):
    """Hash password for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    print("\n=== REGISTER ===")
    username = get_username()
    
    # Check if user exists
    cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        print("❌ Username already exists!")
        return
    
    password = input("Password: ")
    balance = get_float_input("Initial deposit: ")
    
    hashed_pw = hash_password(password)
    cursor.execute("INSERT INTO users VALUES(?,?,?)", (username, hashed_pw, balance))
    conn.commit()
    print("✅ Account created!")

def login():
    print("\n=== LOGIN ===")
    username = get_username()
    password = input("Password: ")
    hashed_pw = hash_password(password)
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = cursor.fetchone()
    
    if user:
        print("✅ Login successful!")
        banking_menu(username)
    else:
        print("❌ Invalid credentials!")

def deposit(username):
    print("\n--- DEPOSIT ---")
    amount = get_float_input("Amount: ")
    if amount <= 0:
        print("Amount must be positive!")
        return
    
    cursor.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, username))
    conn.commit()
    print(f"✅ Deposited ₹{amount:.2f}")

def withdraw(username):
    print("\n--- WITHDRAW ---")
    amount = get_float_input("Amount: ")
    if amount <= 0:
        print("Amount must be positive!")
        return
    
    # Atomic withdrawal
    cursor.execute("UPDATE users SET balance = balance - ? WHERE username=? AND balance >= ?", 
                   (amount, username, amount))
    if cursor.rowcount == 0:
        print("❌ Insufficient balance!")
    else:
        conn.commit()
        print(f"✅ Withdrew ₹{amount:.2f}")

def check_balance(username):
    print("\n--- BALANCE ---")
    cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
    balance = cursor.fetchone()[0]
    print(f"💰 Current balance: ₹{balance:.2f}")

def banking_menu(username):
    while True:
        print("\n=== BANKING ===")
        print("1. Deposit")
        print("2. Withdraw") 
        print("3. Balance")
        print("4. Logout")
        
        choice = input("Choice (1-4): ").strip()
        
        if choice == "1":
            deposit(username)
        elif choice == "2":
            withdraw(username)
        elif choice == "3":
            check_balance(username)
        elif choice == "4":
            print("👋 Logout!")
            break
        else:
            print("Invalid option!")

def main():
    try:
        while True:
            print("\n=== BANK SYSTEM ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            option = input("Choose (1-3): ").strip()
            
            if option == "1":
                register()
            elif option == "2":
                login()
            elif option == "3":
                print("Thank you! 👋")
                break
            else:
                print("Invalid choice!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
