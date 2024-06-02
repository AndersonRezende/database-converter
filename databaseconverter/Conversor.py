from databaseconverter.db.utils.DatabaseUtils import DatabaseUtils


class Conversor:
    def __init__(self, origin, destination):
        self.connection_origin = DatabaseUtils(
            db=origin['db'],
            host=origin['host'],
            user=origin['user'],
            password=origin['password'],
            database=origin['database'],
            port=origin['port'],
        )

        self.connection_destination = DatabaseUtils(
            db=destination['db'],
            host=destination['host'],
            user=destination['user'],
            password=destination['password'],
            database=destination['database'],
            port=destination['port'],
        )

    def convert(self):
        tables = self.connection_origin.table_list()
        print(tables)
        for table in tables:
            print(table[0])
            print(self.connection_origin.table_field_list(table[0]))

