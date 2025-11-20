import mysql.connector


DB_CONFIG_PARAMS = {
    "host": "localhost",
    "user": "root",
    "password": "10473Cvusd:)",
    "port": "3306",
    "database": "cs3560"
}


try:
    DB_CONFIG = mysql.connector.connect(**DB_CONFIG_PARAMS)
except mysql.connector.Error as err:
    print(f"FATAL: Could not connect to database. {err}")
    DB_CONFIG = None

# --- STEP 3: Define the Connection Function for OOP Classes ---
# This function is used inside the `with` blocks in your class methods.
def get_DB_CONFIG_connection(): 
    # Returns a NEW connection using the dictionary
    return mysql.connector.connect(**DB_CONFIG_PARAMS)

current_username = None # Keep this if needed for legacy functions
# --- Review Class --- 
class Review:
    def __init__(self, review_id: int, restaurant_id: int, user_id: int, rating: float, review_content: str, review_date: str):
        self.review_id: int = review_id             # Primary key    
        self.restaurant_id: int = restaurant_id     # Foreign key to Restaurant
        self.user_id: int = user_id                 # Foreign key to User
        self.rating: float = rating                 # Rating out of 5
        self.review_content: str = review_content   # Text content of the review
        self.review_date: str = review_date         # Date when the review was posted

        def __str__(self) -> str: # String representation of the Review object
            return f"Review #{self.review_id} - Rating: {self.rating}/5"
        

    def save(self):
        """Saves the review to the database."""
        if not all([self.restaurant_id, self.user_id, self.rating, self.review_content]):
            print("Error: All review fields must be provided.")
            return False
        
        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor()

                query = """
                    INSERT INTO reviews (restaurantID, customerID, rating, reviewContent, reviewDate)
                    VALUES (%s, %s, %s, %s, CURDATE())
                """
                my_cursor.execute(query, (self.restaurant_id, self.user_id, self.rating, self.review_content))
                DB_CONFIG.commit()

                self.review_id = my_cursor.lastrowid  # Get the auto-generated reviewID

                print(f"Review #{self.review_id} saved successfully.")
                my_cursor.close()
                return True
            
        except mysql.connector.Error as err:
            print(f"Data Error during review save: {err}")
            return False
        
        #Static method to search for reviews by restaurant name
    @staticmethod
    def searching_for_review():
        r_name = input("What restaurant would you like to search for?").strip()
        r_name_clean = r_name.replace(" ", "").lower()

        results = []

        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor()
                query = """
                    SELECT 
                        a.reviewID, b.name, a.rating, a.reviewContent, a.reviewDate, 
                        c.replyContent, c.replyDate
                    FROM reviews a
                    JOIN restaurant b ON b.restaurantID = a.restaurantID
                    LEFT JOIN replies c ON a.reviewID = c.reviewID
                    WHERE REPLACE(LOWER(b.name), ' ', '') = %s
                    ORDER BY a.reviewDate DESC
                """
                my_cursor.execute(query, (r_name_clean,))
                results = my_cursor.fetchall()
                my_cursor.close()

        except mysql.connector.Error as err:
            print(f"Data Error during review search: {err}")
            return
        
        if not results:
            print(f"\nNo reviews found for '{r_name}', try again :).")
            return
        
        print(f"\n--- Reviews for: {results [0][1]} ---") #restults[0][1] is restaurant name

        for (review_id, r_name, rating, review_message, review_date, reply_content, reply_date) in results:
            review_display = f"Restaurant Review: {reply_content} (on {reply_date.strftime('%Y-%m-%d')})" if reply_content else "Restaurant Reply: **None**"

            print(f"""
        **Review ID**: {review_id}
        Restaurant Name: {r_name}
        Rating: {rating}
        Review Message: {review_message}
        Review Date: {review_date.strftime('%Y-%m-%d')}
        {review_display}
-------------------------------
    """)
