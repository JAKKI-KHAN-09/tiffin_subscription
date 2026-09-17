import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND = os.path.join(ROOT, "backend")

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_tiffin.db")

for path in (ROOT, BACKEND):
    if path not in sys.path:
        sys.path.insert(0, path)

from database import models  # noqa: F401
from database.database import Base, engine

TEST_DB_PATH = os.path.join(ROOT, "test_tiffin.db")
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

Base.metadata.create_all(bind=engine)
