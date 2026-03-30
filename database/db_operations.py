from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db_config import get_db, init_db
from database.db_models import UserDB, ProviderProfileDB, BookingDB, ReviewDB, ProviderRequestDB
from datetime import datetime


class DatabaseManager:
    """
    Handles all database CRUD operations.
    C = Create, R = Read, U = Update, D = Delete
    """

    def __init__(self):
        init_db()


    def create_user(self, name, email, password, phone, role, address=""):
        """Create a new user (customer or provider)"""
        db = get_db()
        try:
            # Check if email already exists
            existing = db.query(UserDB).filter(
                UserDB.email == email
            ).first()
            if existing:
                db.close()
                return {"success": False, "message": "Email already exists!"}

            new_user = UserDB(
                name=name,
                email=email,
                password=password,
                phone=phone,
                role=role,
                address=address
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_id = new_user.id
            db.close()
            return {
                "success": True,
                "message": "User created!",
                "user_id": user_id
            }
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def authenticate_user(self, email, password, role):
        """Login - verify email and password"""
        db = get_db()
        try:
            user = db.query(UserDB).filter(
                UserDB.email == email,
                UserDB.password == password,
                UserDB.role == role
            ).first()
            db.close()

            if user:
                return {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "phone": user.phone,
                        "role": user.role,
                        "address": user.address
                    }
                }
            return {"success": False, "message": "Invalid credentials!"}
        except Exception as e:
            db.close()
            return {"success": False, "message": str(e)}

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        db = get_db()
        try:
            user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                result = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "address": user.address
                }
                db.close()
                return result
            db.close()
            return None
        except Exception as e:
            db.close()
            return None

    def get_user_by_email(self, email):
        """Get user by email"""
        db = get_db()
        try:
            user = db.query(UserDB).filter(UserDB.email == email).first()
            if user:
                result = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "address": user.address
                }
                db.close()
                return result
            db.close()
            return None
        except Exception as e:
            db.close()
            return None

    def update_user(self, user_id, **kwargs):
        """Update user fields"""
        db = get_db()
        try:
            user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                if "name" in kwargs:
                    user.name = kwargs["name"]
                if "phone" in kwargs:
                    user.phone = kwargs["phone"]
                if "address" in kwargs:
                    user.address = kwargs["address"]
                if "password" in kwargs:
                    user.password = kwargs["password"]
                db.commit()
                db.close()
                return {"success": True, "message": "User updated!"}
            db.close()
            return {"success": False, "message": "User not found!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        db = get_db()
        try:
            user = db.query(UserDB).filter(
                UserDB.id == user_id,
                UserDB.password == old_password
            ).first()
            if user:
                user.password = new_password
                db.commit()
                db.close()
                return {"success": True}
            db.close()
            return {"success": False, "message": "Wrong password!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}



    def create_provider_profile(self, user_id, service_type, experience,
                                hourly_rate, location, description):
        """Create a provider profile"""
        db = get_db()
        try:
            # Check if profile already exists
            existing = db.query(ProviderProfileDB).filter(
                ProviderProfileDB.user_id == user_id
            ).first()

            if existing:
                db.close()
                return {
                    "success": False,
                    "message": "Profile already exists! Use update instead."
                }

            profile = ProviderProfileDB(
                user_id=user_id,
                service_type=service_type,
                experience=experience,
                hourly_rate=hourly_rate,
                location=location,
                description=description
            )
            db.add(profile)
            db.commit()
            db.close()
            return {"success": True, "message": "Profile created!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def update_provider_profile(self, user_id, **kwargs):
        """Update provider profile"""
        db = get_db()
        try:
            profile = db.query(ProviderProfileDB).filter(
                ProviderProfileDB.user_id == user_id
            ).first()

            if profile:
                if "service_type" in kwargs:
                    profile.service_type = kwargs["service_type"]
                if "experience" in kwargs:
                    profile.experience = kwargs["experience"]
                if "hourly_rate" in kwargs:
                    profile.hourly_rate = kwargs["hourly_rate"]
                if "location" in kwargs:
                    profile.location = kwargs["location"]
                if "description" in kwargs:
                    profile.description = kwargs["description"]
                if "is_available" in kwargs:
                    profile.is_available = kwargs["is_available"]

                profile.updated_at = datetime.now()
                db.commit()
                db.close()
                return {"success": True, "message": "Profile updated!"}

            db.close()
            return {"success": False, "message": "Profile not found!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def get_provider_profile(self, user_id):
        """Get provider profile by user ID"""
        db = get_db()
        try:
            profile = db.query(ProviderProfileDB).filter(
                ProviderProfileDB.user_id == user_id
            ).first()

            if profile:
                result = {
                    "id": profile.id,
                    "user_id": profile.user_id,
                    "service_type": profile.service_type,
                    "experience": profile.experience,
                    "hourly_rate": profile.hourly_rate,
                    "location": profile.location,
                    "description": profile.description,
                    "is_available": profile.is_available
                }
                db.close()
                return result
            db.close()
            return None
        except Exception as e:
            db.close()
            return None

    def get_all_providers(self, service_type=None):
        """Get all providers, optionally filtered by service type"""
        db = get_db()
        try:
            query = db.query(UserDB, ProviderProfileDB).join(
                ProviderProfileDB,
                UserDB.id == ProviderProfileDB.user_id
            ).filter(UserDB.role == "provider")

            if service_type and service_type != "All":
                query = query.filter(
                    ProviderProfileDB.service_type == service_type
                )

            results = query.all()
            providers = []

            for user, profile in results:
                # Get average rating
                avg_rating = db.query(func.avg(ReviewDB.rating)).filter(
                    ReviewDB.provider_id == user.id
                ).scalar()

                review_count = db.query(func.count(ReviewDB.id)).filter(
                    ReviewDB.provider_id == user.id
                ).scalar()

                providers.append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "service_type": profile.service_type,
                    "experience": profile.experience,
                    "hourly_rate": profile.hourly_rate,
                    "location": profile.location,
                    "description": profile.description,
                    "is_available": profile.is_available,
                    "average_rating": round(avg_rating, 1) if avg_rating else 0.0,
                    "review_count": review_count or 0
                })

            db.close()
            return providers
        except Exception as e:
            db.close()
            return []



    def create_booking(self, customer_id, provider_id, service_type,
                       booking_date, description):
        """Create a new booking"""
        db = get_db()
        try:
            booking = BookingDB(
                customer_id=customer_id,
                provider_id=provider_id,
                service_type=service_type,
                booking_date=booking_date,
                description=description,
                status="pending"
            )
            db.add(booking)
            db.commit()
            db.refresh(booking)
            booking_id = booking.id
            db.close()
            return {
                "success": True,
                "message": "Booking created!",
                "booking_id": booking_id
            }
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def update_booking_status(self, booking_id, new_status):
        """Update booking status"""
        valid_statuses = [
            "pending", "accepted", "rejected", "completed", "cancelled"
        ]
        if new_status not in valid_statuses:
            return {"success": False, "message": "Invalid status!"}

        db = get_db()
        try:
            booking = db.query(BookingDB).filter(
                BookingDB.id == booking_id
            ).first()

            if booking:
                booking.status = new_status
                booking.updated_at = datetime.now()
                db.commit()
                db.close()
                return {"success": True, "message": f"Status updated to {new_status}!"}

            db.close()
            return {"success": False, "message": "Booking not found!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def get_customer_bookings(self, customer_id):
            """Get all bookings for a customer including provider contact details"""
            db = get_db()
            try:
                # We join BookingDB with UserDB (the provider) to get their profile info
                bookings = db.query(BookingDB, UserDB).join(
                    UserDB,
                    BookingDB.provider_id == UserDB.id
                ).filter(
                    BookingDB.customer_id == customer_id
                ).order_by(BookingDB.created_at.desc()).all()

                result = []
                for booking, provider in bookings:
                    result.append({
                        "id": booking.id,
                        "provider_id": booking.provider_id,
                        "provider_name": provider.name,
                        "provider_phone": provider.phone,  # <--- ADDED THIS LINE
                        "service_type": booking.service_type,
                        "booking_date": booking.booking_date,
                        "description": booking.description,
                        "status": booking.status,
                        "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M")
                        if booking.created_at else ""
                    })

                db.close()
                return result
            except Exception as e:
                if db:
                    db.close()
                return []

    def get_provider_bookings(self, provider_id, status=None):
        """Get all bookings for a provider"""
        db = get_db()
        try:
            query = db.query(BookingDB, UserDB).join(
                UserDB,
                BookingDB.customer_id == UserDB.id
            ).filter(BookingDB.provider_id == provider_id)

            if status:
                query = query.filter(BookingDB.status == status)

            bookings = query.order_by(BookingDB.created_at.desc()).all()

            result = []
            for booking, customer in bookings:
                result.append({
                    "id": booking.id,
                    "customer_id": booking.customer_id,
                    "customer_name": customer.name,
                    "service_type": booking.service_type,
                    "booking_date": booking.booking_date,
                    "description": booking.description,
                    "status": booking.status,
                    "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M")
                    if booking.created_at else ""
                })

            db.close()
            return result
        except Exception as e:
            db.close()
            return []

    def get_booking_by_id(self, booking_id):
        """Get a single booking"""
        db = get_db()
        try:
            booking = db.query(BookingDB).filter(
                BookingDB.id == booking_id
            ).first()

            if booking:
                result = {
                    "id": booking.id,
                    "customer_id": booking.customer_id,
                    "provider_id": booking.provider_id,
                    "service_type": booking.service_type,
                    "booking_date": booking.booking_date,
                    "description": booking.description,
                    "status": booking.status
                }
                db.close()
                return result
            db.close()
            return None
        except Exception as e:
            db.close()
            return None


    def create_review(self, booking_id, customer_id, provider_id,
                      rating, review_text, service_type):
        """Create a new review"""
        db = get_db()
        try:
            # Check if review already exists for this booking
            existing = db.query(ReviewDB).filter(
                ReviewDB.booking_id == booking_id
            ).first()

            if existing:
                db.close()
                return {
                    "success": False,
                    "message": "Review already exists for this booking!"
                }

            review = ReviewDB(
                booking_id=booking_id,
                customer_id=customer_id,
                provider_id=provider_id,
                rating=rating,
                review_text=review_text,
                service_type=service_type
            )
            db.add(review)
            db.commit()
            db.refresh(review)
            review_id = review.id
            db.close()
            return {
                "success": True,
                "message": "Review submitted!",
                "review_id": review_id
            }
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}

    def get_provider_reviews(self, provider_id):
        """Get all reviews for a provider"""
        db = get_db()
        try:
            reviews = db.query(ReviewDB, UserDB).join(
                UserDB,
                ReviewDB.customer_id == UserDB.id
            ).filter(
                ReviewDB.provider_id == provider_id
            ).order_by(ReviewDB.created_at.desc()).all()

            result = []
            for review, customer in reviews:
                result.append({
                    "id": review.id,
                    "booking_id": review.booking_id,
                    "customer_id": review.customer_id,
                    "customer_name": customer.name,
                    "provider_id": review.provider_id,
                    "rating": review.rating,
                    "review_text": review.review_text,
                    "service_type": review.service_type,
                    "created_at": review.created_at.strftime("%Y-%m-%d %H:%M")
                    if review.created_at else ""
                })

            db.close()
            return result
        except Exception as e:
            db.close()
            return []

    def get_customer_reviews(self, customer_id):
        """Get all reviews given by a customer"""
        db = get_db()
        try:
            reviews = db.query(ReviewDB, UserDB).join(
                UserDB,
                ReviewDB.provider_id == UserDB.id
            ).filter(
                ReviewDB.customer_id == customer_id
            ).order_by(ReviewDB.created_at.desc()).all()

            result = []
            for review, provider in reviews:
                result.append({
                    "id": review.id,
                    "booking_id": review.booking_id,
                    "provider_id": review.provider_id,
                    "provider_name": provider.name,
                    "rating": review.rating,
                    "review_text": review.review_text,
                    "service_type": review.service_type,
                    "created_at": review.created_at.strftime("%Y-%m-%d %H:%M")
                    if review.created_at else ""
                })

            db.close()
            return result
        except Exception as e:
            db.close()
            return []

    def get_reviews_by_service(self, service_type):
        """Get all reviews for a specific service type"""
        db = get_db()
        try:
            reviews = db.query(ReviewDB).filter(
                ReviewDB.service_type == service_type
            ).all()

            result = []
            for review in reviews:
                result.append({
                    "id": review.id,
                    "provider_id": review.provider_id,
                    "rating": review.rating,
                    "review_text": review.review_text,
                    "service_type": review.service_type
                })

            db.close()
            return result
        except Exception as e:
            db.close()
            return []

    def get_provider_average_rating(self, provider_id):
        """Get average rating for a provider"""
        db = get_db()
        try:
            avg = db.query(func.avg(ReviewDB.rating)).filter(
                ReviewDB.provider_id == provider_id
            ).scalar()
            db.close()
            return round(avg, 1) if avg else 0.0
        except Exception as e:
            db.close()
            return 0.0

    def get_provider_rating_distribution(self, provider_id):
        """Get rating distribution (count per star)"""
        db = get_db()
        try:
            distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

            results = db.query(
                ReviewDB.rating,
                func.count(ReviewDB.id)
            ).filter(
                ReviewDB.provider_id == provider_id
            ).group_by(ReviewDB.rating).all()

            for rating, count in results:
                distribution[rating] = count

            db.close()
            return distribution
        except Exception as e:
            db.close()
            return {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}


    def get_provider_earnings(self, provider_id):
        """Calculate total earnings for a provider"""
        db = get_db()
        try:
            # Get profile for hourly rate
            profile = db.query(ProviderProfileDB).filter(
                ProviderProfileDB.user_id == provider_id
            ).first()

            if not profile:
                db.close()
                return 0.0

            # Count completed bookings
            completed_count = db.query(func.count(BookingDB.id)).filter(
                BookingDB.provider_id == provider_id,
                BookingDB.status == "completed"
            ).scalar()

            earnings = (completed_count or 0) * profile.hourly_rate
            db.close()
            return earnings
        except Exception as e:
            db.close()
            return 0.0

    def get_platform_stats(self):
        """Get overall platform statistics"""
        db = get_db()
        try:
            stats = {
                "total_providers": db.query(func.count(UserDB.id)).filter(
                    UserDB.role == "provider"
                ).scalar() or 0,
                "total_customers": db.query(func.count(UserDB.id)).filter(
                    UserDB.role == "customer"
                ).scalar() or 0,
                "total_bookings": db.query(
                    func.count(BookingDB.id)
                ).scalar() or 0,
                "total_reviews": db.query(
                    func.count(ReviewDB.id)
                ).scalar() or 0,
                "completed_bookings": db.query(
                    func.count(BookingDB.id)
                ).filter(
                    BookingDB.status == "completed"
                ).scalar() or 0
            }
            db.close()
            return stats
        except Exception as e:
            db.close()
            return {}

    

    def create_provider_request(self, name, email, password, phone,
                                service_type, experience, hourly_rate,
                                location, description):
        """Submit a provider registration request"""
        db = get_db()
        try:
            # Check if email already exists in users
            existing_user = db.query(UserDB).filter(
                UserDB.email == email
            ).first()
            if existing_user:
                db.close()
                return {"success": False, "message": "Email already registered!"}

            # Check if a pending request already exists
            existing_req = db.query(ProviderRequestDB).filter(
                ProviderRequestDB.email == email,
                ProviderRequestDB.status == "pending"
            ).first()
            if existing_req:
                db.close()
                return {"success": False, "message": "A pending request already exists for this email!"}

            req = ProviderRequestDB(
                name=name, email=email, password=password,
                phone=phone, service_type=service_type,
                experience=experience, hourly_rate=hourly_rate,
                location=location, description=description,
                status="pending"
            )
            db.add(req)
            db.commit()
            db.close()
            return {"success": True, "message": "Request submitted!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}


    def get_all_provider_requests(self, status=None):
        """Get all provider registration requests"""
        db = get_db()
        try:
            query = db.query(ProviderRequestDB)
            if status:
                query = query.filter(ProviderRequestDB.status == status)
            requests = query.order_by(ProviderRequestDB.created_at.desc()).all()

            result = []
            for r in requests:
                result.append({
                    "id": r.id,
                    "name": r.name,
                    "email": r.email,
                    "phone": r.phone,
                    "service_type": r.service_type,
                    "experience": r.experience,
                    "hourly_rate": r.hourly_rate,
                    "location": r.location,
                    "description": r.description,
                    "status": r.status,
                    "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
                    if r.created_at else ""
                })
            db.close()
            return result
        except Exception as e:
            db.close()
            return []


    def process_provider_request(self, request_id, action):
        """
        Approve or reject a provider registration request.
        action = 'approved' or 'rejected'
        """
        db = get_db()
        try:
            req = db.query(ProviderRequestDB).filter(
                ProviderRequestDB.id == request_id
            ).first()

            if not req:
                db.close()
                return {"success": False, "message": "Request not found!"}

            if action == "approved":
                # Check email not already taken
                existing = db.query(UserDB).filter(
                    UserDB.email == req.email
                ).first()
                if existing:
                    req.status = "rejected"
                    db.commit()
                    db.close()
                    return {"success": False, "message": "Email already registered!"}

                # Create the user account
                new_user = UserDB(
                    name=req.name, email=req.email,
                    password=req.password, phone=req.phone,
                    role="provider"
                )
                db.add(new_user)
                db.flush()

                # Create the provider profile
                profile = ProviderProfileDB(
                    user_id=new_user.id,
                    service_type=req.service_type,
                    experience=req.experience,
                    hourly_rate=req.hourly_rate,
                    location=req.location,
                    description=req.description
                )
                db.add(profile)
                req.status = "approved"
                db.commit()
                db.close()
                return {"success": True, "message": f"{req.name} approved and account created!"}

            elif action == "rejected":
                req.status = "rejected"
                db.commit()
                db.close()
                return {"success": True, "message": f"{req.name}'s request rejected."}

            db.close()
            return {"success": False, "message": "Invalid action!"}
        except Exception as e:
            db.rollback()
            db.close()
            return {"success": False, "message": str(e)}



    def seed_sample_data(self):
        """Insert sample data into database"""
        db = get_db()

        # Check if data already exists
        user_count = db.query(func.count(UserDB.id)).scalar()
        if user_count > 0:
            db.close()
            return False  # Data already exists

        try:
            # ---- Providers ----
            providers_data = [
                {
                    "name": "Kamal Silva", "email": "kamal@email.com",
                    "password": "pass123", "phone": "0771234567",
                    "service": "plumbing", "exp": 10, "rate": 1500,
                    "location": "Colombo",
                    "desc": "Expert plumber with 10 years experience."
                },
                {
                    "name": "Nimal Perera", "email": "nimal@email.com",
                    "password": "pass123", "phone": "0777654321",
                    "service": "plumbing", "exp": 5, "rate": 1000,
                    "location": "Kandy",
                    "desc": "Affordable and reliable plumbing services."
                },
                {
                    "name": "Saman Fernando", "email": "saman@email.com",
                    "password": "pass123", "phone": "0779876543",
                    "service": "carpentry", "exp": 8, "rate": 2000,
                    "location": "Colombo",
                    "desc": "Custom furniture, door repairs, and wood work."
                },
                {
                    "name": "Ruwan Dias", "email": "ruwan@email.com",
                    "password": "pass123", "phone": "0771112233",
                    "service": "electrical", "exp": 12, "rate": 1800,
                    "location": "Galle",
                    "desc": "Licensed electrician for all electrical work."
                },
                {
                    "name": "Ajith Kumara", "email": "ajith@email.com",
                    "password": "pass123", "phone": "0774445566",
                    "service": "painting", "exp": 6, "rate": 1200,
                    "location": "Colombo",
                    "desc": "Interior and exterior painting specialist."
                },
                {
                    "name": "Chaminda Bandara", "email": "chaminda@email.com",
                    "password": "pass123", "phone": "0776667788",
                    "service": "cleaning", "exp": 3, "rate": 800,
                    "location": "Kandy",
                    "desc": "Home and office deep cleaning services."
                },
                {
                    "name": "Lasith Malinga", "email": "lasith@email.com",
                    "password": "pass123", "phone": "0778889900",
                    "service": "electrical", "exp": 7, "rate": 1500,
                    "location": "Colombo",
                    "desc": "Wiring, switch repairs, fan installation."
                },
                {
                    "name": "Dinesh Priyantha", "email": "dinesh@email.com",
                    "password": "pass123", "phone": "0770001122",
                    "service": "carpentry", "exp": 15, "rate": 2500,
                    "location": "Galle",
                    "desc": "Master carpenter. Premium furniture work."
                },
            ]

            provider_ids = {}

            for p in providers_data:
                user = UserDB(
                    name=p["name"], email=p["email"],
                    password=p["password"], phone=p["phone"],
                    role="provider"
                )
                db.add(user)
                db.flush()  # Get the ID

                profile = ProviderProfileDB(
                    user_id=user.id,
                    service_type=p["service"],
                    experience=p["exp"],
                    hourly_rate=p["rate"],
                    location=p["location"],
                    description=p["desc"]
                )
                db.add(profile)
                provider_ids[p["email"]] = user.id

            # ---- Customers ----
            customers_data = [
                {
                    "name": "Ashan Bandara", "email": "ashan@email.com",
                    "password": "pass123", "phone": "0712345678",
                    "address": "Colombo 05"
                },
                {
                    "name": "Dilini Jayawardena", "email": "dilini@email.com",
                    "password": "pass123", "phone": "0723456789",
                    "address": "Kandy"
                },
                {
                    "name": "Nuwan Perera", "email": "nuwan@email.com",
                    "password": "pass123", "phone": "0734567890",
                    "address": "Galle"
                },
            ]

            customer_ids = {}

            for c in customers_data:
                user = UserDB(
                    name=c["name"], email=c["email"],
                    password=c["password"], phone=c["phone"],
                    role="customer", address=c["address"]
                )
                db.add(user)
                db.flush()
                customer_ids[c["email"]] = user.id

            # ---- Sample Bookings ----
            booking1 = BookingDB(
                customer_id=customer_ids["ashan@email.com"],
                provider_id=provider_ids["kamal@email.com"],
                service_type="plumbing",
                booking_date="2025-01-15",
                description="Kitchen tap is leaking",
                status="completed"
            )
            db.add(booking1)

            booking2 = BookingDB(
                customer_id=customer_ids["dilini@email.com"],
                provider_id=provider_ids["saman@email.com"],
                service_type="carpentry",
                booking_date="2025-02-10",
                description="Need new kitchen cabinet",
                status="pending"
            )
            db.add(booking2)

            booking3 = BookingDB(
                customer_id=customer_ids["nuwan@email.com"],
                provider_id=provider_ids["ruwan@email.com"],
                service_type="electrical",
                booking_date="2025-02-05",
                description="Ceiling fan not working",
                status="accepted"
            )
            db.add(booking3)

            db.flush()

            # ---- Sample Reviews ----
            reviews_data = [
                # Kamal (plumber) reviews
                {
                    "booking_id": booking1.id,
                    "customer_id": customer_ids["ashan@email.com"],
                    "provider_id": provider_ids["kamal@email.com"],
                    "rating": 5,
                    "text": "Excellent work! Very professional and punctual.",
                    "service": "plumbing"
                },
                {
                    "booking_id": booking1.id + 100,  # Simulated
                    "customer_id": customer_ids["dilini@email.com"],
                    "provider_id": provider_ids["kamal@email.com"],
                    "rating": 4,
                    "text": "Good plumber, friendly and reliable. Quality work.",
                    "service": "plumbing"
                },
                {
                    "booking_id": booking1.id + 101,
                    "customer_id": customer_ids["nuwan@email.com"],
                    "provider_id": provider_ids["kamal@email.com"],
                    "rating": 5,
                    "text": "Best plumber! Highly recommend. Expert and affordable.",
                    "service": "plumbing"
                },
                # Nimal (plumber) reviews
                {
                    "booking_id": booking1.id + 102,
                    "customer_id": customer_ids["ashan@email.com"],
                    "provider_id": provider_ids["nimal@email.com"],
                    "rating": 3,
                    "text": "Average work. Was late and slow. Reasonable price.",
                    "service": "plumbing"
                },
                {
                    "booking_id": booking1.id + 103,
                    "customer_id": customer_ids["dilini@email.com"],
                    "provider_id": provider_ids["nimal@email.com"],
                    "rating": 2,
                    "text": "Poor service. Unprofessional and slow.",
                    "service": "plumbing"
                },
                # Saman (carpenter) reviews
                {
                    "booking_id": booking1.id + 104,
                    "customer_id": customer_ids["ashan@email.com"],
                    "provider_id": provider_ids["saman@email.com"],
                    "rating": 5,
                    "text": "Amazing carpenter! Beautiful furniture. Professional.",
                    "service": "carpentry"
                },
                {
                    "booking_id": booking1.id + 105,
                    "customer_id": customer_ids["dilini@email.com"],
                    "provider_id": provider_ids["saman@email.com"],
                    "rating": 5,
                    "text": "Outstanding quality. Expert craftsmanship. Recommend!",
                    "service": "carpentry"
                },
                # Ruwan (electrician) reviews
                {
                    "booking_id": booking1.id + 106,
                    "customer_id": customer_ids["ashan@email.com"],
                    "provider_id": provider_ids["ruwan@email.com"],
                    "rating": 4,
                    "text": "Good electrician. Fixed wiring quickly. Professional.",
                    "service": "electrical"
                },
                {
                    "booking_id": booking1.id + 107,
                    "customer_id": customer_ids["nuwan@email.com"],
                    "provider_id": provider_ids["ruwan@email.com"],
                    "rating": 5,
                    "text": "Excellent! Expert electrician. Fast and reliable.",
                    "service": "electrical"
                },
                # Ajith (painter) reviews
                {
                    "booking_id": booking1.id + 108,
                    "customer_id": customer_ids["dilini@email.com"],
                    "provider_id": provider_ids["ajith@email.com"],
                    "rating": 4,
                    "text": "Good painting. Clean finish. Friendly person.",
                    "service": "painting"
                },
                # Chaminda (cleaning) reviews
                {
                    "booking_id": booking1.id + 109,
                    "customer_id": customer_ids["ashan@email.com"],
                    "provider_id": provider_ids["chaminda@email.com"],
                    "rating": 5,
                    "text": "Spotless cleaning! Thorough and professional.",
                    "service": "cleaning"
                },
                # Lasith (electrician) reviews
                {
                    "booking_id": booking1.id + 110,
                    "customer_id": customer_ids["dilini@email.com"],
                    "provider_id": provider_ids["lasith@email.com"],
                    "rating": 2,
                    "text": "Poor quality. Unprofessional. Switch broke again.",
                    "service": "electrical"
                },
                # Dinesh (carpenter) reviews
                {
                    "booking_id": booking1.id + 111,
                    "customer_id": customer_ids["ashan@email.com"],
                    "provider_id": provider_ids["dinesh@email.com"],
                    "rating": 4,
                    "text": "Good carpenter. Experienced and skilled. Quality work.",
                    "service": "carpentry"
                },
            ]

            for r in reviews_data:
                review = ReviewDB(
                    booking_id=r["booking_id"],
                    customer_id=r["customer_id"],
                    provider_id=r["provider_id"],
                    rating=r["rating"],
                    review_text=r["text"],
                    service_type=r["service"]
                )
                db.add(review)

            db.commit()
            db.close()
            return True

        except Exception as e:
            db.rollback()
            db.close()
            print(f"Error seeding data: {e}")
            return False