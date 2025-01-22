# from models import User
from database import SessionLocal, engine, Base
from main import FSGeodataClearningHouse
from models import Asset

# Create tables
Base.metadata.create_all(bind=engine)

# Seed the database with initial data
def seed_database():
    session = SessionLocal()

    if not session.query(Asset).first():
        fsch = FSGeodataClearningHouse()
        fsch.get_metadata_xml_links()
        assets = fsch.extract_metadata()

        for asset in assets:
            session.add(Asset(description=asset['description']))
            session.commit()

        print("Database seeded successfully!")
    else:
        print("Database already seeded, skipping.")

    session.close()

# Run the seed function if this file is executed directly
if __name__ == "__main__":
    seed_database()