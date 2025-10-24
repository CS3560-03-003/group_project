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
