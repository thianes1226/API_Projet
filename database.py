
import psycopg2

### Fonction pour établir une connexion à la base de données PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="sarr",
        user="postgres",
        password="thiane1226"
    )