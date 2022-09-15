from sqlalchemy import create_engine
import pandas as pd
from main import settings

def ingestor_job():
    df = pd.read_csv('data/AppleStore.csv', index_col=0)
    db_url = f"sqlite:///{str(settings.DATABASES['default']['NAME'])}"
    cnx = create_engine(db_url, echo=False)
    df.to_sql('datamanager_applestore', con=cnx, if_exists='replace', index=False)

ingestor_job()