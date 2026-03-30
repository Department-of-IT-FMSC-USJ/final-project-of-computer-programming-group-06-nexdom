from database.db_config import engine, Base
import database.db_models  # This ensures all models are loaded

# This line deletes existing tables (if any) and creates new ones
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database recreated successfully!")