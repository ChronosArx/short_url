from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

class Settings:

    def __init__(self) -> None:
        load_dotenv()
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.EXPIRE_ACCESS = float(os.environ.get("EXPIRE_ACCESS"))
        self.EXPIRE_REFRESH = float(os.environ.get("EXPIRE_REFRESH"))
        self.engine = create_engine(self.DATABASE_URL, echo=True)
        self.verify_env_variables()

    
    
    def verify_env_variables(self):
        missing_vars = []
        for var_name in ['EXPIRE_ACCESS', 'EXPIRE_REFRESH', 'SECRET_KEY', 'JWT_ALGORITHM', 'DATABASE_URL']:
            if getattr(self, var_name) is None:
                missing_vars.append(var_name)

        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    def get_db_metadata(self):
        return SQLModel.metadata

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)
        return


settings = Settings()
