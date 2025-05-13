import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pickle
import os
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pickle
import os
from datetime import datetime

class User:
    """Represents a user of the ticket system."""
    def __init__(self, user_id, name, email, password, balance=0.0):
        """Initializes a new User object.
        Args:
            user_id (int): Unique identifier for the user.
            name (str): User's full name.
            email (str): User's email address (used for login).
            password (str): User's password for authentication.
            balance (float, optional): User's account balance (currently not fully implemented). Defaults to 0.0.
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.balance = balance
        self.bookings = [] # List to store the user's bookings

    def get_user_id(self):
        """Returns the user's ID."""
        return self.user_id

    def get_name(self):
        """Returns the user's name."""
        return self.name

    def get_email(self):
        """Returns the user's email address."""
        return self.email

    def get_password(self):
        """Returns the user's password."""
        return self.password

    def get_balance(self):
        """Returns the user's balance."""
        return self.balance

    def update_profile(self, name=None, email=None, password=None):
        """Updates the user's profile information.
        Args:
            name (str, optional): New name. Defaults to None.
            email (str, optional): New email. Defaults to None.
            password (str, optional): New password. Defaults to None.
        """
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = password

    def add_booking(self, booking):
        """Adds a booking to the user's booking history.
        Args:
            booking (Booking): The booking object to add.
        """
        self.bookings.append(booking)

    def view_history(self):
        """Returns the user's booking history."""
        return self.bookings

class AccountManager:
    """Manages user accounts, including creation, retrieval, updating, and deletion."""
    def __init__(self, filename="users.pkl"):
        """Initializes the AccountManager.
        Args:
            filename (str, optional): The filename to store user data using pickle. Defaults to "users.pkl".
        """
        self.users = {} # Dictionary to store User objects, with user_id as keys
        self.next_user_id = 1 # Counter for generating unique user IDs
        self.filename = filename
        self.load_data() # Load user data from the pickle file on initialization

    def _generate_user_id(self):
        """Generates a unique user ID."""
        user_id = self.next_user_id
        self.next_user_id += 1
        return user_id

    def create_account(self, name, email, password, details=None):
        """Creates a new user account.
        Args:
            name (str): User's name.
            email (str): User's email.
            password (str): User's password.
            details (dict, optional): Additional user details (currently not used). Defaults to None.
        Raises:
            ValueError: If the provided email address already exists.
        Returns:
            User: The newly created User object.
        """
        if email in [user.email for user in self.users.values()]:
            raise ValueError(f"Email '{email}' already exists.")
        user_id = self._generate_user_id()
        new_user = User(user_id, name, email, password)
        self.users[user_id] = new_user
        self.save_data() # Save updated user data to the pickle file
        return new_user

    def get_user(self, user_id):
        """Retrieves a User object based on their ID.
        Args:
            user_id (int): The ID of the user to retrieve.
        Returns:
            User: The User object if found, otherwise None.
        """
        return self.users.get(user_id)

    def update_user(self, user_id, name=None, email=None, password=None):
        """Updates an existing user's information.
        Args:
            user_id (int): The ID of the user to update.
            name (str, optional): New name. Defaults to None.
            email (str, optional): New email. Defaults to None.
            password (str, optional): New password. Defaults to None.
        Returns:
            bool: True if the user was updated successfully, False otherwise.
        """
        user = self.get_user(user_id)
        if user:
            user.update_profile(name, email, password)
            self.save_data() # Save updated user data
            return True
        return False

    def delete_user(self, user_id):
        """Deletes a user account.
        Args:
            user_id (int): The ID of the user to delete.
        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        if user_id in self.users:
            del self.users[user_id]
            self.save_data() # Save updated user data
            return True
        return False

    def display_user_details(self, user_id):
        """Retrieves and returns the details of a user.
        Args:
            user_id (int): The ID of the user.
        Returns:
            dict: A dictionary containing the user's details (user_id, name, email, balance), or None if the user is not found.
        """
        user = self.get_user(user_id)
        if user:
            return {"user_id": user.user_id, "name": user.name, "email": user.email, "balance": user.balance}
        return None

    def save_data(self):
        """Saves the user account data to the pickle file."""
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump({'users': self.users, 'next_user_id': self.next_user_id}, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save user data: {e}")

    def load_data(self):
        """Loads the user account data from the pickle file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    data = pickle.load(f)
                    self.users = data.get('users', {})
                    self.next_user_id = data.get('next_user_id', 1)
                    # Ensure next_user_id is greater than any existing user ID
                    if self.users:
                        max_id = max(self.users.keys())
                        if self.next_user_id <= max_id:
                            self.next_user_id = max_id + 1
            except Exception as e:
                messagebox.showerror("Error", f"Could not load user data: {e}")

