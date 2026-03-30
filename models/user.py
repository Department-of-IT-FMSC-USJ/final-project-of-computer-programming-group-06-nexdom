class User:
    """
    Parent class for both Customer and ServiceProvider.
    Contains common attributes and methods shared by all users.
    """

    def __init__(self, user_id, name, email, password, phone, role):
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__phone = phone
        self.__role = role
        self.__is_logged_in = False

    # Getters
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_role(self):
        return self.__role

    def is_logged_in(self):
        return self.__is_logged_in

    # Setters
    def set_name(self, name):
        if name and len(name) >= 2:
            self.__name = name
            return True
        return False

    def set_email(self, email):
        if email and "@" in email:
            self.__email = email
            return True
        return False

    def set_phone(self, phone):
        if phone and len(phone) >= 10:
            self.__phone = phone
            return True
        return False

    # Authentication Methods
    def login(self, email, password):
        """Authenticate user with email and password"""
        if self.__email == email and self.__password == password:
            self.__is_logged_in = True
            return True
        return False

    def logout(self):
        """Logout the user"""
        self.__is_logged_in = False

    def change_password(self, old_password, new_password):
        """Change user password after verifying old password"""
        if self.__password == old_password:
            if len(new_password) >= 6:
                self.__password = new_password
                return True
        return False

    # Display
    def display_info(self):
        """Return user info as dictionary"""
        return {
            "Name": self.__name,
            "Email": self.__email,
            "Phone": self.__phone,
            "Role": self.__role
        }

    def __str__(self):
        return f"User({self.__name}, {self.__email}, {self.__role})"