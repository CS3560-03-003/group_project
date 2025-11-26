import tkinter as tk
from tkinter import ttk, messagebox
import mysql

# Connect to existing code
# main should be what your main code is titled
import Main as db_app

class RestaurantGUI:
    def __init__(self, root):
        self.all_restaurant_names = None
        self.root = root
        self.root.title("Restaurant Review System")
        self.root.geometry("700x600")

        # Store the logged-in user object here (Owner or Customer)
        self.current_user = None

        # Start with the login screen
        self.show_login_screen()

    # clear window to change screen
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # clear current user
    def logout(self):
        self.current_user = None
        self.show_login_screen()

    # Set up login screen
    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Yelp Wannabe", font = ("Arial", 20)).pack(pady = 20)

        # User Type Selection
        self.user_type_var = tk.StringVar(value = "Customer")
        frame_type = tk.Frame(self.root)
        frame_type.pack(pady = 5)
        tk.Radiobutton(frame_type, text = "Customer", variable = self.user_type_var, value = "Customer").pack(side = "left", padx = 10)
        tk.Radiobutton(frame_type, text = "Owner", variable = self.user_type_var, value = "Owner").pack(side = "left", padx = 10)

        # For the create account and Search at the bottom of the page
        footer_frame = tk.Frame(self.root)
        footer_frame.pack(side = "bottom", fill = "x", padx = 20, pady = 20)
        tk.Button(footer_frame, text = "Create New Account", command = self.show_registration_screen).pack(side = "left")
        tk.Button(footer_frame, text = "Restaurant Search", command = self.show_search_reviews_screen).pack(side = "right")

        # Username text box
        tk.Label(self.root, text = "Username:").pack(pady = 5)
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady = 5)

        # Owner text box
        tk.Label(self.root, text = "Password:").pack(pady = 5)
        self.entry_pass = tk.Entry(self.root, show = "*") # to hide password
        self.entry_pass.pack(pady = 5)

        # Log in button
        tk.Button(self.root, text = "Login", command = self.perform_login).pack(pady = 20)

    # Set up create an account screen
    def show_registration_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Create Account", font = ("Arial", 20)).pack(pady = 20)

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

        # loop to make text boxes
        for field in fields:
            tk.Label(self.root, text = f"{field}:").pack(pady = (5, 0))
            entry = tk.Entry(self.root, width = 30)
            if field == "Password":
                entry.config(show = "*")
            entry.pack(pady = 2)
            entries[field] = entry

        # perform account creation
        def perform_registration():
            user_type = type_var.get()
            username = entries["Username"].get().strip()
            password = entries["Password"].get().strip()
            full_name = entries["Full Name"].get().strip()
            email = entries["Email"].get().strip()

            if not all([username, password, full_name, email]):
                messagebox.showwarning("Missing Data", "Please fill in all fields.")
                return

            # make owner or customer object
            if user_type == "Owner":
                new_user = db_app.Owner(0, username, password, email, full_name)
                success = new_user.register()
            else:
                new_user = db_app.Customer(0, username, password, email, full_name)
                success = new_user.register()

            if success:
                messagebox.showinfo("Success", "Account created! Please log in.")
                self.show_login_screen()
            else:
                messagebox.showerror("Error", "Registration failed. Username/Email may exist.")

        tk.Button(self.root, text = "Sign Up", command = perform_registration, width = 15).pack(
            pady = 20)
        tk.Button(self.root, text = "Cancel", command = self.show_login_screen).pack(pady = 5)

    # Log in
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
        tk.Label(self.root, text = header_text, font = ("Arial", 20)).pack(pady = 20)

        # Print depending on if customer or owner
        if isinstance(self.current_user, db_app.Customer):
            self.show_customer_menu()
        elif isinstance(self.current_user, db_app.Owner):
            self.show_owner_menu()

        tk.Button(self.root, text = "Logout", command = self.logout, fg = "red").pack(side = tk.BOTTOM, pady = 20)

    # set up customer options
    def show_customer_menu(self):
        frame = tk.Frame(self.root)
        frame.pack(pady = 20)

        tk.Button(frame, text = "Search Restaurant", width = 20, command = self.show_search_reviews_screen).pack(pady = 10)
        tk.Button(frame, text = "Write a Review", width = 20, command = self.show_add_review_form).pack(pady = 10)
        tk.Button(frame, text = "Manage My Reviews (Edit/Delete)", width = 30, command=self.show_my_reviews_screen).pack(pady = 10)
        tk.Button(frame, text = "Edit Account Info", width = 30, command = self.show_edit_account_screen).pack(pady = 10)

    # set up owner options
    def show_owner_menu(self):
        frame = tk.Frame(self.root)
        frame.pack(pady = 20)

        tk.Button(frame, text = "Search All Reviews", width = 30, command = self.show_search_reviews_screen).pack(pady = 10)
        tk.Button(frame, text = "Reply or Delete Reviews", width = 30, command = self.show_owner_reply_screen).pack(pady = 10)
        tk.Button(frame, text = "View Restaurants", width = 30, command = self.show_owner_restaurants_screen).pack(pady = 10)
        tk.Button(frame, text = "Add New Restaurant", width = 35, command = self.show_add_restaurant_screen).pack(pady = 10)
        tk.Button(frame, text = "Edit a Restaurant", width = 35, command = self.show_edit_restaurant_screen).pack(pady = 10)
        tk.Button(frame, text="Edit Account Settings", width=35, command = self.show_edit_account_screen).pack(pady = 10)

    # set up owner restaurants screen
    def show_owner_restaurants_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "My Restaurants Overview", font = ("Arial", 16, "bold")).pack(pady = 20)

        columns = ('Name', 'Cuisine', 'Price', 'Hours', 'Phone', 'Address')
        tree = ttk.Treeview(self.root, columns = columns, show = 'headings', height = 15)

        tree.heading('Name', text = 'Name')
        tree.column('Name', width = 150, anchor = 'w')

        tree.heading('Cuisine', text = 'Cuisine')
        tree.column('Cuisine', width = 100, anchor = 'center')

        tree.heading('Price', text = 'Price')
        tree.column('Price', width = 60, anchor = 'center')

        tree.heading('Hours', text = 'Hours')
        tree.column('Hours', width = 120, anchor='w')

        tree.heading('Phone', text = 'Phone')
        tree.column('Phone', width = 100, anchor = 'center')

        tree.heading('Address', text = 'Address')
        tree.column('Address', width = 200, anchor = 'w')

        tree.pack(pady = 10, padx = 20, fill = tk.BOTH, expand = True)

        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()

            query = """
                SELECT name, cuisine, priceRange, operatingHours, phoneNumber, address 
                FROM restaurant 
                WHERE ownerID = %s
                ORDER BY name
            """
            cursor.execute(query, (self.current_user.owner_id,))
            rows = cursor.fetchall()

            if not rows:
                tk.Label(self.root, text = "You haven't added any restaurants yet.").pack()

            for row in rows:
                tree.insert('', tk.END, values = row)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        tk.Button(self.root, text = "Back to Dashboard", command = self.show_dashboard).pack(side = tk.BOTTOM, pady = 20)

    # set up owner reply screen
    def show_owner_reply_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Manage & Reply to Reviews", font = ("Arial", 16, "bold")).pack(pady = 20)
        tk.Label(self.root, text = "Select a review to reply or delete.",font = ("Arial", 10, "italic")).pack(pady = 5)

        columns = ('Review ID', 'Restaurant', 'Review', 'Current Reply')
        tree = ttk.Treeview(self.root, columns = columns, show = 'headings', height = 10)

        tree.heading('Review ID', text = 'ID')
        tree.column('Review ID', width = 50, anchor = 'center')

        tree.heading('Restaurant', text = 'Restaurant')
        tree.column('Restaurant', width = 150)

        tree.heading('Review', text = 'Customer Review')
        tree.column('Review', width = 300)

        tree.heading('Current Reply', text = 'Your Reply')
        tree.column('Current Reply', width = 300)

        tree.pack(pady = 10, padx = 20, fill = tk.BOTH, expand = True)

        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()

            query = """
                SELECT r.reviewID, res.name, r.reviewContent, rep.replyContent
                FROM reviews r
                JOIN restaurant res ON r.restaurantID = res.restaurantID
                LEFT JOIN replies rep ON r.reviewID = rep.reviewID
                WHERE res.ownerID = %s
                ORDER BY r.reviewDate DESC
            """
            cursor.execute(query, (self.current_user.owner_id,))
            rows = cursor.fetchall()

            if not rows:
                tk.Label(self.root, text="No reviews found for your restaurants.").pack()
            for row in rows:
                review_id, res_name, content, reply_content = row
                display_reply = reply_content if reply_content else "No Reply"

                tree.insert('', tk.END, values=(review_id, res_name, content, display_reply))
            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady = 20)

        tk.Label(input_frame, text = "Write Reply/Update:", font = ("Arial", 10, "bold")).pack(anchor = "w")
        reply_entry = tk.Entry(input_frame, width = 60)
        reply_entry.pack(pady = 5)

        def get_selected_review_id():
            # 1. Ask the treeview what is selected RIGHT NOW
            current_selection = tree.selection()

            if not current_selection:
                messagebox.showwarning("Warning", "Please click on a review in the list first.")
                return None

            # 2. Get the values from that specific row
            # tree.item(current_selection[0]) returns a dictionary. 'values' is the list of column data.
            row_values = tree.item(current_selection[0])['values']

            # 3. The Review ID is the first column (Index 0)
            raw_id = row_values[0]

            # 4. Clean it up (Handles the tuple error we saw before)
            if isinstance(raw_id, (list, tuple)):
                return int(raw_id[0])
            return int(raw_id)

        # --- POST / UPDATE LOGIC ---
        def post_or_update_reply():
            # 1. CALL THE HELPER (This ensures we get the ID of the clicked row)
            review_id = get_selected_review_id()
            if not review_id: return

            content = reply_entry.get().strip()
            if not content:
                messagebox.showwarning("Warning", "Reply cannot be empty.")
                return

            try:
                conn = db_app.get_DB_CONFIG_connection()
                cursor = conn.cursor()

                # Check if a reply ALREADY exists for this SPECIFIC review_id
                cursor.execute("SELECT replyID FROM replies WHERE reviewID = %s", (review_id,))
                existing = cursor.fetchone()

                if existing:
                    # UPDATE existing reply
                    update_query = "UPDATE replies SET replyContent = %s, replyDate = CURDATE() WHERE reviewID = %s"
                    cursor.execute(update_query, (content, review_id))
                    action = "updated"
                else:
                    # INSERT new reply
                    insert_query = "INSERT INTO replies (reviewID, ownerID, replyContent, replyDate) VALUES (%s, %s, %s, CURDATE())"
                    cursor.execute(insert_query, (review_id, self.current_user.owner_id, content))
                    action = "posted"

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", f"Reply {action} successfully!")

                # Clear the input box so you don't accidentally reply with old text later
                reply_entry.delete(0, tk.END)

                self.show_owner_reply_screen()  # Refresh table

            except Exception as e:
                messagebox.showerror("Error", str(e))

        def delete_review():
            raw_id = tree.selection()
            if not raw_id: return

            item_data = tree.item(raw_id[0])
            review_id = item_data['values'][0]

            if not messagebox.askyesno("Confirm Delete", "Delete this review?\nThis cannot be undone."):
                return

            # call main function
            if db_app.Review.delete(review_id):
                messagebox.showinfo("Deleted", "Review has been removed.")
                self.show_owner_reply_screen()  # Refresh
            else:
                messagebox.showerror("Error", "Failed to delete review.")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady = 10)

        tk.Button(btn_frame, text = "Submit", command = post_or_update_reply, width = 15).pack(side = tk.LEFT, padx = 10)
        tk.Button(btn_frame, text = "Delete Review", command = delete_review).pack(side = tk.LEFT, padx = 10)
        tk.Button(btn_frame, text = "Back to Dashboard", command = self.show_dashboard).pack(side = tk.LEFT, padx = 10)

    # set up add restaurant screen
    def show_add_restaurant_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Add New Restaurant", font = ("Arial", 16, "bold")).pack(pady = 20)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady = 10)

        self.new_res_entries = {}
        fields = ["Name", "Email", "Phone", "Address", "Cuisine", "Price Range", "Hours"]

        for i, label_text in enumerate(fields):
            tk.Label(form_frame, text = f"{label_text}:", font = ("Arial", 10, "bold")).grid(row = i, column = 0, sticky = "e", pady = 5, padx = 10)

            entry = tk.Entry(form_frame, width = 40)
            entry.grid(row = i, column = 1, pady = 5, padx = 10)

            key = label_text
            self.new_res_entries[key] = entry

        def save_new_restaurant():
            name = self.new_res_entries["Name"].get().strip()
            email = self.new_res_entries["Email"].get().strip()
            phone = self.new_res_entries["Phone"].get().strip()
            address = self.new_res_entries["Address"].get().strip()
            cuisine = self.new_res_entries["Cuisine"].get().strip()
            price = self.new_res_entries["Price Range"].get().strip()
            hours = self.new_res_entries["Hours"].get().strip()

            if not all([name, email, phone, address, cuisine, price, hours]):
                messagebox.showwarning("Missing Info", "All fields are required.")
                return

            new_res = db_app.Restaurant(
                restaurant_id = 0,
                name = name,
                email = email,
                address = address,
                phoneNumber = phone,
                priceRange = price,
                operatingHours = hours,
                cuisine = cuisine,
                owner_id = self.current_user.owner_id
            )

            if new_res.save():
                messagebox.showinfo("Success", f"{name} has been added!")
                self.show_dashboard()  # Go back to menu
            else:
                messagebox.showerror("Error", "Could not save restaurant. Check console.")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady = 20)

        tk.Button(btn_frame, text = "Save Restaurant", command = save_new_restaurant, width = 20).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Cancel", command = self.show_dashboard).pack(side = tk.LEFT, padx = 10)

    # set up retaurant edit page
    def show_edit_restaurant_screen(self):
        self.clear_window()


        tk.Label(self.root, text = "Select Restaurant to Edit", font = ("Arial", 16, "bold")).pack(pady = 20)

        columns = ('ID', 'Name', 'Cuisine', 'Price', 'Phone')
        tree = ttk.Treeview(self.root, columns = columns, show = 'headings', height = 10)

        tree.heading('ID', text = 'ID')
        tree.column('ID', width = 40, anchor = 'center')

        tree.heading('Name', text = 'Name')
        tree.column('Name', width = 150, anchor = 'w')

        tree.heading('Cuisine', text = 'Cuisine')
        tree.column('Cuisine', width = 100, anchor = 'center')

        tree.heading('Price', text = 'Price')
        tree.column('Price', width = 60, anchor = 'center')

        tree.heading('Phone', text = 'Phone')
        tree.column('Phone', width = 100, anchor = 'center')

        tree.pack(pady = 10, padx = 20, fill = tk.BOTH, expand = True)

        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()
            query = "SELECT restaurantID, name, cuisine, priceRange, phoneNumber FROM restaurant WHERE ownerID = %s"
            cursor.execute(query, (self.current_user.owner_id,))
            rows = cursor.fetchall()

            for row in rows:
                tree.insert('', tk.END, values = row)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        # --- BUTTONS ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady = 20)

        def go_to_edit_form():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a restaurant first.")
                return

            item = tree.item(selected[0])
            res_id = item['values'][0]

            # Navigate to the form
            self.show_edit_restaurant_form(res_id)

        tk.Button(btn_frame, text = "Edit Selected", command = go_to_edit_form, width = 20).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Back", command = self.show_dashboard).pack(side = tk.LEFT, padx = 10)

    # set up restaurant edit form
    def show_edit_restaurant_form(self, res_id):
        self.clear_window()


        tk.Label(self.root, text = "Edit Restaurant Details", font = ("Arial", 16, "bold")).pack(pady = 20)

        current_data = {}
        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor(dictionary = True)
            query = "SELECT * FROM restaurant WHERE restaurantID = %s"
            cursor.execute(query, (res_id,))
            current_data = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.show_edit_restaurant_selector()
            return

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady = 10)

        self.edit_res_entries = {}

        fields = {
            "Name": "name",
            "Email": "email",
            "Phone": "phoneNumber",
            "Address": "address",
            "Cuisine": "cuisine",
            "Price Range": "priceRange",
            "Hours": "operatingHours"
        }

        for i, (label, col_name) in enumerate(fields.items()):
            tk.Label(form_frame, text = f"{label}:", font = ("Arial", 10, "bold")).grid(row = i, column = 0, sticky = "e", pady = 5, padx = 10)

            entry = tk.Entry(form_frame, width = 40)
            val = current_data.get(col_name, "")
            entry.insert(0, str(val))
            entry.grid(row = i, column = 1, pady = 5, padx = 10)

            self.edit_res_entries[label] = entry

        def save_changes():
            data = {k: v.get().strip() for k, v in self.edit_res_entries.items()}
            if not all(data.values()):
                messagebox.showwarning("Warning", "All fields are required.")
                return

            # Reuse existing save() method
            updated_res = db_app.Restaurant(
                restaurant_id=res_id,
                name=data["Name"],
                email=data["Email"],
                address=data["Address"],
                phoneNumber=data["Phone"],
                priceRange=data["Price Range"],
                operatingHours=data["Hours"],
                cuisine=data["Cuisine"],
                owner_id=self.current_user.owner_id
            )

            if updated_res.save():
                messagebox.showinfo("Success", "Restaurant updated successfully!")
                self.show_edit_restaurant_screen()
            else:
                messagebox.showerror("Error", "Update failed.")

        def delete_restaurant():
            if not messagebox.askyesno("Confirm Delete",
                                       "Are you sure you want to delete this restaurant?\nALL reviews and replies will also be deleted.\nThis cannot be undone."):
                return

            if db_app.Restaurant.delete(res_id):
                messagebox.showinfo("Deleted", "Restaurant deleted.")
                self.show_edit_restaurant_screen()  # Return to list
            else:
                messagebox.showerror("Error", "Failed to delete restaurant. Check console.")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady = 20)

        tk.Button(btn_frame, text = "Save Changes", command = save_changes, width = 15).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Delete Restaurant", command = delete_restaurant, width = 15).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Cancel", command = self.show_edit_restaurant_screen).pack(side = tk.LEFT, padx = 10)

    # helper method to get restaurant information
    def get_all_restaurant_names(self):
        names = []
        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM restaurant ORDER BY name ASC")
            names = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not fetch restaurants: {e}")
        return names

    # set up the review page
    def show_add_review_form(self):
        self.clear_window()
        tk.Label(self.root, text = "Write a New Review", font = ("Arial", 16)).pack(pady = 10)

        tk.Label(self.root, text = "Select Restaurant (Type to Search):").pack()
        self.all_restaurant_names = self.get_all_restaurant_names()

        self.combo_res_name = ttk.Combobox(self.root, width = 30)
        self.combo_res_name.pack(pady = 5)
        self.combo_res_name['values'] = self.all_restaurant_names

        def check_input(event):
            # Get what the user typed
            value = event.widget.get()

            if value == '':
                # If empty, show all options
                self.combo_res_name['values'] = self.all_restaurant_names
            else:
                # Filter the list (Case-insensitive)
                data = []
                for item in self.all_restaurant_names:
                    if value.lower() in item.lower():
                        data.append(item)

                # Update the dropdown list with matches
                self.combo_res_name['values'] = data

        # Bind the function to keyboard typing
        self.combo_res_name.bind('<KeyRelease>', check_input)
        # -----------------------

        # --- 2. RATING & CONTENT ---
        tk.Label(self.root, text="Rating (1-5):").pack()
        combo_rating = ttk.Combobox(self.root, values=[1, 2, 3, 4, 5], state="readonly")
        combo_rating.current(4)
        combo_rating.pack(pady=5)

        tk.Label(self.root, text="Review Content:").pack()
        entry_content = tk.Entry(self.root, width=50)
        entry_content.pack(pady=5)

        def submit_review():
            res_name = self.combo_res_name.get()
            # Use main.py method
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

    # set up own reviews page
    def show_my_reviews_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "My Reviews", font = ("Arial", 16, "bold")).pack(pady = 10)
        tk.Label(self.root, text = "Select a review to Edit or Delete").pack(pady = 5)

        cols = ('Review ID', 'Restaurant', 'Rating', 'Review', 'Reply')
        tree = ttk.Treeview(self.root, columns = cols, show = 'headings', height = 10)

        # Define Columns
        tree.heading('Review ID', text = 'ID')
        tree.column('Review ID', width = 50, anchor = 'center')

        tree.heading('Restaurant', text = 'Restaurant')
        tree.column('Restaurant', width = 150)

        tree.heading('Rating', text = 'Rating')
        tree.column('Rating', width = 50, anchor = 'center')

        tree.heading('Review', text = 'Review')
        tree.column('Review', width = 250)

        tree.heading('Reply', text = 'Owner Reply')
        tree.column('Reply', width = 200)

        tree.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)

        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()

            # Get reviews ONLY for this logged-in customer
            query = """
                SELECT re.reviewID, r.name, re.rating, re.reviewContent, c.replyContent
                FROM reviews re
                JOIN restaurant r ON r.restaurantID = re.restaurantID
                LEFT JOIN replies c ON re.reviewID = c.reviewID
                WHERE re.customerID = %s
                ORDER BY re.reviewDate DESC
            """
            cursor.execute(query, (self.current_user.customer_id,))
            results = cursor.fetchall()

            if not results:
                tk.Label(self.root, text = "You haven't written any reviews yet.").pack()

            for row in results:
                reply_text = row[4] if row[4] else "No Reply"
                tree.insert('', tk.END, values = (row[0], row[1], row[2], row[3], reply_text))

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady = 20)

        def go_to_edit_page():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a review from the list first.")
                return

            item_values = tree.item(selected[0])['values']
            review_id = item_values[0]

            # Navigate to the next screen, passing the ID
            self.show_edit_review_form(review_id)

        tk.Button(btn_frame, text = "Edit Selected", command = go_to_edit_page,
                  bg = "#FF9800", fg = "white", font = ("Arial", 11, "bold")).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Back to Dashboard", command = self.show_dashboard).pack(side = tk.LEFT, padx = 10)

    # helper method to get restaurants reviewed by certian user
    def fetch_reviewed_restaurants(self):
        self.my_reviews_map = {}

        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor(dictionary = True)

            query = """
                        SELECT r.name, re.reviewID, re.rating, re.reviewContent
                        FROM reviews re
                        JOIN restaurant r ON r.restaurantID = re.restaurantID
                        WHERE re.customerID = %s
                    """
            cursor.execute(query, (self.current_user.customer_id,))
            rows = cursor.fetchall()

            names = []
            for row in rows:
                self.my_reviews_map[row['name']] = row
                names.append(row['name'])

            self.my_reviews_combo['values'] = names
            if not names:
                messagebox.showinfo("Info", "You haven't written any reviews yet.")

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # get data needed to edit
    def load_review_for_editing(self, event):
        res_name = self.my_reviews_combo.get()
        data = self.my_reviews_map.get(res_name)

        if data:
            self.current_review_id = data['reviewID']

            self.edit_rating_combo.config(state = "readonly")
            self.edit_content_entry.config(state = "normal")

            # Fill Data
            self.edit_rating_combo.set(data['rating'])
            self.edit_content_entry.delete("1.0", tk.END)
            self.edit_content_entry.insert("1.0", data['reviewContent'])

    # update the review with the new information
    def update_review_action(self):
        try:
            new_rating = self.edit_rating_combo.get()
            new_content = self.edit_content_entry.get("1.0", tk.END).strip()

            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor()

            query = "UPDATE reviews SET rating = %s, reviewContent = %s WHERE reviewID = %s"
            cursor.execute(query, (new_rating, new_content, self.current_review_id))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Review Updated Successfully!")
            self.show_dashboard()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # confirm and delete a review
    def delete_review_action(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure? This will also delete any owner replies.")
        if confirm:
            try:
                conn = db_app.get_DB_CONFIG_connection()
                cursor = conn.cursor()

                cursor.execute("DELETE FROM replies WHERE reviewID = %s", (self.current_review_id,))

                # Delete the review
                cursor.execute("DELETE FROM reviews WHERE reviewID = %s", (self.current_review_id,))

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Deleted", "Review has been removed.")
                self.show_dashboard()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    # set up edit review form
    def show_edit_review_form(self, review_id):
        self.clear_window()

        self.current_review_id = review_id

        tk.Label(self.root, text = "Edit Your Review", font = ("Arial", 16, "bold")).pack(pady = 20)

        current_data = None
        try:
            conn = db_app.get_DB_CONFIG_connection()
            cursor = conn.cursor(dictionary = True)
            query = """SELECT r.name, re.rating, re.reviewContent 
                       FROM reviews re JOIN restaurant r ON r.restaurantID = re.restaurantID 
                       WHERE re.reviewID = %s"""
            cursor.execute(query, (review_id,))
            current_data = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.show_my_reviews_screen()
            return

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Restaurant:", font=("Arial", 10, "bold")).grid(row=0, column=0,
                                                                                               sticky="e", pady=5)
        tk.Label(form_frame, text=current_data['name'], font=("Arial", 10)).grid(row=0, column=1,
                                                                                              sticky="w", padx=10)

        # Rating
        tk.Label(form_frame, text = "Rating:").grid(row = 1, column = 0, sticky = "e", pady = 5)
        self.edit_rating_combo = ttk.Combobox(form_frame, values = [1, 2, 3, 4, 5], state = "readonly", width = 5)
        self.edit_rating_combo.set(current_data['rating'])
        self.edit_rating_combo.grid(row = 1, column = 1, sticky = "w", padx = 10)

        # Content
        tk.Label(form_frame, text = "Review:").grid(row = 2, column = 0, sticky = "ne", pady = 5)
        self.edit_content_entry = tk.Text(form_frame, height = 8, width = 50)
        self.edit_content_entry.insert("1.0", current_data['reviewContent'])
        self.edit_content_entry.grid(row = 2, column = 1, padx = 10, pady = 5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text = "Save Changes", command = self.update_review_action, width = 15).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Delete Review", command = self.delete_review_action,
                  bg = "#F44336", fg = "white", width = 15).pack(side = tk.LEFT, padx = 10)

        tk.Button(btn_frame, text = "Cancel", command = self.show_my_reviews_screen).pack(side = tk.LEFT, padx = 10)

    # set up search reviews page
    def show_search_reviews_screen(self, auto_search_term = None):
        self.clear_window()

        tk.Label(self.root, text = "Search Reviews by Restaurant",
                 font=("Arial", 16)).pack(pady = 10)

        search_frame = tk.Frame(self.root)
        search_frame.pack(pady = 10)

        tk.Label(search_frame, text = "Restaurant Name:").pack(side = tk.LEFT, padx = 5)

        self.search_combo = ttk.Combobox(search_frame, width = 30)
        self.search_combo.pack(side = tk.LEFT, padx = 5)
        res_names = self.get_all_restaurant_names()
        self.search_combo['values'] = res_names

        if auto_search_term:
            self.search_combo.set(auto_search_term)

        def perform_search():

            # Clear any previous results
            for i in tree.get_children(): tree.delete(i)

            # Name from dropdown
            r_name = self.search_combo.get().strip()
            if not r_name: return

            try:
                conn = db_app.get_DB_CONFIG_connection()
                cursor = conn.cursor()

                query = """SELECT b.name, a.rating, a.reviewContent, c.replyContent,
                           (SELECT ROUND(AVG(rating), 1) FROM reviews WHERE restaurantID = b.restaurantID)
                           FROM reviews a JOIN restaurant b ON b.restaurantID = a.restaurantID
                           LEFT JOIN replies c ON a.reviewID = c.reviewID
                           WHERE LOWER(b.name) LIKE %s ORDER BY a.reviewDate DESC"""

                search_term = f"%{r_name.lower()}%"

                cursor.execute(query, (search_term,))
                results = cursor.fetchall()

                if not results:
                    messagebox.showinfo("Info", f"No reviews found for '{r_name}'.")

                for row in results:
                    r_name_db = row[0]
                    user_rating = row[1]
                    content = row[2]
                    reply = row[3] if row[3] else "No Reply"
                    avg_rating = row[4]

                    # Insert with the new Average Rating in the correct column position
                    tree.insert('', tk.END, values = (r_name_db, user_rating, avg_rating, content, reply))
                cursor.close()
                conn.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error searching: {err}")

        def sort_treeview(tree, col, reverse):
            data_list = [(tree.set(k, col), k) for k in tree.get_children('')]

            try:
                data_list.sort(key = lambda t: float(t[0]), reverse = reverse)
            except ValueError:
                data_list.sort(reverse = reverse)

            for index, (val, k) in enumerate(data_list):
                tree.move(k, '', index)

            tree.heading(col, command = lambda: sort_treeview(tree, col, not reverse))

        cols = ('Restaurant', 'Rating', "Avg Rating", 'Review', 'Reply')
        tree = ttk.Treeview(self.root, columns = cols, show = 'headings', height = 10)

        for col in cols:
            tree.heading(col, text = col, command = lambda c = col: sort_treeview(tree, c, False))

            if col == 'Rating':
                tree.column(col, width = 50, anchor = 'center')
            elif col == 'Avg Rating':
                tree.column(col, width = 50, anchor = 'center')
            elif col == 'Restaurant':
                tree.column(col, width = 150)
            else:
                tree.column(col, width = 250)

        tree.pack(fill = tk.BOTH, expand = True, padx = 20)

        tk.Button(search_frame, text = "Search", command = perform_search).pack(side = tk.LEFT, padx = 10)

        # Back Button
        def go_back():
            if self.current_user:
                self.show_dashboard()
            else:
                self.show_login_screen()

        tk.Button(self.root, text = "Back", command = go_back).pack(pady = 10)

    # set up edit account screen
    def show_edit_account_screen(self):
        self.clear_window()

        tk.Label(self.root, text = "Edit Account Information", font = ("Arial", 16, "bold")).pack(pady = 20)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady = 10)

        self.account_entries = {}

        # Define fields and their current values
        fields = {
            "Username": self.current_user.username,
            "Password": self.current_user.password,
            "Email": self.current_user.email,
            "Full Name": self.current_user.full_name
        }

        for i, (label_text, value) in enumerate(fields.items()):
            tk.Label(form_frame, text = f"{label_text}:", font = ("Arial", 10, "bold")).grid(row = i, column = 0, sticky = "e", pady = 10, padx = 10)

            entry = tk.Entry(form_frame, width = 30)
            entry.insert(0, value)
            entry.grid(row = i, column = 1, pady = 10, padx = 10)

            self.account_entries[label_text] = entry

        def save_changes():
            new_user = self.account_entries["Username"].get().strip()
            new_pass = self.account_entries["Password"].get().strip()
            new_email = self.account_entries["Email"].get().strip()
            new_name = self.account_entries["Full Name"].get().strip()

            if not all([new_user, new_pass, new_email, new_name]):
                messagebox.showwarning("Warning", "All fields must be filled.")
                return

            if self.current_user.update_account(new_user, new_pass, new_email, new_name):
                messagebox.showinfo("Success", "Account details updated successfully!")

                # Refresh dashboard title with new name
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Update failed. Username or Email might be taken.")

        def delete_account():
            confirm = messagebox.askyesno("Confirm Delete",
                                          "Are you sure you want to delete your account? This action is irreversible.")
            if confirm:
                if self.current_user.delete_account():
                    messagebox.showinfo("Deleted", "Your account has been deleted.")
                    self.current_user = None
                    self.show_login_screen()
                else:
                    messagebox.showerror("Error", "Failed to delete account.")

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text = "Save Changes", command = save_changes, width = 15).pack(
            side = tk.LEFT, padx = 10)
        tk.Button(btn_frame, text = "Cancel", command = self.show_dashboard).pack(side = tk.LEFT, padx = 10)
        tk.Button(btn_frame, text = "Delete Account", command = delete_account, fg = "red").pack(side = tk.LEFT, padx = 10)


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantGUI(root)
    root.mainloop()