class Ticket:
    """Represents a ticket for a race event."""
    def __init__(self, ticket_id, name, price, validity=None, features=None, discount_available=True):
        """Initializes a new Ticket object.
        Args:
            ticket_id (int): Unique identifier for the ticket type.
            name (str): Name of the ticket type (e.g., "General Admission", "VIP").
            price (float): Price of the ticket.
            validity (str, optional): Duration or validity period of the ticket. Defaults to None.
            features (str, optional): Special features or access granted by the ticket. Defaults to None.
            discount_available (bool, optional): Indicates if a discount can be applied to this ticket type. Defaults to True.
        """
        self.ticket_id = ticket_id
        self.name = name
        self.price = price
        self.validity = validity
        self.features = features
        self.discount_available = discount_available

    def get_ticket_id(self):
        """Returns the ticket ID."""
        return self.ticket_id

    def get_name(self):
        """Returns the name of the ticket."""
        return self.name

    def get_price(self):
        """Returns the price of the ticket."""
        return self.price

    def get_validity(self):
        """Returns the validity of the ticket."""
        return self.validity

    def get_features(self):
        """Returns the features of the ticket."""
        return self.features

    def is_discount_available(self):
        """Returns True if a discount is available for this ticket type, False otherwise."""
        return self.discount_available

    def set_discount_availability(self, available):
        """Sets the discount availability for this ticket type.
        Args:
            available (bool): True if discount should be available, False otherwise.
        """
        self.discount_available = available

class RaceEvent:
    """Represents a race event with its details and available tickets."""
    def __init__(self, event_id, name, date, location, capacity):
        """Initializes a new RaceEvent object.
        Args:
            event_id (int): Unique identifier for the race event.
            name (str): Name of the race event (e.g., "Grand National").
            date (str): Date of the race event.
            location (str): Location of the race event (e.g., "Aintree Racecourse").
            capacity (int): Maximum capacity of attendees for the event.
        """
        self.event_id = event_id
        self.name = name
        self.date = date
        self.location = location
        self.capacity = capacity
        self.tickets = {} # Dictionary to hold Ticket objects available for this event, with ticket name as keys

    def get_event_id(self):
        """Returns the event ID."""
        return self.event_id

    def get_name(self):
        """Returns the name of the event."""
        return self.name

    def get_date(self):
        """Returns the date of the event."""
        return self.date

    def get_location(self):
        """Returns the location of the event."""
        return self.location

    def get_capacity(self):
        """Returns the capacity of the event."""
        return self.capacity

    def add_ticket(self, ticket):
        """Adds a ticket type to the event's available tickets.
        Args:
            ticket (Ticket): The Ticket object to add.
        Raises:
            ValueError: If a ticket type with the same name already exists for this event.
        """
        if ticket.get_name() not in self.tickets:
            self.tickets[ticket.get_name()] = ticket
        else:
            raise ValueError(f"Ticket type '{ticket.get_name()}' already exists for this event.")

    def get_ticket(self, ticket_name):
        """Retrieves a Ticket object for this event based on its name.
        Args:
            ticket_name (str): The name of the ticket type.
        Returns:
            Ticket: The Ticket object if found, otherwise None.
        """
        return self.tickets.get(ticket_name)

    def get_available_tickets(self):
        """Returns a list of all available Ticket objects for this event."""
        return list(self.tickets.values())

    def get_availability(self):
        """Returns the current availability (remaining capacity) for the event.
        In a real system, this might track actual seats sold. For simplicity, returning capacity.
        Returns:
            int: The total capacity of the event.
        """
        return self.capacity

class Booking:
    """Represents a booking made by a user for a race event."""
    def __init__(self, booking_id, user_id, event_id, booking_date=None, status="Pending"):
        """Initializes a new Booking object.
        Args:
            booking_id (int): Unique identifier for the booking.
            user_id (int): ID of the user who made the booking.
            event_id (int): ID of the event booked.
            booking_date (str, optional): Date and time of the booking. Defaults to current timestamp.
            status (str, optional): Current status of the booking (e.g., "Pending", "Confirmed", "Cancelled"). Defaults to "Pending".
        """
        self.booking_id = booking_id
        self.user_id = user_id
        self.event_id = event_id
        self.booking_date = booking_date if booking_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = status
        self.tickets = [] # List to store the Ticket objects included in this booking
        self.total_amount = 0.0 # Total amount for this booking

    def get_booking_id(self):
        """Returns the booking ID."""
        return self.booking_id

    def get_user_id(self):
        """Returns the ID of the user who made the booking."""
        return self.user_id

    def get_event_id(self):
        """Returns the ID of the event booked."""
        return self.event_id

    def get_booking_date(self):
        """Returns the date and time of the booking."""
        return self.booking_date

    def get_status(self):
        """Returns the current status of the booking."""
        return self.status

    def add_ticket(self, ticket):
        """Adds a ticket to this booking and updates the total amount.
        Args:
            ticket (Ticket): The Ticket object to add.
        """
        self.tickets.append(ticket)
        self.calculate_total()

    def get_tickets(self):
        """Returns a list of Ticket objects in this booking."""
        return self.tickets

    def calculate_total(self):
        """Calculates and returns the total amount for this booking."""
        self.total_amount = sum(ticket.get_price() for ticket in self.tickets)
        return self.total_amount

