from django_extensions.management.jobs import DailyJob
from sqlalchemy import create_engine
import pandas as pd
from datamanager.models import AppleStore
from main import settings

class Job(DailyJob):
    help = "Atualizar os dados diariamente."

    def execute(self):
        df = pd.read_csv(f'{settings.BASE_DIR}/ingestor/data/AppleStore.csv', index_col=0)
        db_url = f"sqlite:///{str(settings.DATABASES['default']['NAME'])}"
        engine = create_engine(db_url, echo=False)
        top1news = df.loc[df['prime_genre'] == 'News'].sort_values(by='rating_count_tot', ascending=False).head(1)
        top10music_book = df.loc[df['prime_genre'].isin(["Music", "Book"])].sort_values(by='rating_count_tot',
                                                                                        ascending=False).head(10)
        df = pd.concat([top1news, top10music_book])
        df.drop(columns=['currency', 'ver', 'cont_rating', 'sup_devices.num', 'ipadSc_urls.num',
                         'lang.num', 'vpp_lic', 'user_rating', 'user_rating_ver',
                         'rating_count_ver', 'rating_count_tot'], inplace=True)
        existing_data = AppleStore.objects.all()
        create_data = df.loc[~df['id'].isin(existing_data.values_list('id', flat=True))]
        update_data = df.loc[df['id'].isin(existing_data.values_list('id', flat=True))]
        create_data['n_citacoes'] = 0
        create_data.to_sql('datamanager_applestore', con=engine, if_exists='append', index=False)

        update_data.to_sql('temp_table', engine, if_exists='replace')

        sql = """
            UPDATE datamanager_applestore AS f
            SET track_name = t.track_name,
            size_bytes = t.size_bytes,
            price = t.price,
            prime_genre = t.prime_genre
            FROM temp_table AS t
            WHERE f.id = t.id
        """

        with engine.begin() as conn:
            conn.execute(sql)
