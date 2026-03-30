from models.user import User


class Customer(User):
    """
    Customer class - inherits from User.
    Handles searching providers, booking services, and giving reviews.
    """

    def __init__(self, user_id, name, email, password, phone, address):
        super().__init__(user_id, name, email, password, phone, role="customer")
        self.__address = address
        self.__booking_history = []
        self.__reviews_given = []

    # ---- Getters ----
    def get_address(self):
        return self.__address

    def get_booking_history(self):
        return self.__booking_history

    def get_reviews_given(self):
        return self.__reviews_given

    # ---- Setters ----
    def set_address(self, address):
        if address and len(address) >= 3:
            self.__address = address
            return True
        return False

    # ---- Core Methods ----
    def search_providers(self, provider_list, service_type):
        """
        Search for service providers by service type.
        Returns list of matching providers.
        """
        results = []
        for provider in provider_list:
            profile = provider.get_profile()
            if profile is not None:
                if profile.get_service_type().lower() == service_type.lower():
                    results.append(provider)
        return results

    def book_service(self, booking):
        """Add a booking to customer's history"""
        self.__booking_history.append(booking)
        return booking

    def cancel_booking(self, booking_id):
        """Cancel a pending booking"""
        for booking in self.__booking_history:
            if booking.get_booking_id() == booking_id:
                if booking.get_status() == "pending":
                    booking.set_status("cancelled")
                    return True
        return False

    def give_review(self, review):
        """Submit a review for a completed service"""
        self.__reviews_given.append(review)
        return review

    def get_booking_by_id(self, booking_id):
        """Find a specific booking by ID"""
        for booking in self.__booking_history:
            if booking.get_booking_id() == booking_id:
                return booking
        return None

    # ---- Display ----
    def display_info(self):
        """Return customer info as dictionary"""
        info = super().display_info()
        info["Address"] = self.__address
        info["Total Bookings"] = len(self.__booking_history)
        info["Reviews Given"] = len(self.__reviews_given)
        return info

    def __str__(self):
        return f"Customer({self.get_name()}, {self.get_email()})"