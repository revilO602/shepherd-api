from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """
    Mixin class to add timestamp columns (created_at, updated_at) to SQLAlchemy models.
    """

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True)
