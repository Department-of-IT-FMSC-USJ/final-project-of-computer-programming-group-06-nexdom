from models.user import User


class ProviderProfile:
    """
    Service Provider's professional profile.
    Contains service details, experience, rates, and availability.
    """

    def __init__(self, user_id, service_type, experience,
                 hourly_rate, location, description):
        self.__user_id = user_id
        self.__service_type = service_type
        self.__experience = experience
        self.__hourly_rate = hourly_rate
        self.__location = location
        self.__description = description
        self.__is_available = True

    # Getters
    def get_user_id(self):
        return self.__user_id

    def get_service_type(self):
        return self.__service_type

    def get_experience(self):
        return self.__experience

    def get_hourly_rate(self):
        return self.__hourly_rate

    def get_location(self):
        return self.__location

    def get_description(self):
        return self.__description

    def is_available(self):
        return self.__is_available

    # Setters
    def set_service_type(self, service_type):
        self.__service_type = service_type

    def set_experience(self, experience):
        if experience >= 0:
            self.__experience = experience

    def set_hourly_rate(self, rate):
        if rate > 0:
            self.__hourly_rate = rate

    def set_location(self, location):
        self.__location = location

    def set_description(self, description):
        self.__description = description

    def set_availability(self, status):
        self.__is_available = status

    def to_dict(self):
        """Return profile as dictionary"""
        return {
            "Service Type": self.__service_type,
            "Experience": f"{self.__experience} years",
            "Hourly Rate": f"Rs.{self.__hourly_rate}",
            "Location": self.__location,
            "Description": self.__description,
            "Available": "Yes" if self.__is_available else "No"
        }


class ServiceProvider(User):
    """
    Service Provider class - inherits from User.
    Handles profile management, booking responses, and reviews.
    """

    def __init__(self, user_id, name, email, password, phone):
        super().__init__(user_id, name, email, password, phone, role="provider")
        self.__profile = None
        self.__booking_requests = []
        self.__reviews_received = []
        self.__total_earnings = 0.0

    # Getters
    def get_profile(self):
        return self.__profile

    def get_booking_requests(self):
        return self.__booking_requests

    def get_reviews_received(self):
        return self.__reviews_received

    def get_total_earnings(self):
        return self.__total_earnings

    def get_average_rating(self):
        """Calculate average rating from all reviews"""
        if not self.__reviews_received:
            return 0.0
        total = sum(r.get_rating() for r in self.__reviews_received)
        return round(total / len(self.__reviews_received), 1)

    # Profile Management
    def create_profile(self, service_type, experience, hourly_rate,
                       location, description):
        """Create provider profile"""
        self.__profile = ProviderProfile(
            user_id=self.get_user_id(),
            service_type=service_type,
            experience=experience,
            hourly_rate=hourly_rate,
            location=location,
            description=description
        )

    def update_profile(self, **kwargs):
        """Update specific profile fields using keyword arguments"""
        if self.__profile is None:
            return False

        if "service_type" in kwargs:
            self.__profile.set_service_type(kwargs["service_type"])
        if "experience" in kwargs:
            self.__profile.set_experience(kwargs["experience"])
        if "hourly_rate" in kwargs:
            self.__profile.set_hourly_rate(kwargs["hourly_rate"])
        if "location" in kwargs:
            self.__profile.set_location(kwargs["location"])
        if "description" in kwargs:
            self.__profile.set_description(kwargs["description"])
        if "availability" in kwargs:
            self.__profile.set_availability(kwargs["availability"])
        return True

    # Booking Management
    def receive_booking(self, booking):
        """Receive a new booking request"""
        self.__booking_requests.append(booking)

    def accept_booking(self, booking_id):
        """Accept a pending booking request"""
        for booking in self.__booking_requests:
            if booking.get_booking_id() == booking_id:
                if booking.get_status() == "pending":
                    booking.set_status("accepted")
                    return True
        return False

    def reject_booking(self, booking_id):
        """Reject a pending booking request"""
        for booking in self.__booking_requests:
            if booking.get_booking_id() == booking_id:
                if booking.get_status() == "pending":
                    booking.set_status("rejected")
                    return True
        return False

    def complete_booking(self, booking_id):
        """Mark an accepted booking as completed and add earnings"""
        for booking in self.__booking_requests:
            if booking.get_booking_id() == booking_id:
                if booking.get_status() == "accepted":
                    booking.set_status("completed")
                    if self.__profile:
                        self.__total_earnings += self.__profile.get_hourly_rate()
                    return True
        return False

    def get_bookings_by_status(self, status):
        """Get all bookings with a specific status"""
        return [b for b in self.__booking_requests
                if b.get_status() == status]

    # Review Management
    def receive_review(self, review):
        """Receive a review from a customer"""
        self.__reviews_received.append(review)

    def get_rating_distribution(self):
        """Get count of each rating (1-5)"""
        distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for review in self.__reviews_received:
            rating = review.get_rating()
            if rating in distribution:
                distribution[rating] += 1
        return distribution

    def display_info(self):
        """Return provider info as dictionary"""
        info = super().display_info()
        info["Rating"] = f"{self.get_average_rating()} ⭐"
        info["Total Reviews"] = len(self.__reviews_received)
        info["Total Earnings"] = f"Rs.{self.__total_earnings}"
        return info

    def __str__(self):
        return f"ServiceProvider({self.get_name()}, {self.get_average_rating()}⭐)"