import sqlite3
import numpy as np

from data.const import DATABASE


class SQLite_execute:
    def __init__(self):
        self.db_file = DATABASE

    def __create_connection(self):
        """
                Create a database connection to the SQLite database specified
                by db_file.
            :param db_file: database file
            :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as error:
            return str(error)

        return conn

    def create_tables(self, sql: str) -> str:
        """
                Insert the data in the tables named projects and tasks.
            :param database: Path to database
            :param sql: Command to create a table
            :return: None
        """
        # create a database connection
        conn = self.__create_connection()

        # create tables
        e = 'Unable to open database file'
        if conn != e:
            try:
                # create table
                c = conn.cursor()
                c.execute(sql)
                return "Foi"
            except sqlite3.Error as error:
                return str(error)

        else:
            return "Error! cannot create the database connection."

    def execute_table(self, sql: str) -> int:
        """
                Create a new project into the projects table
            :param sql: The command to executable data
            :return: project id
        """
        # create a database connection
        conn = self.__create_connection()

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

    def select_table(self, sql: str) -> list:
        """
                Query all rows in the tasks table
            :param sql: The command to select data
            :return: print
        """
        # create a database connection
        conn = self.__create_connection()

        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()

        return rows

    def database_info(self) -> dict:
        sql = "SELECT * FROM sqlite_master"
        database_tables = self.select_table(sql)
        table_names = [tables[1] for tables in database_tables]

        table_info = {}
        for name in table_names:
            try:
                sql = f"PRAGMA table_info({name})"
                info = np.array(self.select_table(sql))[:, [1]]
                info = info.reshape(1, -1)[0]
                info = list(info)
            except Exception:
                info = []

            try:
                sql_2 = f"SELECT id FROM {name}"
                elements = self.select_table(sql_2)[-1][0]
            except Exception:
                elements = []

            table_info[name] = {
                "colunas": info,
                "num_instancias": elements
            }

        return table_info

    def edita_banco(self) -> int:
        id_min = 751
        id_max = 1_154
        sql = f"DELETE FROM vendas WHERE id BETWEEN {id_min} and {id_max}"
        retorno = self.execute_table(sql)
        return retorno

    def sql_table_vendas(self) -> str:
        vendas = """
                    CREATE TABLE IF NOT EXISTS vendas (
                        id integer PRIMARY KEY,
                        curr_date text DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        cod text NOT NULL,
                        descr text NOT NULL,
                        custo float NOT NULL,
                        unit float NOT NULL,
                        qtde float NOT NULL,
                        desconto float NOT NULL,
                        liquido float NOT NULL,
                        vendas float NOT NULL,
                        classe text NOT NULL,
                        data text NOT NULL
                    );
            """
        return vendas
