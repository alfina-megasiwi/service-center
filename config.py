from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

class Settings:
    POSTGRES_USER=os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER=os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT")
    POSTGRES_DB=os.getenv("POSTGRES_DB")

    DATABASE_URL=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

setting = Settings()