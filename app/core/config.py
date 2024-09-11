from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

class Settings:

    def __init__(self) -> None:
        load_dotenv()
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.DOMAIN_URL = os.getenv('DOMAIN_URL')

        # Manejo de posibles errores en la conversión
        try:
            self.EXPIRE_ACCESS = float(os.getenv("EXPIRE_ACCESS"))
            self.EXPIRE_REFRESH = float(os.getenv("EXPIRE_REFRESH"))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid value for EXPIRE_ACCESS or EXPIRE_REFRESH: {e}")

        self.verify_env_variables()
        self.engine = create_engine(self.DATABASE_URL, echo=True)


    
    def verify_env_variables(self):
        missing_vars = []
        for var_name in ['EXPIRE_ACCESS', 'EXPIRE_REFRESH', 'SECRET_KEY', 'JWT_ALGORITHM', 'DATABASE_URL', 'DOMAIN_URL']:
            if getattr(self, var_name) is None:
                missing_vars.append(var_name)

        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    def get_db_metadata(self):
        return SQLModel.metadata

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)
        return
    
    def get_domain_name(self) -> str:
        if 'localhost' in self.DOMAIN_URL:
            return f'http://{self.DOMAIN_URL}'
        return f'https://{self.DOMAIN_URL}'



settings = Settings()
