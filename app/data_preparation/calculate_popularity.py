import math
import requests
from app.models.poi import Poi
from app.database import SessionLocal
from app.data_collection.parse_ta_response import parse_response_into_poi
from app.config import settings


def calculate_popularity(rating, num_reviews):
    # Calculate the popularity using the formula
    if num_reviews > 0:
        popularity = rating * math.log2(num_reviews + 1)
    else:
        popularity = 0.0  # Default value when num_reviews is 0 or negative

    return popularity


def add_popularity_to_pois():
    session = SessionLocal()
    try:
        # pois = session.query(Poi).filter(Poi.name.is_(None)).all()
        pois = session.query(Poi).all()
        for poi in pois:
            print(poi.id)
            poi.popularity = calculate_popularity(poi.rating, poi.num_reviews)

        # Commit the session to persist changes
        session.flush()
        session.commit()
        print("Additional data inserted successfully.")
    except Exception as e:
        # Rollback changes if an error occurs
        session.rollback()
        print(f"Error inserting additional data: {e}")

    finally:
        # Close the session to release resources
        session.close()


add_popularity_to_pois()
