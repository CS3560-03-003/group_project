import tkinter as tk
from tkinter import ttk, messagebox
import mysql

# Connect to existing code
# main should be what your main code is titled
import main as db_app

class RestaurantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Review System")
        self.root.geometry("600x500")

        # Store the logged-in user object here (Owner or Customer)
        self.current_user = None

        # Start with the login screen
        self.show_login_screen()

    def clear_window(self):
        # clear window to change screen
        for widget in self.root.winfo_children():
            widget.destroy()

    # Set up login screen
    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Yelp Wannabe", font = ("Ariel", 20)).pack(pady = 20)

        # User Type Selection
        self.user_type_var = tk.StringVar(value = "Customer")
        frame_type = tk.Frame(self.root)
        frame_type.pack(pady = 5)
        tk.Radiobutton(frame_type, text = "Customer", variable = self.user_type_var, value = "Customer").pack(side = tk.LEFT, padx = 10)
        tk.Radiobutton(frame_type, text = "Owner", variable = self.user_type_var, value = "Owner").pack(side = tk.LEFT, padx = 10)

        # Inputs
        tk.Label(self.root, text = "Username:").pack(pady = 5)
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady = 5)

        tk.Label(self.root, text = "Password:").pack(pady = 5)
        self.entry_pass = tk.Entry(self.root, show = "*")
        self.entry_pass.pack(pady = 5)

        tk.Button(self.root, text = "Login", command = self.perform_login, bg = "#4CAF50", fg = "white").pack(pady = 20)

    def perform_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        user_type = self.user_type_var.get()

        if user_type == "Owner":
            # Login with main code for owner
            user = db_app.Owner.login(username, password)
        else:
            # Login with main code for customer
            user = db_app.Customer.login(username, password)

        if user:
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome, {user.full_name}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid login")

    # Set up dashboard screen
    def show_dashboard(self):
        self.clear_window()

        # Header
        header_text = f"Dashboard: {self.current_user.full_name} ({type(self.current_user).__name__})"
        tk.Label(self.root, text = header_text, font = ("Arial", 14, "bold")).pack(pady = 10)

        # Print depending on if customer or owner
        if isinstance(self.current_user, db_app.Customer):
            self.show_customer_menu()
        elif isinstance(self.current_user, db_app.Owner):
            self.show_owner_menu()

        tk.Button(self.root, text = "Logout", command = self.show_login_screen, fg = "red").pack(side = tk.BOTTOM, pady = 20)

    # set up customer options
    def show_customer_menu(self):
        frame = tk.Frame(self.root)
        frame.pack(pady = 20)

        tk.Button(frame, text = "Write a Review", width = 20, command = self.show_add_review_form).pack(pady = 10)
        tk.Button(frame, text = "Search Restaurant", width = 20, command = self.show_add_review_form).pack(pady = 10)

    def get_all_restaurant_names(self):

        names = []
        try:
            # Use the database
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM restaurant ORDER BY name ASC")
            results = cursor.fetchall()

            # Get just the names of the restaurants
            names = [row[0] for row in results]

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not fetch restaurants: {e}")
        return names

    def show_add_review_form(self):
        self.clear_window()
        tk.Label(self.root, text = "Write a New Review", font = ("Arial", 16)).pack(pady = 10)

        tk.Label(self.root, text="Select Restaurant:").pack()
        self.combo_res_name = ttk.Combobox(self.root, width = 30, state = "readonly")
        self.combo_res_name['values'] = self.get_all_restaurant_names()
        if self.combo_res_name['values']:
            self.combo_res_name.current(0)
        self.combo_res_name.pack(pady = 5)

        tk.Label(self.root, text = "Rating (1-5):").pack()

        combo_rating = ttk.Combobox(self.root, values = [1, 2, 3, 4, 5], state = "readonly")
        combo_rating.current(4)  # Default to 5 stars
        combo_rating.pack(pady = 5)

        restaurant_names = self.get_all_restaurant_names()
        self.combo_res_name['values'] = restaurant_names

        if restaurant_names:
            self.combo_res_name.current(0)  # start on first name

        tk.Label(self.root, text = "Review Content:").pack()
        entry_content = tk.Entry(self.root, width = 50)
        entry_content.pack(pady = 5)

        def submit_review():
            res_name = self.combo_res_name.get()
            # Use EV_main.py method
            restaurant = db_app.Restaurant.get_restaurant_by_name(res_name)

            if not restaurant:
                messagebox.showerror("Error", "Restaurant not found!")
                return

            # make review object
            try:
                rating = float(combo_rating.get())
            except ValueError:
                messagebox.showerror("Error", "Please select a rating")
                return

            new_review = db_app.Review(
                review_id = None,
                restaurant_id = restaurant.restaurant_id,
                user_id = self.current_user.customer_id,
                rating = rating,
                review_content = entry_content.get(),
                review_date = ""
            )

            # use main method
            if new_review.save():
                messagebox.showinfo("Success", "Review posted!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Failed to save review.")

        tk.Button(self.root, text = "Submit Review", command = submit_review, bg = "blue", fg = "white").pack(pady = 10)
        tk.Button(self.root, text = "Back", command = self.show_dashboard).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantGUI(root)
    root.mainloop()
