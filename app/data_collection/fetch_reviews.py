import requests
from app.models.poi import Poi
from app.database import SessionLocal
from app.data_collection.parse_ta_response import parse_response_into_poi
from app.config import settings


def fetch_ta_reviews():
    session = SessionLocal()
    try:
        # pois = session.query(Poi).filter(Poi.name.is_(None)).all()
        pois = session.query(Poi).all()
        for poi in pois:
            location_id = poi.id
            print(poi.id)
            url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews?key={settings.TA_API_KEY}"

            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                db_reviews = []
                reviews = response.json().get("data")
                for review in reviews:
                    db_reviews.append(
                        {
                            "title": review.get("title"),
                            "text": review.get("text"),
                            "trip_type": review.get("trip_type"),
                        }
                    )
                poi.reviews = db_reviews
            else:
                print(
                    f"Failed to fetch details for location ID {location_id}. Status code: {response.status_code}"
                )

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


fetch_ta_reviews()
