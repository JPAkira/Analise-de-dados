from sqlalchemy import create_engine
from main import settings

def get_connection():
    db_url = f"sqlite:///{str(settings.DATABASES['default']['NAME'])}"
    engine = create_engine(db_url, echo=False)
    return engine