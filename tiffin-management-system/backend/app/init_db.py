from database.database import Base, engine
from database import models  # noqa: F401


def initialize_database():
    Base.metadata.create_all(bind=engine)
    return True
