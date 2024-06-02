from databaseconverter.db.connections.DatabaseConnector import (DatabaseConnector, )
import psycopg2


class Postgres(DatabaseConnector):
    def __init__(self, config):
        self.conn = None
        self.config = config

    # def get_connection(self):
    #    self.conn = mysql.connector.connect(**self.config)

    def open_connection(self):
        self.conn = psycopg2.connect(**self.config)
        return self.conn

    def close_connection(self):
        if self.conn.closed == 0:
            self.conn.cursor().close()
            self.conn.close()

    def table_list(self):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(Postgres.sql_table_list())
        tables = cursor.fetchall()
        self.close_connection()
        return tables
    
    def table_field_list(self, table):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(Postgres.sql_table_field('public', table))
        fields = cursor.fetchall()
        self.close_connection()
        return fields

    @staticmethod
    def sql_table_list(schema='public'):
        return f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';"

    @staticmethod
    def sql_table_field(schema, table):
        # column_name, is_nullable, data_type, character_maximum_length, numeric_precision, numeric_scale,
        # Order by ordinal_position
        return (
            f'SELECT column_name, data_type, is_nullable, character_maximum_length, numeric_precision, numeric_scale '
            f"FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{table}'"
            f'ORDER BY ordinal_position;'
        )

    @staticmethod
    def get_create_table_sql(table, fields):
        # Converter o tipo de dado e gerar o sql do campo e fazer o append no texto
        return f'CREATE TABLE {table} ({fields})'
