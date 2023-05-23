import logging
import os
import pathlib
import re
import time
import pandas as pd
from typing import Callable, List, Dict


import s3fs
import sqlalchemy
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)


class SQLConnector:
    def __init__(self, engine, host, port, user, password, database=None, driver=None, service_name=None):

        self.engine = self._create_engine(engine, host, port, user, password, database, driver, service_name)
        self.session_maker = sessionmaker(bind=self.engine)

    @staticmethod
    def _create_engine(engine, host, port, user, password, database=None, driver=None, service_name=None) -> sqlalchemy.engine.Engine:
        str_engine = f"{engine}://{user}:{password}@{host}:{port}"

        if database is not None:
            str_engine = f"{str_engine}/{database}"
        if driver is not None:
            str_engine = f"{str_engine}?driver={driver}"
        if service_name is not None:
            str_engine = f"{str_engine}/?service_name={service_name}"

        if engine == "mssql+pyodbc":
            return sqlalchemy.create_engine(str_engine, pool_pre_ping=True, fast_executemany=True)
        else:
            return sqlalchemy.create_engine(str_engine, pool_pre_ping=True)

    def read_table_in_memory(self, table_name: str, table_fields: List[str] = ["*"]) -> pd.DataFrame:
        table = pd.read_sql_query(
            f"select {','.join(table_fields)} from {table_name}", con=self.engine
        )
        return table

    def upload_table(
            self,
            df: pd.DataFrame,
            table_name: str,
            schema="dbo",
            if_exists="replace",
            index=False,
            **kwargs):
        # https://stackoverflow.com/questions/50645445/python-pandas-to-sql-maximum-2100-parameters
        # max_params_load = 2100
        # chunksize = max(int(np.floor(max_params_load / max(len(df.columns), 1))) - 1, 1)
        df.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists=if_exists,
            index=index,
            **kwargs)

    def execute_statement(self, statement):
        """Execute statement

        Args:
            statement (string): Statement to execute
        """
        session = self.session_maker()
        try:
            result = session.execute(statement)
            session.commit()
        finally:
            session.close()
        return result

    def bulk_load_file_to_table(self, filepath: str, table_name: str, sep: str = ","):
        """
        This function allows to perform a bulk load from a csv file to a table
        Args:
            filepath: path of the csv file (ends with .csv)
            table_name: table name in the form of schema.table
            sep: csv separator

        Returns:

        """
        # Build connection
        raw_connection = self.engine.raw_connection()
        cursor = raw_connection.cursor()
        # Define copy query
        copy_query = f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER '{sep}'"

        # Use vanilla open or s3 open depending on filepath
        open_func = self._get_open_function(filepath)

        # Bulk load file
        with open_func(filepath, "r") as file:
            cursor.copy_expert(copy_query, file)
            raw_connection.commit()
        # Close connection
        raw_connection.close()
        return None

    def dump_table_to_file(self, table_name: str, filepath: str, sep: str = ","):
        """
        This function allows to directly dump a table into a local file without having to read it into memory

        Args:
            table_name: name of the table to be dumped
            filepath: destination path of the file (should end in .csv)
            sep: separator

        Returns: nothing

        """

        # Build query
        copy_query = f"COPY {table_name} TO STDOUT WITH CSV HEADER DELIMITER '{sep}'"

        # Initialize cursor
        raw_connection = self.engine.raw_connection()
        cursor = raw_connection.cursor()

        # Use vanilla open or s3 open depending on filepath
        open_func = self._get_open_function(filepath)

        # Perform copy
        with open_func(filepath, "wb") as file_dump:
            cursor.copy_expert(copy_query, file_dump)

        # Close connection to database
        raw_connection.close()

        return None

    def execute_script(self, sql_script_path: str, from_query_id: int = 0):
        """
        Executes script from sql file
        Args:
            sql_script_path: path where the sql script is located
            from_query_id: Start on which query

        Returns:

        """
        # Open sql file
        file = open(sql_script_path)
        # Read sql file
        sql_text = file.read()
        list_sql_queries = self.clean_sql_string(sql_text)
        # Close file
        file.close()
        # Execute query
        for query_id in range(len(list_sql_queries))[from_query_id:]:
            log.info(f"Running query: {query_id}")
            log.info(f"Query: {list_sql_queries[query_id].text[:100]}")
            self.engine.execute(list_sql_queries[query_id])
            time.sleep(0.1)
        return None

    @staticmethod
    def clean_sql_string(sql_text: str) -> List[sqlalchemy.sql.expression.TextClause]:
        # Remove multi line comments
        lines_no_comments = re.sub("/\*[^/\*]+\*/", "", sql_text, flags=re.DOTALL)
        # Remove -- single line comments
        lines = lines_no_comments.split("\n")
        uncommented_lines = [
            line for line in lines if not line.lstrip().startswith("--")
        ]
        cleaned_text = "\n".join(uncommented_lines)
        # Build escaped sql
        sql_queries = cleaned_text.split(";")
        # If script ends with ";" remove last character
        sql_queries = [
            query
            for query in sql_queries
            if not bool(re.search("^( +)+$", query))
            and not bool(re.search("^(\n+)+$", query))
            and not query == ""
        ]
        escaped_sql = [sqlalchemy.text(query) for query in sql_queries]
        return escaped_sql

    def execute_multiple_scripts(self, sql_script_list: str):
        """
        Allows to execute multiple scripts
        Args:
            sql_script_list: list of paths to scripts

        Returns:

        """
        for sql_script in sql_script_list:
            self.execute_script(sql_script)
            time.sleep(0.1)
        return None

    @staticmethod
    def _get_open_function(filepath: str) -> Callable:
        # Use vanilla open usually
        open_func = open
        # If path lives in s3, use s3fs open function
        if pathlib.Path(filepath).parts[1][0:3] == "s3-":
            s3 = s3fs.S3FileSystem(anon=False)
            open_func = s3.open
        return open_func

    def class_iterate(self, function_name: str, dict_input: Dict):
        attribute_call = self.__getattribute__(function_name)
        for input_object in dict_input.keys():
            attribute_call(**dict_input[input_object])

    def drop_foreign_key(self, table_name: str, column_name: str, foreign_column: str):
        sql_string = f"""
                    ALTER TABLE {table_name}
                    DROP CONSTRAINT FK_{table_name}_{column_name}_{foreign_column}
        """

        self.execute_statement(sql_string)

    def create_foreign_key(
            self,
            table_name: str,
            column_name: str,
            foreign_table: str,
            foreign_column: str
    ):
        sql_string = f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT FK_{table_name}_{column_name}_{foreign_column} FOREIGN KEY ({column_name})
        REFERENCES {foreign_table} ({foreign_column})
        ON DELETE NO ACTION
        ON UPDATE NO ACTION"""

        self.execute_statement(sql_string)

    def create_primary_key(self, table_name: str, column_name: str, column_type: str):

        not_nullable_string = f"""ALTER TABLE {table_name} ALTER COLUMN {column_name} {column_type} NOT NULL"""
        self.execute_statement(not_nullable_string)

        primary_key_string = f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT PK_{table_name}_{column_name} PRIMARY KEY ({column_name})"""
        self.execute_statement(primary_key_string)

    def make_column_unique(self, table_name: str, column_name: str):

        unique_str = f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT {column_name}_unique unique ({column_name})"""
        self.execute_statement(unique_str)

    def truncate_table(self, table_name: str):
        str = f"TRUNCATE TABLE {table_name}"
        self.execute_statement(str)

    def truncate_multiple(self, list_tables: List[str]):

        for table in list_tables:
            self.truncate_table(table)

    def check_if_table_exists(self, table_name: str) -> bool:
        tables = self.read_table_in_memory("information_schema.tables")
        tables = tables[tables["TABLE_NAME"] == table_name]
        return tables.shape[0] > 0


class DataMigrationAPI:
    def __init__(self, sql_table_name, temp_path, connector):
        self.dbfs_exe = "/home/ubuntu/anaconda3/envs/dbconnect/bin/dbfs"
        self.connector = connector
        self.sql_table_name = sql_table_name
        self.table_name = sql_table_name.replace(".", "_")
        self.csv_path = os.path.join(temp_path, f"{self.table_name}.csv")
        self.gzip_path = os.path.join(temp_path, f"{self.table_name}.zip")

    def send_to_databricks(self, databricks_folder):
        """

        Args:
            databricks_folder:

        Returns:

        """
        log.info(f"Initialize migration of table {self.table_name}")
        log.info("Dump: Start")
        self.connector.dump_table_to_file(self.sql_table_name, self.csv_path)
        log.info(f"Dumped table to: {self.csv_path}")
        log.info("Dump: End")

        log.info(f"Compression: Start")
        self.compress_file()
        log.info(f"Compressed table in {self.gzip_path}")
        log.info(f"Compression: End")

        log.info("Send to databricks: Start")
        self.copy_to_databricks(databricks_folder)
        log.info(f"Sent to {os.path.join(databricks_folder, self.table_name + '.zip')}")
        log.info("Send to databricks: End")

        log.info("Remove temporary files: Start")
        os.remove(self.csv_path)
        os.remove(self.gzip_path)
        log.info("Remove temporary files: End")
        log.info(
            f"Table {self.table_name} successfully sent to"
            f" {os.path.join(databricks_folder, self.table_name + '.zip')}"
        )

    def compress_file(self):
        os.system(f"zip {self.gzip_path} {self.csv_path}")

    def copy_to_databricks(self, databricks_folder):
        databricks_path = os.path.join(databricks_folder, self.table_name + ".zip")
        os.system(f"{self.dbfs_exe} cp {self.gzip_path} {databricks_path}")
