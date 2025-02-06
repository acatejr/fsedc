from database import SessionLocal, engine, Base
from crawlers import FSGeodataClearningHouse
from models import Asset

Base.metadata.create_all(bind=engine)

def seed_database():
    fsgch = FSGeodataClearningHouse()
    fsgch.get_metadata_xml_links()
    assets = fsgch.extract_metadata_from_urls()

    if assets:
        session = SessionLocal()
        Base.metadata.create_all(bind=engine)

        for asset in assets:
            session.add(
                Asset(
                    title=asset["title"],
                    description=asset["description"],
                    url=asset["url"],
                )
            )

        session.commit()
        session = None


def main():
    seed_database()


if __name__ == "__main__":
    main()