class Payment:
    """Represents a payment made for a booking."""
    def __init__(self, payment_id, booking_id, amount, payment_date=None, method="Credit Card"):
        """Initializes a new Payment object.
        Args:
            payment_id (int): Unique identifier for the payment.
            booking_id (int): ID of the booking this payment is for.
            amount (float): Amount paid.
            payment_date (str, optional): Date and time of the payment. Defaults to current timestamp.
            method (str, optional): Payment method used (e.g., "Credit Card", "Debit Card"). Defaults to "Credit Card".
        """
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = payment_date if payment_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.method = method

    def get_payment_id(self):
        """Returns the payment ID."""
        return self.payment_id

    def get_booking_id(self):
        """Returns the ID of the booking this payment is for."""
        return self.booking_id

    def get_amount(self):
        """Returns the payment amount."""
        return self.amount

    def get_payment_date(self):
        """Returns the date and time of the payment."""
        return self.payment_date

    def get_method(self):
        """Returns the payment method used."""
        return self.method

    def process_payment(self):
        """Simulates processing a payment.
        In a real system, this would involve interaction with a payment gateway.
        Returns:
            bool: True to simulate successful payment.
        """
        return True # Simulate successful payment

class Admin:
    """Represents an administrator with privileges to view reports and modify system settings."""
    def __init__(self, admin_id, name):
        """Initializes a new Admin object.
        Args:
            admin_id (int): Unique identifier for the administrator.
            name (str): Name of the administrator.
        """
        self.admin_id = admin_id
        self.name = name

    def get_admin_id(self):
        """Returns the administrator ID."""
        return self.admin_id

    def get_name(self):
        """Returns the administrator's name."""
        return self.name

    def view_report(self, bookings):
        """Generates a sales report based on the provided bookings.
        Args:
            bookings (list): A list of Booking objects.
        Returns:
            dict: A dictionary where keys are event IDs and values are dictionaries of ticket names and their sales counts.
        """
        sales_report = {}
        for booking in bookings:
            event_id = booking.get_event_id()
            for ticket in booking.get_tickets():
                ticket_name = ticket.get_name()
                if event_id not in sales_report:
                    sales_report[event_id] = {}
                sales_report[event_id][ticket_name] = sales_report[event_id].get(ticket_name, 0) + 1
        return sales_report

    def modify_discount_availability(self, event, ticket_name, available):
        """Modifies the discount availability for a specific ticket type of an event.
        Args:
            event (RaceEvent): The RaceEvent object.
            ticket_name (str): The name of the ticket type.
            available (bool): True to make the discount available, False otherwise.
        Returns:
            bool: True if the discount availability was modified successfully, False otherwise.
        """
        ticket = event.get_ticket(ticket_name)
        if ticket:
            ticket.set_discount_availability(available)
            return True
        return False
