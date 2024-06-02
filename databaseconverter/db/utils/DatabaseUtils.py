from databaseconverter.db.connections.Mysql import Mysql
from databaseconverter.db.connections.Postgres import Postgres
from databaseconverter.db.connections.Oracle import Oracle


class DatabaseUtils:
    def __init__(self, db, host, user, password, database, port):
        self.db = db
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'port': self.port,
        }
        match self.db:
            case 'mysql':
                self.connection = Mysql(self.config)
            case 'postgres':
                self.connection = Postgres(self.config)
            case 'oracle':
                self.connection = Oracle(self.config)
            case 'sqlserver':
                print('sqlserver')
            case _:
                raise Exception('Database not supported.')

    def get_connection(self):
        return self.connection

    def table_list(self):
        return self.connection.table_list()

    def table_field_list(self, table):
        return self.connection.table_field_list(table)

    def get_create_table_sql(self, table_name):
        command = ''
        match self.db:
            case 'mysql':
                command = f'SHOW CREATE TABLE {table_name}'
                # command = "SELECT CONCAT('CREATE TABLE ', GROUP_CONCAT(column_definition SEPARATOR ', '), ';') AS create_table_statement " \
                #          "FROM (SELECT CONCAT(column_name, ' ', column_type) AS column_definition FROM INFORMATION_SCHEMA.COLUMNS " \
                #          "WHERE table_name = '{table_name}') AS columns_definition;"
            case 'postgres':
                command = """SELECT 'CREATE TABLE ' || table_name || ' (' || string_agg(column_name || ' ' || data_type || 
                          "CASE WHEN character_maximum_length IS NOT NULL THEN '(' || character_maximum_length || ')'
                          "ELSE '' END, ', ') || ');'
                          f"FROM information_schema.columns WHERE table_name = '{table_name}'
                          "GROUP BY table_name;"""
            case 'oracle':
                command = "SELECT dbms_metadata.get_ddl('TABLE', '{table_name}', '{self.database}') FROM dual;"
            case 'sqlserver':
                command = "SELECT t.name AS 'Nome da Tabela', OBJECT_DEFINITION(OBJECT_ID) AS 'DDL de Criação da Tabela' FROM sys.tables t;"
                # select DBMS_METADATA.GET_DDL('TABLE','USUARIO','SIM3G_FLORA_2018_01_23') from DUAL;
            case _:
                raise Exception('Database not supported.')
        return command
