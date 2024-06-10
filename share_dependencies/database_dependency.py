from ..database.data_base_conf import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()