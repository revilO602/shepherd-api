from app.data_collection.ta_locations import ta_locations
from app.models.poi import Poi
from app.database import SessionLocal


# scrape POI ids and other info from Tripadvisor and create rows in the DB for futher data collection
def init_locations():
    session = SessionLocal()
    # Insert data into the 'pois' table
    print("Inserting POIs")
    for location in ta_locations:
        poi_instance = Poi(id=location["id"], image_url=location["image_url"])
        session.add(poi_instance)
    session.flush()
    # Commit the session to save the data into the database
    session.commit()

    # Close the session
    session.close()


init_locations()