class Reply:

    def __init__(self, reply_id: int, review_id: int, user_id: int, reply_content: str, reply_date: str):
        self.reply_id: int = reply_id               #Will hold ID once saved to DB
        self.review_id: int = review_id             # Foreign key to Review
        self.user_id: int = user_id                 # Foreign key to User  
        self.reply_content: str = reply_content
        self.reply_date: str = reply_date

    def save(self):

        """
        Saves the reply to the database.
        If a reply for the given review_id already exists, it will not create a new one.

        """

        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor()


                # -- Step 1: Check if a reply already exists for the given review_id
                # This ensures that each review has at most one reply
                my_cursor.execute("SELECT replyID FROM replies WHERE reviewID = %s", (self.review_id,))
                if my_cursor.fetchone():
                    print(f" Error: A reply for reviewID {self.review_id} already exists. Cannot create duplicate replies.")
                    return False
                
                # -- Step 2: Insert the new reply into the database
                query = """
                    INSERT INTO replies (reviewID, ownerID, replyContent, replyDate)
                    VALUES (%s, %s, %s, CURDATE())
                """
                my_cursor.execute(query, (self.review_id, self.user_id, self.reply_content))
                DB_CONFIG.commit()

                self.reply_id = my_cursor.lastrowid  # Get the auto-generated replyID

                print(f" Owner Reply for reviewID {self.review_id} posted successfully.")
                my_cursor.close()
                return True
            
        except mysql.connector.Error as err:
            print(f"Data Error during reply save: {err}")
            return False
        

class Restaurant:

    def __init__(self, restaurant_id: int, name: str, email: str, address: str, phoneNumber: str, priceRange: str, operatingHours: str, cuisine: str, owner_id: int):
        self.restaurant_id: int = restaurant_id
        self.name: str = name
        self.email: str = email
        self.address: str = address
        self.phoneNumber: str = phoneNumber
        self.priceRange: str = priceRange
        self.operatingHours: str = operatingHours
        self.cuisine: str = cuisine
        self.owner_id: int = owner_id          # Foreign key to "Owner" User type

    def save(self):

        if not all([self.name, self.email, self.address, self.phoneNumber, self.priceRange, self.operatingHours, self.cuisine]):
            print("Error: All restaurant fields must be provided.")
            return False
        

        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor()

                query = """
                    INSERT INTO restaurant (name, email, address, phoneNumber, priceRange, operatingHours, cuisine, ownerID)
                if self.restaurant_id == 0:  # Checks if restaurant is a new or existing restaurant
                        
                    query = """
                        INSERT INTO restaurant (name, email, address, phoneNumber, priceRange, operatingHours, cuisine, ownerID)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    my_cursor.execute(query, (self.name, self.email, self.address, self.phoneNumber, self.priceRange, self.operatingHours, self.cuisine, self.owner_id))
                    DB_CONFIG.commit()

                    self.restaurant_id = my_cursor.lastrowid  # Get the auto-generated restaurantID

                    print(f"Restaurant '{self.name}' added successfully with ID {self.restaurant_id}.")
                    my_cursor.close()
                    return True
        
                else:  # Updates existing restaurant

                    query = """
                        UPDATE restaurant 
                        SET name = %s, email = %s, address = %s, phoneNumber = %s, priceRange = %s, operatingHours = %s, cuisine = %s
                        WHERE restaurantID = %s
                    """
                    my_cursor.execute(query, (self.name, self.email, self.address, self.phoneNumber, self.priceRange, self.operatingHours, self.cuisine, self.restaurant_id))
                    DB_CONFIG.commit()

                    print(f"Restaurant '{self.name}' successfully updated.")
                    my_cursor.close()
                    return True

        except mysql.connector.Error as err:
            print(f"Data Error during restaurant save: {err}")
            return False
        
    def update(self, fieldName, updatedValue):  # Takes the field and updates the value for that field.
        if fieldName == 'name':
            self.name = updatedValue
        elif fieldName == 'email':
            self.email = updatedValue
        elif fieldName == 'address':
            self.address = updatedValue
        elif fieldName == 'phoneNumber':
            self.phoneNumber = updatedValue
        elif fieldName == 'priceRange':
            self.priceRange = updatedValue
        elif fieldName == 'operatingHours':
            self.operatingHours = updatedValue
        elif fieldName == 'cuisine':
            self.cuisine = updatedValue
        else:
            raise ValueError(f"Field '{fieldName}' does not exist.")
        
        self.save()

    @staticmethod
    def get_restaurant_by_name(name: str):

        name_clean = name.replace(" ", "").lower()

        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor(dictionary=True)
                query = """
                    SELECT restaurantID, name, location, cuisine, address, ownerID 
                    FROM restaurant
                    WHERE REPLACE(LOWER(name), ' ', '') = %s
                """
                my_cursor.execute(query, (name_clean,))
                result = my_cursor.fetchone()
                my_cursor.close()

                if result:
                    return Restaurant(
                        restaurant_id=result['restaurantID'],
                        name=result['name'],
                        location=result['location'],
                        cuisine=result['cuisine'],
                        address=result['address'],
                        owner_id=result['ownerID']
                    )
                else:
                    print(f"No restaurant found with the name '{name}'.")
                    return None

        except mysql.connector.Error as err:
            print(f"Data Error during restaurant lookup: {err}")
            return None
    
