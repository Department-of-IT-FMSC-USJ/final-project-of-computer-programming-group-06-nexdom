from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

# SQLite (No installation needed!)
DATABASE_URL = "sqlite:///service_app.db"

# If you want to switch to MySQL later, just change this line:
# DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/service_app_db"

# If you want to switch to PostgreSQL later:
# DATABASE_URL = "postgresql+psycopg2://username:password@localhost/service_app_db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set True to see SQL queries in terminal
    connect_args={"check_same_thread": False}  # Needed for SQLite + Streamlit
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db():
    """Get a database session. Always close after use."""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise


def init_db():
    """Create all tables in the database."""
    from database.db_models import (
        UserDB, ProviderProfileDB, BookingDB, ReviewDB
    )
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")