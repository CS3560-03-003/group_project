from typing import List, Dict, Union

class User:
    def __init__(self, user_id: int, username: str, password: str, name: str, email: str, location: str, join_date: str, user_type: str):
        self.user_id: int = user_id
        self.username: str = username
        self.password: str = password
        self.name: str = name
        self.email: str = email
        self.location: str = location
        self.join_date: str = join_date
        self.user_type: str = user_type         # Customer or Owner

class Restaurant:
    def __init__(self, restaurant_id: int, name: str, email: str, address: str, phone_number: str, price_range: str, operating_hours: str, cuisine: str, owner_id: int):
        self.restaurant_id: int = restaurant_id
        self.name: str = name
        self.email: str = email
        self.address: str = address
        self.phone_number: str = phone_number
        self.price_range: str = price_range
        self.operating_hours: str = operating_hours
        self.cuisine: str = cuisine
        self.owner_id: int = owner_id               # Foreign key to "Owner" User type

class Review:
    def __init__(self, review_id: int, date_posted: str, user_id: int, restaurant_id: int, rating: float, review_content: str, last_edited: str):
        self.review_id: int = review_id
        self.date_posted: str = date_posted
        self.user_id: int = user_id                 # Foreign key to User
        self.restaurant_id: int = restaurant_id     # Foreign key to Restaurant
        self.rating: float = rating
        self.review_content: str = review_content
        self.last_edited: str = last_edited

class Reply:
    def __init__(self, reply_id: int, review_id: int, user_id: int, reply_content: str, reply_date: str):
        self.reply_id: int = reply_id
        self.review_id: int = review_id             # Foreign key to Review
        self.user_id: int = user_id                 # Foreign key to User  
        self.reply_content: str = reply_content
        self.reply_date: str = reply_date



class ReviewSystemManager:
    # Initialize the Review System Database 
    def __init__(self):
        self.users: Dict[int, User] = {} 
        self.restaurants: Dict[int, Restaurant] = {}
        self.reviews: Dict[int, Review] = {}
        self.replies: Dict[int, Reply] = {}

        self.logged_in_user: User | None = None

        self._next_user_id = 1
        self._next_restaurant_id = 1
        self._next_review_id = 1
        self._next_reply_id = 1

    # User Management Methods

    # Register a new user
    def register_user(self, username: str, password: str, name: str, email: str, location: str, user_type: str) -> User | None:
        pass

    # Login an existing user
    def login_user(self, username: str, password: str) -> User | None:
        pass
        
    # Logout the currently logged-in user
    def logout_user(self) -> None:
        pass

    # Check if a user is currently logged in
    def is_user_logged_in(self) -> bool:
        pass
    
    # Delete the currently logged-in user's account
    def delete_user_account(self) -> bool:
        pass

    # Get the role of the currently logged-in user
    def get_user_role(self) -> str | None:
        pass

    # Search Restaurants
    def search_restaurants(self, query: str) -> List[Restaurant]:
        pass

    # Review Management Methods

    # Add a new review for a restaurant
    def add_review(self, restaurant_id: int, rating: float, content: str) -> Review | None:
        pass

    # Edit an existing review
    def get_reviews_for_my_restaurants(self) -> Dict[Restaurant, List[Union[Review, Reply]]]:
        pass
    
    # Helper method to get reply by review ID
    def _get_reply_by_review_id(self, review_id: int) -> Reply | None:
        pass

    # Validate if the logged-in user is the owner of the restaurant for a given review
    def _validate_owner_access(self, review_id: int) -> bool:
        pass

    # Add, Edit, Delete Reply Methods
    def add_reply(self, review_id: int, content: str) -> Reply | None:
        pass

    def edit_reply(self, review_id: int, new_content: str) -> bool:
        pass

    def delete_reply(self, review_id: int) -> bool:
        pass