class Owner:
    """Represents a restaurant owner user."""

    def __init__(self, owner_id: int, username: str, password: str, email: str, full_name: str):
        self.owner_id: int = owner_id           # Primary key
        self.username: str = username
        self.password: str = password           
        self.email: str = email
        self.full_name: str = full_name


    def register(self):
        """Registers the owner in the database."""
        if not all([self.username, self.password, self.email, self.full_name]):
            print("Error: All owner fields must be provided.")
            return False
        
        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor()

                my_cursor.execute("SELECT ownerID FROM Owners WHERE username = %s OR email = %s", (self.username, self.email))
                if my_cursor.fetchone():
                    print("Error: An owner with the given username or email already exists.")
                    return False

                query = """
                    INSERT INTO Owners (username, password, email, full_name)
                    VALUES (%s, %s, %s, %s)
                """
                #Execute the insert query
                my_cursor.execute(query, (self.username, self.password, self.email, self.full_name,))
                DB_CONFIG.commit()

                self.owner_id = my_cursor.lastrowid  # Get the auto-generated ownerID

                print(f"Owner '{self.username}' registered successfully with ID {self.owner_id}.")
                my_cursor.close()
                return True
        
        except mysql.connector.Error as err:
            print(f"Data Error during owner registration: {err}")
            return False
        

    @staticmethod
    def login(username: str, password: str):

        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor(dictionary=True)
                query = """
                    SELECT ownerID, username, email, full_name
                    FROM Owners
                    WHERE username = %s AND password = %s
                """
                
                my_cursor.execute(query, (username, password))
                result = my_cursor.fetchone()
                my_cursor.close()

                if result:
                    print(f"Welcome {result['full_name']}! You are now logged in as 'owner'.")
                    return Owner(
                        owner_id=result['ownerID'],
                        username=result['username'],
                        password=password,
                        email=result['email'],
                        full_name=result['full_name']
                    )
                else:
                    print("Invalid username or password.")
                    return None
        except mysql.connector.Error as err:
            print(f"Data Error during owner login: {err}")
            return None
            
class Customer:

    def __init__(self, customer_id: int, username: str, password: str, email: str, full_name: str):
        self.customer_id: int = customer_id         # Primary key
        self.username: str = username
        self.password: str = password           
        self.email: str = email
        self.full_name: str = full_name

    def register(self):
        """Registers the customer in the database."""
        if not all([self.username, self.password, self.email, self.full_name]):
            print("Error: All customer fields must be provided.")
            return False
        
        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor()

                my_cursor.execute("SELECT customerID FROM Customers WHERE username = %s OR email = %s", (self.username, self.email))
                if my_cursor.fetchone():
                    print("Error: A customer with the given username or email already exists.")
                    return False

                query = """
                    INSERT INTO Customers (username, password, email, full_name)
                    VALUES (%s, %s, %s, %s)
                """
                my_cursor.execute(query, (self.username, self.password, self.email, self.full_name))
                DB_CONFIG.commit()

                self.customer_id = my_cursor.lastrowid  # Get the auto-generated customerID

                print(f"Customer '{self.username}' registered successfully with ID {self.customer_id}.")
                my_cursor.close()
                return True
        
        except mysql.connector.Error as err:
            print(f"Data Error during customer registration: {err}")
            return False
        
    @staticmethod
    def login(username: str, password: str):
        """Logs in the customer with the given credentials."""

        try:
            with get_DB_CONFIG_connection() as DB_CONFIG:
                my_cursor = DB_CONFIG.cursor(dictionary=True)
                query = """
                    SELECT customerID, username, email, full_name
                    FROM Customers
                    WHERE username = %s AND password = %s
                """
                
                my_cursor.execute(query, (username, password))
                result = my_cursor.fetchone()
                my_cursor.close()

                if result:
                    print(f"Welcome {result['full_name']}! You are now logged in as 'customer'.")
                    return Customer(
                        customer_id=result['customerID'],
                        username=result['username'],
                        password=password,
                        email=result['email'],
                        full_name=result['full_name']
                    )
                else:
                    print("Invalid username or password.")
                    return None
                
        except mysql.connector.Error as err:
            print(f"Data Error during customer login: {err}")
            return None


