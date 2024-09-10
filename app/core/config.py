from sqlmodel import SQLModel, create_engine
import os


class Settings:

    def __init__(self) -> None:
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        print(self.DATABASE_URL)
        self.engine = create_engine(self.DATABASE_URL, echo=True)

    def get_db_metadata(self):
        return SQLModel.metadata

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)
        return


settings = Settings()
