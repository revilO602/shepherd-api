from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from app.database import Base
from app.models.mixins import TimestampMixin


class Poi(Base):
    __tablename__ = "pois"

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    name = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    ranking = Column(Integer)
    ranking_out_of = Column(Integer)
    num_reviews = Column(Integer)
    popularity = Column(Float)
    tags = Column(ARRAY(String()))
    reviews = Column(JSONB)

    tf_idf_relevances = Column(JSONB)