#Remnants of code from group member below
#The below function adds a new user to the database
#used when we have a new user creating an account
def registration_workflow():
    print("Lets create an account!")
    try:
        type_of_user = int(input("""***After creating an account, you will be redirected to the home page to log in***
    Are you a [1] restaurant owner or a [2] customer: 
    """))

    except ValueError:
        print("Invalid input, please enter 1 or 2.")
        return
    
    username = input("Enter your username: ").strip()
    password = input("Enter your account password: ").strip()
    full_name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()

    if type_of_user == 1:
        #Uses the Owner class to register a new restaurant owner
        new_owner = Owner(owner_id=0, username=username, password=password, email=email, full_name=full_name)
        new_owner.register()

        try:
            print("\n Do you want to add a restaurant now?")
            add_restaurant_choice = int(input("[1] Yes   [2] No: ").strip())
        
        except ValueError:
            print("Invalid input, please enter 1 or 2.")
            return
        
        if add_restaurant_choice == 1:
            restaurant_name = input("Enter the restaurant name: ").strip()
            restaurant_email = input("Enter the restaurant email: ").strip()
            restaurant_address = input("Enter the restaurant address: ").strip()
            restaurant_phoneNumber = input("Enter the restaurant phone number: ").strip()
            restaurant_priceRange = input("Enter the restaurant price range: (Using $ from 1 to 5 dollar signs) ").strip()
            restaurant_operatingHours = input("Enter the restaurant operating hours: ").strip()
            restaurant_cuisine = input("Enter the restaurant cuisine type: ").strip()


            new_restaurant = Restaurant(
                restaurant_id=0,
                name=restaurant_name,
                email=restaurant_email,
                phoneNumber=restaurant_phoneNumber,
                priceRange=restaurant_priceRange,
                operatingHours=restaurant_operatingHours,
                cuisine=restaurant_cuisine,
                address=restaurant_address,
                owner_id=new_owner.owner_id
            )

            new_restaurant.save()

        if add_restaurant_choice == 2:
            print("Note: You can add a restaurant later from your owner dashboard.")
   
    elif type_of_user == 2:
       #Uses the Customer class to register a new customer
        new_customer = Customer(customer_id=0, username=username, password=password, email=email, full_name=full_name)
        new_customer.register()

    else:
        print("Invalid input, please enter 1 or 2.")
        return

