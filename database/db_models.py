from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text,
    DateTime, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base


# ==========================================
# USERS TABLE
# ==========================================
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    role = Column(String(20), nullable=False)  # 'customer' or 'provider'
    address = Column(String(255), default="")  # For customers
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    provider_profile = relationship(
        "ProviderProfileDB",
        back_populates="user",
        uselist=False
    )
    bookings_as_customer = relationship(
        "BookingDB",
        back_populates="customer",
        foreign_keys="BookingDB.customer_id"
    )
    bookings_as_provider = relationship(
        "BookingDB",
        back_populates="provider",
        foreign_keys="BookingDB.provider_id"
    )
    reviews_given = relationship(
        "ReviewDB",
        back_populates="customer",
        foreign_keys="ReviewDB.customer_id"
    )
    reviews_received = relationship(
        "ReviewDB",
        back_populates="provider",
        foreign_keys="ReviewDB.provider_id"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role}')>"


# ==========================================
# PROVIDER PROFILE TABLE
# ==========================================
class ProviderProfileDB(Base):
    __tablename__ = "provider_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    service_type = Column(String(50), nullable=False)
    experience = Column(Integer, default=0)
    hourly_rate = Column(Float, default=0.0)
    location = Column(String(255), default="")
    description = Column(Text, default="")
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship
    user = relationship("UserDB", back_populates="provider_profile")

    def __repr__(self):
        return f"<ProviderProfile(user_id={self.user_id}, service='{self.service_type}')>"


# ==========================================
# BOOKINGS TABLE
# ==========================================
class BookingDB(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(String(50), nullable=False)
    booking_date = Column(String(20), nullable=False)
    description = Column(Text, default="")
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    customer = relationship(
        "UserDB",
        back_populates="bookings_as_customer",
        foreign_keys=[customer_id]
    )
    provider = relationship(
        "UserDB",
        back_populates="bookings_as_provider",
        foreign_keys=[provider_id]
    )
    review = relationship("ReviewDB", back_populates="booking", uselist=False)

    def __repr__(self):
        return f"<Booking(id={self.id}, status='{self.status}')>"


# ==========================================
# REVIEWS TABLE
# ==========================================
class ReviewDB(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, default="")
    service_type = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.now)

    # Add constraint: rating must be 1-5
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="valid_rating"),
    )

    # Relationships
    booking = relationship("BookingDB", back_populates="review")
    customer = relationship(
        "UserDB",
        back_populates="reviews_given",
        foreign_keys=[customer_id]
    )
    provider = relationship(
        "UserDB",
        back_populates="reviews_received",
        foreign_keys=[provider_id]
    )

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"