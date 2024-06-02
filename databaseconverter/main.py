import os
from dotenv import load_dotenv

from databaseconverter.Conversor import Conversor


def load_env():
    load_dotenv()


if __name__ == '__main__':
    load_env()
    origin_config = {
        'host': os.getenv('ORIGIN_DB_HOST'),
        'user': os.getenv('ORIGIN_DB_USER'),
        'password': os.getenv('ORIGIN_DB_PASSWORD'),
        'database': os.getenv('ORIGIN_DB_DATABASE'),
        'port': os.getenv('ORIGIN_DB_PORT'),
        'db': os.getenv('ORIGIN_DB'),
    }

    destination_config = {
        'host': os.getenv('DESTINATION_DB_HOST'),
        'user': os.getenv('DESTINATION_DB_USER'),
        'password': os.getenv('DESTINATION_DB_PASSWORD'),
        'database': os.getenv('DESTINATION_DB_DATABASE'),
        'port': os.getenv('DESTINATION_DB_PORT'),
        'db': os.getenv('DESTINATION_DB'),
    }
    print(origin_config)

    conversor = Conversor(origin_config, destination_config)
    conversor.convert()
