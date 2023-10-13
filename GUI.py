import tkinter as tk
from tkinter import messagebox
import json

# Maximum number of users allowed
MAX_USERS = 10

# Function to load user data from a JSON file
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save user data to a JSON file
def save_users(data):
    with open("users.json", "w") as file:
        json.dump(data, file)

# Function to load user variables from a JSON file for a specific mode
def load_user_variables(username, mode):
    try:
        with open(username + f"_{mode}_variables.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save user variables to a JSON file for a specific mode
def save_user_variables(username, mode, variables):
    # Load existing user variables for the selected mode
    existing_variables = load_user_variables(username, mode)

    # Update existing variables with new values
    existing_variables.update(variables)

    # Save user variables for the selected mode back to the JSON file
    with open(username + f"_{mode}_variables.json", "w") as file:
        json.dump(existing_variables, file)

# Initialize user data
users = load_users()
current_user = None  # Initialize the current user
dcm_connected = False  # Initialize DCM connection status

# Function to handle user login
def login():
    global current_user
    global dcm_connected  # Declare the global variable

    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username] == password:
        current_user = username  # Set the current user
        dcm_connected = True  # Set DCM connection status to True
        show_mode_select(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to handle user registration
def register():
    if len(users) >= MAX_USERS:
        messagebox.showerror("Registration Failed", "Maximum number of users reached.")
        return

    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        if username in users:
            messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Registration Successful", "Account created for " + username)
    else:
        messagebox.showerror("Registration Failed", "Please enter both username and password")

# Function to show the mode selection page
def show_mode_select(username):
    # Destroy the current window
    if 'welcome_window' in globals():
        welcome_window.destroy()

    # Create the mode selection window
    mode_window = tk.Tk()
    mode_window.title("Mode Selection")
    mode_window.geometry("400x250")

    # Create labels and buttons for mode selection
    label = tk.Label(mode_window, text="Select Mode", font=("Arial", 14))
    label.pack(pady=10)

    def select_mode(mode):
        save_user_variables(username, mode, {})  # Initialize user variables for the selected mode
        mode_window.destroy()
        show_welcome_page(username, mode)

    aai_button = tk.Button(mode_window, text="AAI Mode", command=lambda: select_mode("AAI"))
    aai_button.pack()

    vvi_button = tk.Button(mode_window, text="VVI Mode", command=lambda: select_mode("VVI"))
    vvi_button.pack()

    VOO_button = tk.Button(mode_window, text="VOO Mode", command=lambda: select_mode("VOO"))
    VOO_button.pack()

    AOO_button = tk.Button(mode_window, text="AOO Mode", command=lambda: select_mode("AOO"))
    AOO_button.pack()

    # Add an "Egrams" button
    egrams_button = tk.Button(mode_window, text="Egrams", command=lambda: egrams_function())
    egrams_button.pack()
    mode_window.mainloop()

# Function to show the welcome page with user-specific variables
def show_welcome_page(username, mode):
    # Load user variables from JSON file for the selected mode
    user_variables = load_user_variables(username, mode)

    # Create the welcome page window
    global welcome_window
    welcome_window = tk.Tk()
    welcome_window.title("Pacemaker Control Panel")
    welcome_window.geometry("800x400")

    # Create Labels for variables with professional font and colors
    font = ("Arial", 14)
    label_color = "#333"

    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def update_variables():
        updated_variables = {}
        for var_name, entry in variable_entries.items():
            updated_value = entry.get()
            if is_numeric(updated_value):
                updated_variables[var_name] = float(updated_value)
            else:
                messagebox.showerror("Invalid Input", f"Variable {var_name} must be a numeric value.")
                return

        # Save all updated user variables for the selected mode
        save_user_variables(username, mode, updated_variables)

        messagebox.showinfo("Variables Updated", "User variables updated successfully.")

    def create_entry(var_name, var_value):
        label = tk.Label(welcome_window, text=var_name + ":", font=font, fg=label_color)
        label.pack(pady=5, anchor="w")

        entry = tk.Entry(welcome_window, font=font, bg="#fff", width=10)
        entry.insert(0, str(var_value))
        entry.pack(pady=5, anchor="w")

        variable_entries[var_name] = entry

    variable_entries = {}

    if mode == "AAI":
        create_entry("Lower Rate Limit", user_variables.get("Lower Rate Limit", ""))
        create_entry("Upper Rate Limit", user_variables.get("Upper Rate Limit", ""))
        create_entry("Atrial Amplitude", user_variables.get("Atrial Amplitude", ""))
        create_entry("Atrial Pulse Width", user_variables.get("Atrial Pulse Width", ""))
        create_entry("ARP", user_variables.get("ARP", ""))
    elif mode == "VVI":
        create_entry("Lower Rate Limit", user_variables.get("Lower Rate Limit", ""))
        create_entry("Upper Rate Limit", user_variables.get("Upper Rate Limit", ""))
        create_entry("Ventricular Amplitude", user_variables.get("Ventricular Amplitude", ""))
        create_entry("Ventricular Pulse Width", user_variables.get("Ventricular Pulse Width", ""))
        create_entry("VRP", user_variables.get("VRP", ""))
    elif mode == "AOO":
        create_entry("Lower Rate Limit", user_variables.get("Lower Rate Limit", ""))
        create_entry("Upper Rate Limit", user_variables.get("Upper Rate Limit", ""))
        create_entry("Atrial Amplitude", user_variables.get("Atrial Amplitude", ""))
        create_entry("Atrial Pulse Width", user_variables.get("Atrial Pulse Width", ""))
        #create_entry("Ventricular Amplitude", user_variables.get("Ventricular Amplitude", ""))
        #create_entry("Ventricular Pulse Width", user_variables.get("Ventricular Pulse Width", ""))
        #create_entry("VRP", user_variables.get("VRP", ""))
        #create_entry("ARP", user_variables.get("ARP", ""))
    elif mode == "VOO":
        create_entry("Lower Rate Limit", user_variables.get("Lower Rate Limit", ""))
        create_entry("Upper Rate Limit", user_variables.get("Upper Rate Limit", ""))
        create_entry("Ventricular Amplitude", user_variables.get("Ventricular Amplitude", ""))
        create_entry("Ventricular Pulse Width", user_variables.get("Ventricular Pulse Width", ""))

    update_button = tk.Button(welcome_window, text="Update Variables", command=update_variables, font=font, bg="#007acc", fg="white")
    update_button.pack(pady=10)

    back_button = tk.Button(welcome_window, text="Back to Mode Selection", command=lambda: show_mode_select(username), font=font, bg="#ff3333", fg="white")
    back_button.pack(pady=10)

    welcome_window.mainloop()

# Create the main login/registration window
login_window = tk.Tk()
login_window.title("Medical System")
login_window.geometry("400x250")

# Create labels, entry widgets, and buttons
font = ("Arial", 14)
label_color = "white"
entry_bg_color = "#f2f2f2"

username_label = tk.Label(login_window, text="Username:", font=font, fg=label_color, bg="#007acc")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window, font=font, bg=entry_bg_color)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Password:", font=font, fg=label_color, bg="#007acc")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, show="*", font=font, bg=entry_bg_color)
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=login, font=font, bg="#4CAF50", fg=label_color)
login_button.pack(pady=10)

register_button = tk.Button(login_window, text="Register", command=register, font=font, bg="#ff3333", fg=label_color)
register_button.pack(pady=5)

if 1:
   Welcome_label = tk.Label(login_window, text="Welcome to Pacemaker Monitoring System", font=font, fg="blue")
   Welcome_label.pack()
# Display "DCM connected" message if DCM is connected
if 1:
    dcm_label = tk.Label(login_window, text="DCM connected", font=font, fg="green")
    dcm_label.pack()

if 1:
    PACEMAKER_label = tk.Label(login_window, text="PACEMAKER ID:1 is currently being used", font=font, fg="green")
    PACEMAKER_label.pack()

# Function for the "Egrams" button (you can customize this function's behavior)
def egrams_function():
    messagebox.showinfo("Egrams", "This is the Egrams feature. You can customize its behavior here.")
login_window.mainloop()
