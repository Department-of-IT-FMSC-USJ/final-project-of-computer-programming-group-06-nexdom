from database.db_config import engine, Base
import database.db_models 


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database recreated successfully!")