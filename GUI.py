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

        def show_registration_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Create Account", font = ("Arial", 20, "bold")).pack(pady = 20)

        # User Type Selection
        tk.Label(self.root, text = "I am a:").pack()
        type_var = tk.StringVar(value = "Customer")
        frame_type = tk.Frame(self.root)
        frame_type.pack(pady = 5)

        tk.Radiobutton(frame_type, text = "Customer", variable = type_var, value = "Customer").pack(
            side = tk.LEFT, padx = 10)
        tk.Radiobutton(frame_type, text = "Restaurant Owner", variable = type_var, value = "Owner").pack(
            side = tk.LEFT, padx = 10)

        # Inputs
        entries = {}
        fields = ["Username", "Password", "Full Name", "Email"]

        for field in fields:
            tk.Label(self.root, text = f"{field}:").pack(pady = (5, 0))
            entry = tk.Entry(self.root, width = 30)
            if field == "Password":
                entry.config(show = "*")
            entry.pack(pady = 2)
            entries[field] = entry
    
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

    def show_search_reviews_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Search Reviews by Restaurant",
                 font=("Arial", 16), bg = "#E3F2FD", fg = "#0D47A1").pack(pady = 10)

        search_frame = tk.Frame(self.root, bg = "#E3F2FD")
        search_frame.pack(pady = 10)

        tk.Label(search_frame, text = "Restaurant Name:", bg = "#E3F2FD").pack(side = tk.LEFT, padx = 5)

        self.search_combo = ttk.Combobox(search_frame, width = 30, state = "readonly")
        self.search_combo.pack(side = tk.LEFT, padx = 5)

        res_names = self.get_all_restaurant_names()
        self.search_combo['values'] = res_names
        if res_names:
            self.search_combo.current(0)

        columns = ('Restaurant', 'Rating', 'Review', 'Reply')
        tree = ttk.Treeview(self.root, columns = columns, show = 'headings', height = 10)

        # Define Column Headings
        tree.heading('Restaurant', text = 'Restaurant')
        tree.heading('Rating', text = 'Rating')
        tree.heading('Review', text = 'Review')
        tree.heading('Reply', text = 'Owner Reply')

        # Define Column Widths
        tree.column('Restaurant', width = 120)
        tree.column('Rating', width = 50, anchor='center')
        tree.column('Review', width = 250)
        tree.column('Reply', width = 250)

        tree.pack(pady = 10, padx = 20, fill = tk.BOTH, expand = True)

        def perform_search():
            # Name from dropdown
            r_name = self.search_combo.get().strip()

            if not r_name:
                return

            # Logic used from main
            r_name_clean = r_name.replace(" ", "").lower()

            # clear previous
            for item in tree.get_children():
                tree.delete(item)

            try:
                conn = db_app.get_DB_CONFIG_connection()
                cursor = conn.cursor()

                query = """
                    SELECT 
                        b.name, a.rating, a.reviewContent, c.replyContent
                    FROM reviews a
                    JOIN restaurant b ON b.restaurantID = a.restaurantID
                    LEFT JOIN replies c ON a.reviewID = c.reviewID
                    WHERE REPLACE(LOWER(b.name), ' ', '') = %s
                    ORDER BY a.reviewDate DESC
                """

                cursor.execute(query, (r_name_clean,))
                results = cursor.fetchall()

                if not results:
                    messagebox.showinfo("Info", f"No reviews found for '{r_name}'.")

                for row in results:
                    # Handle no reply
                    restaurant_name, rating, content, reply = row
                    display_reply = reply if reply else "No Reply"
                    tree.insert('', tk.END, values = (restaurant_name, rating, content, display_reply))

                cursor.close()
                conn.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error searching: {err}")

        # Search Button
        tk.Button(search_frame, text = "Search", command = perform_search,
                  bg = "#2196F3", fg = "white").pack(side = tk.LEFT, padx = 10)

        # Back Button
        tk.Button(self.root, text = "Back to Dashboard", command = self.show_dashboard).pack(pady = 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantGUI(root)
    root.mainloop()
