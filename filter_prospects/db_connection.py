import psycopg2
from django.conf import settings

user = settings.DATABASES["default"]["USER"]
pswd = settings.DATABASES["default"]["PASSWORD"]
host = settings.DATABASES["default"]["HOST"]
port = settings.DATABASES["default"]["PORT"]
db = settings.DATABASES["default"]["NAME"]


def get_local_connection():
    connection = psycopg2.connect(user=user,
                                  password=pswd,
                                  host=host,
                                  port=port,
                                  database=db)

    return connection
