# Analise-de-dados


# Instalação
```
python -m venv .venv
pip install -r requirements.txt
```

# Criar o banco de dados local
```
python manage.py migrate
```

# Atualização dos dados:
```
O job roda diariamente atualizando o banco de dados e gerando o arquivo de resposta a partir do arquivo contido em "ingestor/data/AppleStore.csv"
```

# Api com o top 10 mais citados na própria API:
```
http://127.0.0.1:8000/api/top10citacoes/
```

#  Retorno dos CSVs em "ingestor/data/" contendo top 1 categoria news e top 10 categoria music e books. É atualizado diariamente