#The function below imitates owner dashboard functions
#Used when owner wants to create, update, or delete a restaurant
def modify_restaurant(owner_id):
    mycursor = DB_CONFIG.cursor()
    while True:
        try:
            print("\nWhat would you like to do?")
            print("[1] Create new restaurant")
            print("[2] Update a restaurant")
            print("[3] Delete a restaurant")
            print("[4] Quit")
            choice = input("Enter choice: ").strip()

        except ValueError:
            print("Invalid input, please enter 1, 2, 3,or 4.")
            return

        if choice == '4':
            print("Exiting Owner Dashboard.")
            break

        if choice == '1':  # Create a new restaurant
            print(f"Please enter restaurant information: ")
            restaurant_name = input("Enter the restaurant name: ").strip()
            restaurant_email = input("Enter the restaurant email: ").strip()
            restaurant_address = input("Enter the restaurant address: ").strip()
            restaurant_phoneNumber = input("Enter the restaurant phone number: ").strip()
            restaurant_priceRange = input("Enter the restaurant price range: (Using $ from 1 to 5 dollar signs) ").strip()
            restaurant_operatingHours = input("Enter the restaurant operating hours: ").strip()
            restaurant_cuisine = input("Enter the restaurant cuisine type: ").strip()

            new_restaurant = Restaurant(
                restaurant_id=0,
                name=restaurant_name,
                email=restaurant_email,
                phoneNumber=restaurant_phoneNumber,
                priceRange=restaurant_priceRange,
                operatingHours=restaurant_operatingHours,
                cuisine=restaurant_cuisine,
                address=restaurant_address,
                owner_id=owner_id
            )

            new_restaurant.save()
            continue

        elif choice == '2':  # Update restaurant information
            query = "SELECT * FROM restaurant WHERE ownerID = %s"
            mycursor.execute(query, (owner_id,))
            restaurants = mycursor.fetchall()

            if restaurants:
                print(f"Your restaurants: ")
                for i, restaurant in enumerate(restaurants, 1):
                    print(f"{i}. {restaurant[1]}")

                try:
                    choice = int(input("Enter the number of the restaurant you want to update: ")) - 1

                    if 0 <= choice < len(restaurants):
                            restaurant_info = restaurants[choice]

                    while True:
                        selected_restaurant = Restaurant(
                            restaurant_id=restaurant_info[0],
                            name=restaurant_info[1],
                            email=restaurant_info[2],
                            address=restaurant_info[3],
                            phoneNumber=restaurant_info[4],
                            priceRange=restaurant_info[5],
                            operatingHours=restaurant_info[6],
                            cuisine=restaurant_info[7],
                            owner_id=restaurant_info[8]
                        )
                        
                        fieldName = input("What field would you like to update?: ").strip()
                        updatedValue = input("Enter the updated information: ").strip()

                        selected_restaurant.update(fieldName, updatedValue)

                        another = input("""Update another field? 
                        [1] Yes
                        [2] No""").strip().lower()
                        if another == '2':
                            break

                except ValueError:
                    print("Please enter a valid number")
                
            else:
                print("You don't own any restaurants.")
                continue

        elif choice == '3':  # Delete restaurant from database
            query = "SELECT * FROM restaurant WHERE ownerID = %s"
            mycursor.execute(query, (owner_id,))
            restaurants = mycursor.fetchall()

            if restaurants:
                print("Your restaurants: ")
                for i, restaurant in enumerate(restaurants, 1):
                    print(f"{i}. {restaurant[1]}")
                try:
                    choice = int(input("Enter the number of the restaurant you want to delete: ")) - 1

                    if 0 <= choice < len(restaurants):
                        restaurant_id = restaurants[choice][0]
                        restaurant_name = restaurants[choice][1]

                        confirmation = input(f"""Are you sure you want to delete restaurant {restaurant_name}? 
                        [1] Yes
                        [2] No""").lower()
                    
                        if confirmation == '1':
                            mycursor.execute(f"DELETE FROM restaurant WHERE restaurantID = %s AND ownerID = %s", (restaurant_id, owner_id))
                            DB_CONFIG.commit()
                            print(f"Restaurant {restaurant_name} deleted")
                        else:
                            print(f"Restaurant {restaurant_name} not deleted")

                except ValueError:
                    print("Please enter a valid number")

            else:
                print("You don't own any restaurants.")
                continue

    mycursor.close()

#the below function is called when a user wants to delete their account
#deletes account from the database
def delete_account():
    username = input("Enter your username: ").strip()
    password = input("Enter your account password: ").strip()
    
    mycursor = DB_CONFIG.cursor()

    mycursor.execute("SELECT ownerID FROM Owners WHERE username = %s AND password = %s", (username, password))
    user_data = mycursor.fetchone()
    table_name = "Owners"
    if not user_data:
        # 2. Check Customers
        mycursor.execute("SELECT customerID FROM Customers WHERE username = %s AND password = %s", (username, password))
        user_data = mycursor.fetchone()
        table_name = "Customers"
    
    if user_data:
        confirmation = input("""Are you sure you want to delete this account? 
        [1] Yes
        [2] No""").lower()
        
        if confirmation == "1":
            # Execute deletion on the correct table
            mycursor.execute(f"DELETE FROM {table_name} WHERE username = %s", (username,))
            DB_CONFIG.commit()
            print("Account deleted")
        else:
            print("Account not deleted")
    else:
        print("Account not found")
        
    mycursor.close()

