import cx_Oracle

# import oracledb
# conn = oracledb.connect(user="[Username]", password="[Password]", dsn="localhost:1521/FREEPDB1")
# with conn.cursor() as cur:
#    cur.execute("SELECT 'Hello World!' FROM dual")
#    res = cur.fetchall()
#    print(res)

from databaseconverter.db.connections.DatabaseConnector import (DatabaseConnector,)
import psycopg2


class Oracle(DatabaseConnector):
    def __init__(self, config):
        self.conn = None
        self.config = config

    # def get_connection(self):
    #    self.conn = mysql.connector.connect(**self.config)

    def open_connection(self):
        self.conn = cx_Oracle.connect(
            user=self.config.user,
            password=self.config.password,
            dsn=self.config.host,
        )
        return self.conn

    def close_connection(self):
        if self.conn.is_connected():
            self.conn.cursor().close()
            self.conn.close()

    def table_list(self):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(Oracle.sql_table_list(self.config['database']))
        tables = cursor.fetchall()
        self.close_connection()
        return tables

    def table_field_list(self, table):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(Oracle.sql_table_field(self.config['database'], table))
        fields = cursor.fetchall()
        self.close_connection()
        return fields

    @staticmethod
    def sql_table_list(schema):
        return f"SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = '{schema}';"

    def table_fields(schema, table):
        # column_name, is_nullable, data_type, character_maximum_length, numeric_precision, numeric_scale,
        # Order by ordinal_position
        return (
            f'SELECT column_name, nullable, data_type, char_col_decl_length, data_precision, data_scale '
            f'FROM ALL_TAB_COLUMNS WHERE OWNER = {schema} AND TABLE_NAME ILIKE {table} ORDER BY COLUMN_ID '
        )
