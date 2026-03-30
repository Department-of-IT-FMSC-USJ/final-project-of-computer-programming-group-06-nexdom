from datetime import datetime


class Review:
    """
    Represents a customer review for a service provider.
    Stores rating (1-5), review text, and related info.
    """

    _next_id = 1

    def __init__(self, booking_id, customer_id, customer_name,
                 provider_id, provider_name, rating, review_text,
                 service_type, review_id=None):

        if review_id:
            self.__review_id = review_id
        else:
            self.__review_id = Review._next_id
            Review._next_id += 1

        self.__booking_id = booking_id
        self.__customer_id = customer_id
        self.__customer_name = customer_name
        self.__provider_id = provider_id
        self.__provider_name = provider_name
        self.__service_type = service_type
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Validate rating between 1 and 5
        if isinstance(rating, int) and 1 <= rating <= 5:
            self.__rating = rating
        else:
            self.__rating = 3

        self.__review_text = review_text

    # Getters
    def get_review_id(self):
        return self.__review_id

    def get_booking_id(self):
        return self.__booking_id

    def get_customer_id(self):
        return self.__customer_id

    def get_customer_name(self):
        return self.__customer_name

    def get_provider_id(self):
        return self.__provider_id

    def get_provider_name(self):
        return self.__provider_name

    def get_rating(self):
        return self.__rating

    def get_review_text(self):
        return self.__review_text

    def get_service_type(self):
        return self.__service_type

    def get_created_at(self):
        return self.__created_at

    def to_dict(self):
        """Return review as dictionary"""
        return {
            "Review ID": self.__review_id,
            "Customer": self.__customer_name,
            "Provider": self.__provider_name,
            "Rating": self.__rating,
            "Review": self.__review_text,
            "Service": self.__service_type,
            "Date": self.__created_at
        }

    def __str__(self):
        stars = "⭐" * self.__rating
        return f"Review #{self.__review_id} | {stars} | '{self.__review_text[:30]}...'"