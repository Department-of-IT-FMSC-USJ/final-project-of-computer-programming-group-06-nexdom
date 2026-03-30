from datetime import datetime


class Booking:
    """
    Represents a service booking between a customer and provider.
    Tracks booking details and status throughout the lifecycle.
    """

    _next_id = 1

    def __init__(self, customer_id, customer_name, provider_id,
                 provider_name, service_type, booking_date,
                 description, booking_id=None):

        if booking_id:
            self.__booking_id = booking_id
        else:
            self.__booking_id = Booking._next_id
            Booking._next_id += 1

        self.__customer_id = customer_id
        self.__customer_name = customer_name
        self.__provider_id = provider_id
        self.__provider_name = provider_name
        self.__service_type = service_type
        self.__booking_date = booking_date
        self.__description = description
        self.__status = "pending"
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ---- Getters ----
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

    def get_service_type(self):
        return self.__service_type

    def get_booking_date(self):
        return self.__booking_date

    def get_description(self):
        return self.__description

    def get_status(self):
        return self.__status

    def get_created_at(self):
        return self.__created_at

    # ---- Setters ----
    def set_status(self, status):
        valid = ["pending", "accepted", "rejected", "completed", "cancelled"]
        if status in valid:
            self.__status = status
            return True
        return False

    def to_dict(self):
        """Return booking as dictionary"""
        return {
            "Booking ID": self.__booking_id,
            "Customer": self.__customer_name,
            "Provider": self.__provider_name,
            "Service": self.__service_type,
            "Date": self.__booking_date,
            "Description": self.__description,
            "Status": self.__status,
            "Created": self.__created_at
        }

    def __str__(self):
        return (f"Booking #{self.__booking_id} | "
                f"{self.__service_type} | "
                f"Status: {self.__status}")