#this function is called when a user who is already logged in (through calling login function before this), wants to enter a new review
def adding_review_workflow(logged_in_customerid: int):
    print("\n--- Add a New Review ---")

    
    restaurant_name = input("Enter the restaurant name you reviewed: ").strip()

    restaurant_obj = Restaurant.get_restaurant_by_name(restaurant_name)

    if not restaurant_obj:
        print("Unfortunately the restaurant you entered is not partnered with our application.")
        return
    
    # Get rating from user
    try: 
        rating_input = input("Enter rating (1-5): ").strip()
        rating = float(rating_input)

        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return
        
    except ValueError:
        print("Invalid rating. Please enter a number between 1 and 5.")
        return
    

    #Get review content from user
    content = input("Write your review: ").strip()
    if not content:
        print("Review cannot be empty.")
        return
    
    print("\n--- Attempting to post your review... ---")

    #create Review object and save to database
    new_review = Review(
        review_id=None, # Will be set after saving to DB
        restaurant_id=restaurant_obj.restaurant_id,
        customer_id=logged_in_customerid,
        rating=rating,
        review_content=content,
        review_date=""  # Will be set to current date in the save method
    )

    if new_review.save():
        print(f"Your review for {restaurant_obj.name} has been posted.")
    else:
        print(" Review posting failed due to an error.")