class DataManager:
    """Manages the storage and retrieval of application data, including users, events, bookings, and payments."""
    def __init__(self, user_file="users.pkl", event_file="events.pkl", booking_file="bookings.pkl", payment_file="payments.pkl"):
        """Initializes the DataManager.
        Args:
            user_file (str, optional): Filename for storing user data. Defaults to "users.pkl".
            event_file (str, optional): Filename for storing event data. Defaults to "events.pkl".
            booking_file (str, optional): Filename for storing booking data. Defaults to "bookings.pkl".
            payment_file (str, optional): Filename for storing payment data. Defaults to "payments.pkl".
        """
        self.user_manager = AccountManager(user_file) # Manages user accounts
        self.events = self.load_events(event_file) # Loads race event data
        self.bookings = self.load_bookings(booking_file) # Loads booking data
        self.payments = self.load_payments(payment_file) # Loads payment data
        self.next_booking_id = self.get_next_id(self.bookings) + 1 # Generates the next unique booking ID
        self.next_payment_id = self.get_next_id(self.payments) + 1 # Generates the next unique payment ID
        self.event_filename = event_file # Filename for event data
        self.booking_filename = booking_file # Filename for booking data
        self.payment_filename = payment_file # Filename for payment data

    def get_next_id(self, data_dict):
        """Finds the next available ID in a dictionary of data.
        Args:
            data_dict (dict): A dictionary where keys are IDs.
        Returns:
            int: The next highest ID, or 0 if the dictionary is empty.
        """
        return max(data_dict.keys()) if data_dict else 0

    def get_account_manager(self):
        """Returns the AccountManager instance."""
        return self.user_manager

    def get_events(self):
        """Returns a list of all RaceEvent objects."""
        return list(self.events.values())

    def get_event(self, event_id):
        """Retrieves a RaceEvent object by its ID.
        Args:
            event_id (int): The ID of the event to retrieve.
        Returns:
            RaceEvent: The RaceEvent object if found, otherwise None.
        """
        return self.events.get(event_id)

    def add_event(self, event):
        """Adds a new RaceEvent object to the stored events.
        Args:
            event (RaceEvent): The RaceEvent object to add.
        """
        self.events[event.get_event_id()] = event
        self.save_events() # Persist the updated event data

    def save_events(self):
        """Saves the race event data to the pickle file."""
        try:
            with open(self.event_filename, 'wb') as f:
                pickle.dump(self.events, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save event data: {e}")

    def load_events(self, filename):
        """Loads the race event data from the pickle file.
        Args:
            filename (str): The name of the file to load from.
        Returns:
            dict: A dictionary containing RaceEvent objects, or an empty dictionary if the file doesn't exist or loading fails.
        """
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load event data: {e}")
        return {}

    def create_booking(self, user_id, event_id, selected_tickets):
        """Creates a new booking for a user for a specific event.
        Args:
            user_id (int): The ID of the user making the booking.
            event_id (int): The ID of the event being booked.
            selected_tickets (dict): A dictionary of ticket names and their quantities.
        Returns:
            Booking: The newly created Booking object if successful, otherwise None.
        """
        booking_id = self.next_booking_id
        self.next_booking_id += 1
        booking = Booking(booking_id, user_id, event_id) # Create a new Booking object
        event = self.get_event(event_id) # Retrieve the event details
        if event:
            for ticket_name, quantity in selected_tickets.items():
                ticket = event.get_ticket(ticket_name) # Get the Ticket object for the selected ticket name
                if ticket:
                    for _ in range(quantity):
                        # Create individual Ticket instances for the booking
                        booking.add_ticket(Ticket(ticket.get_ticket_id(), ticket.get_name(), ticket.get_price(), ticket.get_validity(), ticket.get_features()))
            user = self.user_manager.get_user(user_id) # Retrieve the user object
            if user:
                user.add_booking(booking) # Add the booking to the user's history
                self.bookings[booking_id] = booking # Store the booking
                self.user_manager.save_data() # Update user data (to save the new booking reference)
                self.save_bookings() # Persist the new booking data
                return booking
        return None

    def get_bookings_for_user(self, user_id):
        """Retrieves all bookings made by a specific user.
        Args:
            user_id (int): The ID of the user.
        Returns:
            list: A list of Booking objects associated with the user.
        """
        return [booking for booking in self.bookings.values() if booking.get_user_id() == user_id]

    def save_bookings(self):
        """Saves the booking data to the pickle file."""
        try:
            with open(self.booking_filename, 'wb') as f:
                pickle.dump(self.bookings, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save booking data: {e}")

    def load_bookings(self, filename):
        """Loads the booking data from the pickle file.
        Args:
            filename (str): The name of the file to load from.
        Returns:
            dict: A dictionary containing Booking objects, or an empty dictionary if the file doesn't exist or loading fails.
        """
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load booking data: {e}")
        return {}

    def create_payment(self, booking_id, amount, method):
        """Creates a new payment record for a booking.
        Args:
            booking_id (int): The ID of the booking the payment is for.
            amount (float): The amount paid.
            method (str): The payment method used.
        Returns:
            Payment: The newly created Payment object.
        """
        payment_id = self.next_payment_id
        self.next_payment_id += 1
        payment = Payment(payment_id, booking_id, amount, method=method) # Create a new Payment object
        self.payments[payment_id] = payment # Store the payment
        self.save_payments() # Persist the new payment data
        return payment

    def save_payments(self):
        """Saves the payment data to the pickle file."""
        try:
            with open(self.payment_filename, 'wb') as f:
                pickle.dump(self.payments, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save payment data: {e}")

    def load_payments(self, filename):
        """Loads the payment data from the pickle file.
        Args:
            filename (str): The name of the file to load from.
        Returns:
            dict: A dictionary containing Payment objects, or an empty dictionary if the file doesn't exist or loading fails.
        """
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load payment data: {e}")
        return {}

class GUI:
    """Graphical User Interface for the Race Event Ticket System."""
    def __init__(self, data_manager):
        """Initializes the GUI.
        Args:
            data_manager (DataManager): An instance of the DataManager class for data access.
        """
        self.data_manager = data_manager
        self.account_manager = data_manager.get_account_manager() # Get the account manager from data manager
        self.admin = Admin(1, "AdminUser") # Simple admin user instance
        self.current_user_id = None # Stores the ID of the currently logged-in user
        self.window = tk.Tk() # Create the main Tkinter window
        self.window.title("Race Event Ticket System") # Set the title of the window
        self.setup_login_register() # Initialize the login and registration interface

    def run(self):
        """Starts the Tkinter event loop, making the GUI interactive."""
        self.window.mainloop()

    def setup_login_register(self):
        """Sets up the login and registration screen."""
        # Destroy any existing widgets in the window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create a frame for the login section
        login_frame = ttk.LabelFrame(self.window, text="Login")
        login_frame.pack(padx=20, pady=20)

        # Email label and entry
        ttk.Label(login_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.login_email_entry = ttk.Entry(login_frame)
        self.login_email_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password label and entry (masked for security)
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.login_password_entry = ttk.Entry(login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login and Register buttons
        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        ttk.Button(login_frame, text="Register", command=self.setup_registration).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        """Handles the login process."""
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()
        # Iterate through the stored users to find a match
        for user in self.account_manager.users.values():
            if user.get_email() == email and user.get_password() == password:
                self.current_user_id = user.get_user_id() # Store the logged-in user's ID
                messagebox.showinfo("Login Successful", f"Welcome, {user.get_name()}!")
                self.show_main_menu() # Navigate to the main menu
                return
        # If no matching user is found
        messagebox.showerror("Login Failed", "Invalid email or password.")

    def setup_registration(self):
        """Sets up the user registration screen."""
        # Destroy any existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create a frame for registration
        reg_frame = ttk.LabelFrame(self.window, text="Register New Account")
        reg_frame.pack(padx=20, pady=20)

        # Name label and entry
        ttk.Label(reg_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.reg_name_entry = ttk.Entry(reg_frame)
        self.reg_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Email label and entry
        ttk.Label(reg_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.reg_email_entry = ttk.Entry(reg_frame)
        self.reg_email_entry.grid(row=1, column=1, padx=5, pady=5)

        # Password label and entry (masked)
        ttk.Label(reg_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.reg_password_entry = ttk.Entry(reg_frame, show="*")
        self.reg_password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Register and Back to Login buttons
        ttk.Button(reg_frame, text="Register", command=self.register_user).grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        ttk.Button(reg_frame, text="Back to Login", command=self.setup_login_register).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def register_user(self):
        """Handles the user registration process."""
        name = self.reg_name_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        # Check if all required fields are filled
        if not name or not email or not password:
            messagebox.showerror("Registration Failed", "All fields are required.")
            return
        try:
            # Attempt to create a new user account
            self.account_manager.create_account(name, email, password)
            messagebox.showinfo("Registration Successful", "Account created successfully. Please log in.")
            self.setup_login_register() # Go back to the login screen
        except ValueError as e:
            # Handle errors during account creation (e.g., email already exists)
            messagebox.showerror("Registration Failed", str(e))

    def show_main_menu(self):
        """Displays the main menu after successful login."""
        # Destroy all current widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create the main menu frame
        main_frame = ttk.LabelFrame(self.window, text="Main Menu")
        main_frame.pack(padx=20, pady=20)

        # Buttons for different functionalities
        ttk.Button(main_frame, text="View/Update Account", command=self.show_account_management).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Purchase Tickets", command=self.show_ticket_purchasing).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="View Booking History", command=self.show_booking_history).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Admin Dashboard", command=self.show_admin_dashboard).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Logout", command=self.setup_login_register).pack(fill=tk.X, pady=10)

    def show_account_management(self):
        """Displays the account management screen for the logged-in user."""
        # Check if a user is logged in
        if self.current_user_id is None:
            messagebox.showerror("Error", "No user logged in.")
            return

        # Destroy current widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Get the logged-in user's details
        user = self.account_manager.get_user(self.current_user_id)
        if not user:
            messagebox.showerror("Error", "User not found.")
            self.show_main_menu()
            return

        # Create the account management frame
        account_frame = ttk.LabelFrame(self.window, text="Account Management")
        account_frame.pack(padx=20, pady=20)

        # Display user information with entry fields for updates
        ttk.Label(account_frame, text=f"User ID: {user.get_user_id()}").pack(pady=2)
        ttk.Label(account_frame, text=f"Name:").pack(pady=2)
        self.name_entry = ttk.Entry(account_frame)
        self.name_entry.insert(0, user.get_name()) # Fill with current name
        self.name_entry.pack(pady=2)

        ttk.Label(account_frame, text=f"Email:").pack(pady=2)
        self.email_entry = ttk.Entry(account_frame)
        self.email_entry.insert(0, user.get_email()) # Fill with current email
        self.email_entry.pack(pady=2)

        ttk.Label(account_frame, text=f"Password:").pack(pady=2)
        self.password_entry = ttk.Entry(account_frame, show="*")
        self.password_entry.insert(0, user.get_password()) # Fill with current password (masked)
        self.password_entry.pack(pady=2)

        # Buttons for updating profile, viewing purchase orders, and going back to the main menu
        ttk.Button(account_frame, text="Update Profile", command=self.update_profile).pack(pady=10)
        ttk.Button(account_frame, text="View Purchase Orders", command=self.view_purchase_orders).pack(pady=5)
        ttk.Button(account_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def update_profile(self):
        """Handles the process of updating the logged-in user's profile."""
        # Check if a user is logged in
        if self.current_user_id is None:
            messagebox.showerror("Error", "No user logged in.")
            return
        # Get the updated information from the entry fields
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        # Attempt to update the user's information
        if self.account_manager.update_user(self.current_user_id, name, email, password):
            messagebox.showinfo("Profile Updated", "Your profile has been updated.")
        else:
            messagebox.showerror("Update Failed", "Could not update profile.")
        self.show_account_management() # Refresh the account management screen

    def view_purchase_orders(self):
        """Displays the purchase orders (booking history) for the logged-in user."""
        # Check if a user is logged in
        if self.current_user_id is None:
            messagebox.showerror("Error", "No user logged in.")
            return

        # Destroy current widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create a frame for displaying purchase orders
        orders_frame = ttk.LabelFrame(self.window, text="Purchase Orders")
        orders_frame.pack(padx=20, pady=20)

        # Get the logged-in user's details
        user = self.account_manager.get_user(self.current_user_id)
        if user:
            # Retrieve the user's booking history
            bookings = self.data_manager.get_bookings_for_user(user.get_user_id())
            if bookings:
                # Iterate through each booking and display its details
                for booking in bookings:
                    order_details = f"Booking ID: {booking.get_booking_id()}, Event ID: {booking.get_event_id()}, Date: {booking.get_booking_date()}, Total: ${booking.calculate_total():.2f}"
                    ttk.Label(orders_frame, text=order_details).pack(pady=2, anchor="w")
                    # Display the tickets within each booking
                    for ticket in booking.get_tickets():
                        ticket_info = f"  - {ticket.get_name()} (${ticket.get_price():.2f})"
                        ttk.Label(orders_frame, text=ticket_info).pack(pady=1, anchor="w")
                    ttk.Separator(orders_frame).pack(fill=tk.X, pady=5)
                else:
                    ttk.Label(orders_frame, text="No purchase orders found.").pack(pady=5)
            else:
                ttk.Label(orders_frame, text="User not found.").pack(pady=5)

            # Button to go back to the account management screen
            ttk.Button(orders_frame, text="Back to Account", command=self.show_account_management).pack(pady=10)

    def show_ticket_purchasing(self):
        """Displays the interface for purchasing tickets."""
        # Check if a user is logged in
        if self.current_user_id is None:
            messagebox.showerror("Error", "No user logged in.")
            return

        # Destroy current widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create a frame for purchasing tickets
        purchase_frame = ttk.LabelFrame(self.window, text="Purchase Tickets")
        purchase_frame.pack(padx=20, pady=20)

        # Label and Combobox to select an event
        event_label = ttk.Label(purchase_frame, text="Select Event:")
        event_label.pack(pady=5)
        self.event_combobox = ttk.Combobox(purchase_frame, values=[event.get_name() for event in self.data_manager.get_events()])
        self.event_combobox.pack(pady=5)
        self.event_combobox.bind("<<ComboboxSelected>>", self.populate_ticket_options) # Populate tickets when an event is selected

        # Dictionary to store ticket quantity selection frames
        self.ticket_frames = {}
        # Dictionary to store the selected tickets and their quantities for the cart
        self.cart = {}
        # Frame to hold the ticket options (populated after event selection)
        self.ticket_options_frame = ttk.Frame(purchase_frame)
        self.ticket_options_frame.pack(pady=10)

        # Label and Listbox to display the shopping cart
        self.cart_label = ttk.Label(purchase_frame, text="Shopping Cart:")
        self.cart_label.pack(pady=5)
        self.cart_listbox = tk.Listbox(purchase_frame, height=5)
        self.cart_listbox.pack(pady=5)

        # Buttons for adding to cart, removing from cart, checkout, and going back to the main menu
        ttk.Button(purchase_frame, text="Add to Cart", command=self.add_to_cart).pack(pady=5)
        ttk.Button(purchase_frame, text="Remove from Cart", command=self.remove_from_cart).pack(pady=5)
        ttk.Button(purchase_frame, text="Checkout", command=self.checkout).pack(pady=10)
        ttk.Button(purchase_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def populate_ticket_options(self, event=None):
        """Populates the ticket options frame based on the selected event."""
        selected_event_name = self.event_combobox.get()  # Get the name of the selected event from the combobox
        self.selected_event = None
        # Find the corresponding RaceEvent object
        for event_obj in self.data_manager.get_events():
            if event_obj.get_name() == selected_event_name:
                self.selected_event = event_obj
                break

        if self.selected_event:
            # Clear any existing widgets in the ticket options frame
            for widget in self.ticket_options_frame.winfo_children():
                widget.destroy()
            self.ticket_frames = {}  # Reset the dictionary to store ticket quantity spinboxes
            ttk.Label(self.ticket_options_frame, text="Select Ticket Quantities:").pack(pady=5)
            # Iterate through the available tickets for the selected event
            for ticket in self.selected_event.get_available_tickets():
                ticket_frame = ttk.Frame(self.ticket_options_frame)
                ticket_frame.pack(pady=2, anchor="w")
                # Display ticket name, price, validity, and features
                ttk.Label(ticket_frame,
                          text=f"{ticket.get_name()} (${ticket.get_price():.2f}) - {ticket.get_validity()} - {ticket.get_features()}: ").pack(
                    side=tk.LEFT)
                # Spinbox to select the quantity of each ticket
                qty_spinbox = tk.Spinbox(ticket_frame, from_=0, to=10)
                qty_spinbox.pack(side=tk.LEFT, padx=5)
                # Store the spinbox widget associated with the ticket name
                self.ticket_frames[ticket.get_name()] = qty_spinbox

    def add_to_cart(self):
        """Adds the selected tickets and their quantities to the shopping cart."""
        if not self.selected_event:
            messagebox.showerror("Error", "Please select an event first.")
            return

        # Iterate through the ticket quantity spinboxes
        for ticket_name, qty_widget in self.ticket_frames.items():
            quantity = int(qty_widget.get())  # Get the selected quantity
            if quantity > 0:
                # Add the selected quantity to the cart (or update if already present)
                self.cart[ticket_name] = self.cart.get(ticket_name, 0) + quantity
        self.update_cart_display()  # Refresh the display of the shopping cart

    def remove_from_cart(self):
        """Removes a selected item from the shopping cart."""
        selected_item_index = self.cart_listbox.curselection()  # Get the index of the selected item in the listbox
        if selected_item_index:
            # Extract the ticket name from the selected item string
            selected_ticket = self.cart_listbox.get(selected_item_index[0]).split(" x ")[1]
            if selected_ticket in self.cart:
                del self.cart[selected_ticket]  # Remove the ticket from the cart
                self.update_cart_display()  # Update the cart display

    def update_cart_display(self):
        """Updates the display of the shopping cart in the listbox."""
        self.cart_listbox.delete(0, tk.END)  # Clear the current contents of the listbox
        # Add each item in the cart to the listbox in the format "quantity x ticket_name"
        for ticket, qty in self.cart.items():
            self.cart_listbox.insert(tk.END, f"{qty} x {ticket}")

    def checkout(self):
        """Handles the checkout process, creating a booking and processing payment."""
        if not self.cart:
            messagebox.showinfo("Info", "Your cart is empty.")
            return

        if not self.selected_event:
            messagebox.showerror("Error", "No event selected.")
            return

        total_price = 0
        # Calculate the total price of the items in the cart
        for ticket_name, quantity in self.cart.items():
            ticket = self.selected_event.get_ticket(ticket_name)
            if ticket:
                total_price += ticket.get_price() * quantity

        # Prompt the user for a payment method
        payment_method = simpledialog.askstring("Payment", f"Total amount: ${total_price:.2f}\nEnter payment method:")
        if payment_method:
            # Create a new booking in the data manager
            booking = self.data_manager.create_booking(self.current_user_id, self.selected_event.get_event_id(),
                                                       self.cart)
            if booking:
                # Create a new payment record
                payment = self.data_manager.create_payment(booking.get_booking_id(), booking.calculate_total(),
                                                           payment_method)
                # Simulate payment processing
                if payment and payment.process_payment():
                    messagebox.showinfo("Checkout Successful",
                                        f"Booking successful! Booking ID: {booking.get_booking_id()}, Payment ID: {payment.get_payment_id()}, Total: ${payment.get_amount():.2f}, Method: {payment.get_method()}")
                    self.cart = {}  # Clear the shopping cart after successful checkout
                    self.update_cart_display()  # Update the cart display to show it's empty
                else:
                    messagebox.showerror("Payment Failed", "There was an issue processing your payment.")
            else:
                messagebox.showerror("Booking Failed", "Could not create booking.")

    def show_booking_history(self):
        """Displays the booking history for the logged-in user."""
        if self.current_user_id is None:
            messagebox.showerror("Error", "No user logged in.")
            return

        # Clear the current window content
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create a frame for the booking history
        history_frame = ttk.LabelFrame(self.window, text="Booking History")
        history_frame.pack(padx=20, pady=20)

        # Get the booking history for the current user
        bookings = self.data_manager.get_bookings_for_user(self.current_user_id)
        if bookings:
            # Iterate through each booking and display its details
            for booking in bookings:
                event = self.data_manager.get_event(booking.get_event_id())
                event_name = event.get_name() if event else "Unknown Event"
                booking_details = f"Booking ID: {booking.get_booking_id()}, Event: {event_name}, Date: {booking.get_booking_date()}, Total: ${booking.calculate_total():.2f}, Status: {booking.get_status()}"
                ttk.Label(history_frame, text=booking_details).pack(pady=2, anchor="w")
                # Display the tickets within each booking
                for ticket in booking.get_tickets():
                    ticket_info = f"  - {ticket.get_name()} (${ticket.get_price():.2f})"
                    ttk.Label(history_frame, text=ticket_info).pack(pady=1, anchor="w")
                ttk.Separator(history_frame).pack(fill=tk.X, pady=5)
        else:
            ttk.Label(history_frame, text="No booking history found.").pack(pady=5)

        # Button to go back to the main menu
        ttk.Button(history_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def show_admin_dashboard(self):
        """Displays the admin dashboard with sales report and discount modification options."""
        # Clear the current window content
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create a frame for the admin dashboard
        admin_frame = ttk.LabelFrame(self.window, text="Admin Dashboard")
        admin_frame.pack(padx=20, pady=20)

        # Display the ticket sales report
        ttk.Label(admin_frame, text="Ticket Sales Report:").pack(pady=5)
        bookings = self.data_manager.bookings.values()  # Get all bookings
        sales_report = self.admin.view_report(list(bookings))  # Generate the sales report
        report_text = tk.Text(admin_frame, height=10, width=50)
        report_text.pack(pady=5)
        # Format and display the sales report
        for event_id, sales in sales_report.items():
            event = self.data_manager.get_event(event_id)
            event_name = event.get_name() if event else f"Event ID {event_id}"
            report_text.insert(tk.END, f"Event: {event_name}\n")
            for ticket_name, count in sales.items():
                report_text.insert(tk.END, f"  - {ticket_name}: {count}\n")
            report_text.insert(tk.END, "\n")
        report_text.config(state=tk.DISABLED)  # Make the report text read-only

        # Section for modifying discount availability
        ttk.Label(admin_frame, text="Modify Discount Availability:").pack(pady=5)
        event_label_discount = ttk.Label(admin_frame, text="Select Event:")
        event_label_discount.pack()
        # Combobox to select an event for discount modification
        self.event_combobox_discount = ttk.Combobox(admin_frame, values=[event.get_name() for event in
                                                                         self.data_manager.get_events()])
        self.event_combobox_discount.pack()
        self.event_combobox_discount.bind("<<ComboboxSelected>>",
                                          self.populate_ticket_discount_options)  # Populate ticket options for discount modification

        # Frame to hold the ticket discount availability options
        self.ticket_discount_frame = ttk.Frame(admin_frame)
        self.ticket_discount_frame.pack(pady=5)

        # Button to go back to the main menu
        ttk.Button(admin_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def populate_ticket_discount_options(self, event=None):
        selected_event_name = self.event_combobox_discount.get()
        self.selected_discount_event = None
        for event_obj in self.data_manager.get_events():
            if event_obj.get_name() == selected_event_name:
                self.selected_discount_event = event_obj
                break

        if self.selected_discount_event:
            for widget in self.ticket_discount_frame.winfo_children():
                widget.destroy()
            ttk.Label(self.ticket_discount_frame, text="Set Discount Availability:").pack(pady=5)
            for ticket in self.selected_discount_event.get_available_tickets():
                discount_control = ttk.Frame(self.ticket_discount_frame)
                discount_control.pack(pady=2, anchor="w")
                ttk.Label(discount_control, text=f"{ticket.get_name()}: ").pack(side=tk.LEFT)
                available_var = tk.BooleanVar(value=ticket.is_discount_available())
                checkbutton = ttk.Checkbutton(discount_control, text="Available", variable=available_var, command=lambda t=ticket, var=available_var: self.update_discount(self.selected_discount_event, t.get_name(), var.get()))
                checkbutton.pack(side=tk.LEFT)

    def update_discount(self, event, ticket_name, available):
        if event:
            if self.admin.modify_discount_availability(event, ticket_name, available):
                messagebox.showinfo("Discount Updated", f"Discount for {ticket_name} set to {'available' if available else 'unavailable'}.")
            else:
                messagebox.showerror("Update Failed", f"Could not update discount for {ticket_name}.")

if __name__ == "__main__":
    data_manager = DataManager()

    # Initialize some events and tickets if they don't exist
    if not data_manager.get_events():
        event1 = RaceEvent(1, "Grand National", "2025-06-10", "Aintree Racecourse", 500)
        event1.add_ticket(Ticket(101, "Single Race", 50.00, "Valid for one race", "Access to general areas"))
        event1.add_ticket(Ticket(102, "Weekend Package", 120.00, "Valid for all weekend races", "Access to VIP lounge"))
        event1.add_ticket(Ticket(103, "Group Discount", 45.00, "Per person for groups of 5+", "General access, group booking only"))
        data_manager.add_event(event1)

        event2 = RaceEvent(2, "Royal Ascot", "2025-07-15", "Ascot Racecourse", 1000)
        event2.add_ticket(Ticket(201, "Queen Anne Enclosure", 80.00, "Access to Queen Anne Enclosure", "Dress code applies"))
        event2.add_ticket(Ticket(202, "Village Enclosure", 60.00, "Access to Village Enclosure", "Lively atmosphere"))
        data_manager.add_event(event2)

    gui = GUI(data_manager)
    gui.run()