import pyodbc
from dataclasses import dataclass, field, InitVar
from timsy_config import Config
import timsy_log

logger = timsy_log.getLogger('SqlConn')


def precursor(func):
    def wrapper(*args, **kwargs):
        cursor: pyodbc.Cursor | None = None
        try:
            wrapper_self: SqlConn = args[0]
            cursor: pyodbc.Cursor = wrapper_self.get_cursor()
            if cursor is None:
                raise ValueError('Cursor is None')
            return func(*args, cursor=cursor, **kwargs)
        except Exception as e:
            logger.error(f'{type(e).__name__}: {e}')
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    return wrapper


@dataclass
class SqlConn:
    config: Config = field(default_factory=Config)
    server: str = field(init=False)
    database: str = field(init=False)
    trusted_connection: str = field(init=False)
    config_override: InitVar[dict | None] = None
    conn: pyodbc.Connection = field(init=False, default=None)
    is_connected: bool = field(init=False, default=False)

    def __post_init__(self, config_override):
        if config_override is not None:
            self.server = config_override.get('server', self.config.get('DEFAULT', 'server'))
            self.database = config_override.get('database', self.config.get('DEFAULT', 'database'))
            self.trusted_connection = config_override.get('trusted_connection',
                                                          self.config.get('DEFAULT', 'trusted_connection'))
        else:
            self.server = self.config.get('DEFAULT', 'server')
            self.database = self.config.get('DEFAULT', 'database')
            self.trusted_connection = self.config.get('DEFAULT', 'trusted_connection')

    def open_connection(self):
        self.conn = pyodbc.connect(
            f'DRIVER=ODBC Driver 17 for SQL Server;'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'Trusted_Connection={self.trusted_connection}'
        )
        self.is_connected = True

    def verify_connection(self) -> bool:
        if not self.is_connected:
            self.open_connection()
        return self.is_connected

    def test_connection(self):
        try:
            self.verify_connection()
            cursor = self.conn.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchall()
            logger.info('Connection Successful')
        except Exception as e:
            logger.error(f'Connection Failed: {type(e).__name__}: {e}')
            self.close_connection()
            self.is_connected = False
            raise e

    def get_cursor(self) -> pyodbc.Cursor:
        if not self.is_connected:
            self.open_connection()
        return self.conn.cursor()

    @precursor
    def test_query(self, query: str, cursor=None):
        if cursor is None:
            raise ValueError('Cursor is None')
        cursor.execute(query)
        cursor.fetchall()
        logger.info('Connection Successfully passed cursor!')

    @precursor
    def test_temp_two_part(self, temp_table_name: str, cursor: pyodbc.Cursor = None):
        try:
            if not temp_table_name.startswith('#'):
                temp_table_name = f'#{temp_table_name}'
            cursor.execute(f"DROP TABLE IF EXISTS {temp_table_name};")
            cursor.execute(f'CREATE TABLE {temp_table_name} (id VARCHAR(30));')
            cursor.execute(f"INSERT INTO {temp_table_name} SELECT ('Hello Temp Table') UNION SELECT ('Still Hello');")
            cursor.execute(f'SELECT * FROM {temp_table_name};')
            result = cursor.fetchall()
            for index, r in enumerate(result):
                if isinstance(r, pyodbc.Row):
                    logger.info(f'Temp Table Result {index}: {r.id}')
            logger.info(f'Temp Table Result Column Names: {result[0].cursor_description}')
            logger.info(f'Temp Table Result: {result}')
            cursor.execute(f'DROP TABLE IF EXISTS {temp_table_name}')
            logger.info('Connection Successfully passed cursor!')
        except Exception as e:
            logger.error(f'Connection Failed: {type(e).__name__}: {e}')
            raise e

    @precursor
    def test_pyodbc_tables(self, table_name:str = None, cursor: pyodbc.Cursor = None):
        try:
            if table_name:
                tables = cursor.tables(table=table_name).fetchall()
                if len(tables) > 0:
                    for row in tables:
                        logger.info(f'Table Name: [{row.table_cat}].[{row.table_schem}].[{row.table_name}]')
                else:
                    logger.info(f'Table {table_name} Does Not Exist')
            else:
                logger.info('No Table Name Provided to Search')
                for row in cursor.tables():
                    logger.info(f'Table Name: {row.table_name}')
        except Exception as e:
            logger.error(f'Connection Failed: {type(e).__name__}: {e}')
            raise e

    @precursor
    def test_pyodbc_columns(self, catalog:str = None, schema:str = None, table_name:str = None, column:str = None, cursor: pyodbc.Cursor = None):
        try:
            rows = cursor.columns(table=table_name, catalog=catalog, schema=schema, column=column).fetchall()
            if len(rows) > 0:
                for row in rows:
                    column_name:str = row.column_name
                    for detail, value in zip(row.cursor_description, row):
                        if value is not None:
                            logger.info(f'Column {column_name} : {detail[0]}({detail[1]}): {value}')
            else:
                logger.info(f'No Columns Found for parameters: {catalog}, {schema}, {table_name}, {column}')
        except Exception as e:
            logger.error(f'Connection Failed: {type(e).__name__}: {e}')
            raise e


    def close_connection(self):
        if self.is_connected:
            self.conn.close()
            self.is_connected = False

    def __del__(self):
        self.close_connection()
        logger.info('Connection Closed')


def base_run_01():
    sql_conn = SqlConn()
    sql_conn.test_connection()
    del sql_conn
    logger.info('Connection Deleted')


def base_run_02():
    sql_conn = SqlConn()
    sql_conn.verify_connection()
    sql_conn.test_query(query='SELECT 1')
    sql_conn.test_query('SELECT 1')


def base_run_03():
    sql_conn = SqlConn()
    sql_conn.verify_connection()
    sql_conn.test_temp_two_part('HelloTable')
    del sql_conn
    logger.info('Base Run 03 Completed')

def base_run_04():
    sql_conn = SqlConn()
    # sql_conn.test_pyodbc_tables()
    sql_conn.test_pyodbc_tables('Person')

def base_run_05():
    sql_conn = SqlConn()
    sql_conn.test_pyodbc_columns(table_name='Person', schema='Person', catalog='AdventureWorks2022')

def base_run_06():
    sql_conn = SqlConn()
    sql_conn.test_pyodbc_columns(column='FirstName',table_name='Person', schema='Person', catalog='AdventureWorks2022')

def base_run_07():
    sql_conn = SqlConn()
    sql_conn.test_pyodbc_columns(column='Banana',table_name='Person', schema='Person', catalog='AdventureWorks2022')


if __name__ == '__main__':
    base_run_07()