#Updated function for restaurant owners to reply to reviews that incorporates the Reply class and its save method
#Below function is used when a restaurant owner logs in, and wants to see reviews, reply to them, or delete/ edit replies they entered in the past
def res_owner_reply_function(owner_id: int):

    print("\n--- Restaurant Owner Reply Console ---")
    print("Tip: Use this console to manage your restaurant's reviews and replies.\n")

    try:
        with get_DB_CONFIG_connection() as DB_CONFIG:
            mycursor = DB_CONFIG.cursor(dictionary=True)

            mycursor.execute("SELECT restaurantID, name FROM restaurant WHERE ownerID = %s", (owner_id,))
            ownedrestaurants = mycursor.fetchall()

            if not ownedrestaurants:
                print("You do not own any restaurants in our system.")
                return
            
            #If the owner owns multiple restaurants, list them
            #Ask which restaurant they want to manage
            if len(ownedrestaurants) > 1:
                print("You own multiple restaurants. Please select one to manage:")
                for i, res in enumerate(ownedrestaurants):
                    print(f"[{i+1}] {res['name']} (ID: {res['restaurantID']})")

                choice_input = input("Enter the number of the restaurant you want to manage: ").strip()

                try:
                    res_index =  int(choice_input) - 1
                    if 0 <= res_index < len(ownedrestaurants):
                        selected_restaurant = ownedrestaurants[res_index]
                    else:
                        print("Invalid selection.")
                        return
                except ValueError:
                    print("Invalid input.")
                    return
            else:
                selected_restaurant = ownedrestaurants[0]

                print(f"Managing reviews for restaurant: {selected_restaurant['name']} (ID: {selected_restaurant['restaurantID']})")

            # 2. ----  Restaurant Management Menu Loop  ----
            while True:
                print("\nWhat would you like to do?")
                print("[1] View reviews with NO reply (and add replies)")
                print("[2] View reviews WITH a reply (and edit/delete replies)")
                print("[3] Quit")
                choice_main = input("Enter choice: ").strip()

                if choice_main == '3':
                    print("Exiting Restaurant Owner Reply Console.")
                    break
                
                if choice_main == '1':
                    #View unreplied reviews and add replies
                    mycursor.execute("""
                        SELECT a.reviewID, a.reviewDate, a.rating, a.reviewContent
                        FROM reviews a
                        LEFT JOIN replies c ON c.reviewID = a.reviewID
                        WHERE a.restaurantID = %s AND c.reviewID IS NULL
                        ORDER BY a.reviewDate
                    """, (selected_restaurant['restaurantID'],))
                    pending = mycursor.fetchall()

                    if not pending:
                        print(f"✅ No unreplied reviews currently found for {selected_restaurant['name']}.")
                        continue # Go back to the main owner menu
                    
                    print(f"\n--- Unreplied Reviews for {selected_restaurant['name']} ---")
                    valid_ids = set() # Needed to validate user input later

                    # Loop through and display the reviews
                    for row in pending:
                        # Since the cursor is set to dictionary=True in this function:
                        valid_ids.add(row['reviewID'])
                        print(f"""
                    Review ID: {row['reviewID']}
                    Date:      {row['reviewDate'].strftime('%Y-%m-%d')}
                    Rating:    {row['rating']}
                    Content:   {row['reviewContent']}
                    """)
                        print("-" * 50)

                    while True:

                        choice = input("Enter a reviewID to reply to (or '0' to go back): ").strip()
                        if choice == '0':
                            break

                        review_id = int(choice)
                        reply_text = input("Enter your reply: ").strip()

                        if not reply_text:
                            print("Empty reply skipped.")
                            continue

                        #Create a Reply object and save it to the database
                        new_reply = Reply(
                            reply_id=None,  # Will be set after saving to DB
                            review_id=review_id,
                            user_id=owner_id,
                            reply_content=reply_text,
                            reply_date=None  # Will be set to current date in the save method
                        )

                        new_reply.save()

                elif choice_main == '2':
                #View replied reviews and edit/delete replies
                    mycursor.execute("""
                        SELECT a.reviewID, a.reviewDate, a.rating, a.reviewContent,
                            c.replyContent, c.replyDate
                        FROM reviews a
                        JOIN replies c ON c.reviewID = a.reviewID
                        WHERE a.restaurantID = %s AND c.ownerID = %s
                        ORDER BY a.reviewDate
                    """, (selected_restaurant['restaurantID'], owner_id)) # Corrected to use owner_id
                    
                    replied = mycursor.fetchall()

                    if not replied:
                        print("No reviews with replies found.")
                        continue

                    print(f"\n--- Replied Reviews for {selected_restaurant['name']} ---")

                    replied_ids = set()

                    for row in replied:
                        replied_ids.add(row['reviewID'])
                        print(f"""
                    Review ID: {row['reviewID']}
                    Date:      {row['reviewDate'].strftime('%Y-%m-%d')}
                    Rating:    {row['rating']}
                    Review:    {row['reviewContent']}
                    Reply:     {row['replyContent']}
                    Replied:   {row['replyDate'].strftime('%Y-%m-%d')}
                    """)
                        print("_" * 50)
                    while True:
                        print("[1] Edit a reply   [2] Delete a reply   [3] Back")
                        action = input("Choose action: ").strip()

                        if action == '3':
                            break
                        
                        if action not in ['1', '2']:
                            print("Invalid action. Please choose 1, 2, or 3.")
                            continue

                        rid = input("Enter the reviewID to modify: ").strip()

                        if not rid.isdigit():
                            print("Please enter a numeric reviewID.")
                            continue

                        rid = int(rid)

                        if rid not in replied_ids:
                            print("reviewID not in the list above.")
                            continue

                        if action == '1':
                            new_text = input("Enter the new reply text: ").strip()
                            if not new_text:
                                print("Empty reply update skipped.")
                                continue

                            mycursor.execute("""
                                UPDATE replies
                                    SET replyContent = %s, replyDate = CURDATE()
                                    WHERE reviewID = %s AND ownerID = %s
                            """, (new_text, rid, owner_id))
                            DB_CONFIG.commit()
                            print("Reply updated successfully.")

                        elif action == '2':
                            # ... (Delete logic) ...
                            
                            mycursor.execute("""
                                DELETE FROM replies
                                    WHERE reviewID = %s AND ownerID = %s
                            """, (rid, owner_id))
                            DB_CONFIG.commit()
                            print("Reply deleted successfully.")

    except mysql.connector.Error as err:
        print(f"Data Error during restaurant owner reply management: {err}")
    finally:
        if mycursor:
            mycursor.close()
  

#just testing here, can delete
#user_type = login()
#if current_username:
#    adding_review(current_username)
#else:
#    print("No user is logged in.")


