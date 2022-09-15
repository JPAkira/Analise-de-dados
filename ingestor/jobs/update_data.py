from django_extensions.management.jobs import DailyJob
import pandas as pd
from datamanager.models import AppleStore
from ingestor.utils import get_connection
from main import settings

class Job(DailyJob):
    help = "Atualizar os dados diariamente."

    def execute(self):
        df = pd.read_csv(f'{settings.BASE_DIR}/ingestor/data/AppleStore.csv', index_col=0)

        # Conexão com o banco de dados
        engine = get_connection()

        # Buscando o TOP1 do gênero News
        top1news = df.loc[df['prime_genre'] == 'News'].sort_values(by='rating_count_tot', ascending=False).head(1)

        # Removendo colunas desnecessárias
        top1news.drop(columns=['currency', 'ver', 'cont_rating', 'sup_devices.num', 'ipadSc_urls.num',
                         'lang.num', 'vpp_lic', 'user_rating', 'user_rating_ver',
                         'rating_count_ver', 'rating_count_tot'], inplace=True)

        # Exportando para csv
        top1news.to_csv(f'{settings.BASE_DIR}/ingestor/data/top1news.csv', index=False)


        # Buscando o TOP10 do gênero Music / Book
        top10music_book = df.loc[df['prime_genre'].isin(["Music", "Book"])].sort_values(by='rating_count_tot',
                                                                                        ascending=False).head(10)

        # Removendo colunas desnecessárias
        top10music_book.drop(columns=['currency', 'ver', 'cont_rating', 'sup_devices.num', 'ipadSc_urls.num',
                         'lang.num', 'vpp_lic', 'user_rating', 'user_rating_ver',
                         'rating_count_ver', 'rating_count_tot'], inplace=True)

        # Exportando para csv
        top10music_book.to_csv(f'{settings.BASE_DIR}/ingestor/data/top10music_book.csv', index=False)
        df = pd.concat([top1news, top10music_book])
        df.drop(columns=['currency', 'ver', 'cont_rating', 'sup_devices.num', 'ipadSc_urls.num',
                         'lang.num', 'vpp_lic', 'user_rating', 'user_rating_ver',
                         'rating_count_ver', 'rating_count_tot'], inplace=True)

        # Verificando quais registros estão no banco de dados
        existing_data = AppleStore.objects.all()
        create_data = df.loc[~df['id'].isin(existing_data.values_list('id', flat=True))]
        update_data = df.loc[df['id'].isin(existing_data.values_list('id', flat=True))]

        # Inicializando como 0 citações, como não temos o histórico
        create_data['n_citacoes'] = 0

        # Criando novos registros
        create_data.to_sql('datamanager_applestore', con=engine, if_exists='append', index=False)

        # Atualizando novos registros
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

        print('Dados atualizados com sucesso!')
