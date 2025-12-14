import pytest
from app.database import SessionLocal
from app.models import User, Sweet

@pytest.fixture(autouse=True)
def clear_database():
    db = SessionLocal()
    db.query(User).delete()
    db.query(Sweet).delete()
    db.commit()
    db.close()