#call this function whenever you are tesing things out and want to make sure all the tables are correct
#or use this whenever you want to see the tables
def print_all_tables():
    """Fetches and prints all rows from the five core tables (for debugging purposes)."""
    
    # Check if the global connection object is available
    if not DB_CONFIG:
        print("Cannot print tables due to database connection error.")
        return

    mycursor = DB_CONFIG.cursor()
    
    # Updated list of tables to match your final schema
    tables = ["Owners", "Customers", "restaurant", "reviews", "replies"]
    
    for table in tables:
        try:
            # Note: We must use the specific ID name for the foreign key display logic
            # However, for simple printing, SELECT * is easiest.
            mycursor.execute(f"SELECT * FROM {table}") 
            results = mycursor.fetchall()
            
            print("\n")
            print(f"--- {table.upper()} TABLE: ---")
            
            if not results:
                print("--- (EMPTY) ---")
                continue
            
            # Print column headers first (optional, but helpful)
            # headers = [i[0] for i in mycursor.description]
            # print(headers)
            
            for row in results:
                print(row)
                
        except mysql.connector.Error as err:
            print(f"Error reading table {table}: {err}")

    mycursor.close()

# The procedural call that runs on script load should be removed or commented out for the main app loop
# print_all_tables()
print_all_tables()


# --- Global State ---
current_user = None 

# --- Login Workflow (REVISED) ---
def login_workflow():
    global current_user
    
    if current_user:
        # We can determine the type here using isinstance()
        user_class = type(current_user).__name__
        print(f"You are already logged in as {current_user.username} ({user_class}).")
        return

    user_type_input = input("Log in as [1] Owner or [2] Customer: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    logged_in_object = None
    
    if user_type_input == '1':
        logged_in_object = Owner.login(username, password)
    elif user_type_input == '2':
        logged_in_object = Customer.login(username, password)
    else:
        print("Invalid choice for user type.")
        return
    
    if logged_in_object:
        current_user = logged_in_object # Set the object regardless of type

# --- Logout Workflow (Cleaned) ---
def logout_workflow():
    global current_user
    if current_user:
        user_class = type(current_user).__name__
        print(f"👋 {current_user.username} successfully logged out.")
        current_user = None
    else:
        print("No user is currently logged in.")

# ====================================================================
# D. MAIN MENU
# ====================================================================

def main_menu():
    global current_user

    while True:
        status = f"{current_user.username} ({type(current_user).__name__})" if current_user else "Not Logged In"
        print(f"\n===== Restaurant Review System | Status: {status} =====")
        print("[1] Search Reviews (General View)")
        
        # Determine available actions based on login status and object type
        is_owner = isinstance(current_user, Owner)
        is_customer = isinstance(current_user, Customer)
        
        if not current_user:
            print("[2] Login")
            print("[3] Register New Account")
            print("[6] Delete Account")
        else:
            if is_customer:
                print("[4] Post New Review")
            
            if is_owner:
                print("[5] Owner Console (Manage Replies)")
                print("[7] Owner Dashboard")
                
            print("[9] Logout")
            
        print("[0] Exit System")
        print("[*] Print All Tables (DEBUG)")

        choice = input("Enter your choice: ").strip()
        
        # --- Handle Choices ---
        if choice == '1':
            Review.searching_for_review()
        
        elif choice == '2' and not current_user:
            login_workflow()
        
        elif choice == '3' and not current_user:
            registration_workflow()
            
        elif choice == '4' and is_customer:
            # We now safely access the user's ID via the object's attribute 
            logged_in_id = current_user.customer_id 
            adding_review_workflow(logged_in_id) 

        elif choice == '5' and is_owner:
            logged_in_id = current_user.owner_id
            res_owner_reply_function(logged_in_id)

        elif choice == '6' and not current_user:
            delete_account()

        elif choice == '7' and is_owner:
            logged_in_id = current_user.owner_id
            modify_restaurant(logged_in_id)


        elif choice == '9' and current_user:
            logout_workflow()
        
        elif choice == '*':
            print_all_tables()
            
        elif choice == '0':
            print("Shutting down. Goodbye!")
            break
            
        else:
            print("Invalid choice or action not available.")

            
# --- Final Execution Block ---
if __name__ == "__main__":
    if DB_CONFIG: 
        main_menu()
    else:
        print("Application cannot start due to initial database connection error.")