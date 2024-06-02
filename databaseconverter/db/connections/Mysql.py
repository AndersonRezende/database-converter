from databaseconverter.db.connections.DatabaseConnector import (DatabaseConnector, )
import mysql.connector


class Mysql(DatabaseConnector):
    def __init__(self, config):
        self.conn = None
        self.config = config

    # def get_connection(self):
    #    self.conn = mysql.connector.connect(**self.config)

    def open_connection(self):
        self.conn = mysql.connector.connect(**self.config)
        return self.conn

    def close_connection(self):
        if self.conn.is_connected():
            self.conn.cursor().close()
            self.conn.close()

    def table_list(self):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(Mysql.sql_table_list(self.config['database']))
        tables = cursor.fetchall()
        self.close_connection()
        return tables

    def table_field_list(self, table):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(Mysql.sql_table_field(self.config['database'], table))
        fields = cursor.fetchall()
        self.close_connection()
        return fields

    @staticmethod
    def sql_table_list(schema):
        return f'show tables from {schema};'

    @staticmethod
    def sql_table_field(schema, table):
        return (
            f'SELECT * FROM INFORMATION_SCHEMA.COLUMNS '
            f'WHERE TABLE_SCHEMA = {schema} AND TABLE_NAME = "{table}"'
            f'ORDER BY ordinal_position;'
        )
