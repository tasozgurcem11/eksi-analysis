import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlite3
from sqlite3 import Error
import math
from sqlalchemy import inspect
import psycopg2.extras
import psycopg2

class PGSQLConnection:
    """
    Main class for the database connection.
    Functions for creating tables, uploading data, reading data, etc.
    Possible connection types:
        +Bitdotio
        +POSTGRESQL Database
        +SQLite

    """

    def __init__(self, conn_type='postgresql', api_key='', conn_url='', sqlite_path=None, config=''):
        self.conn_url = conn_url
        self.config = config
        self.api_key = api_key
        self.conn_type = conn_type
        self.sqlite_path = sqlite_path


        if conn_type == 'postgresql':
            self.engine = create_engine(
                conn_url,
                execution_options={
                    "isolation_level": "REPEATABLE READ"
                },
                connect_args={"options": "-c statement_timeout=55000"}
            )

        elif conn_type == 'sqlite':
            """ create a database connection to a SQLite database """
            conn = None
            try:
                conn = sqlite3.connect(sqlite_path)
                print(sqlite3.version)

            except Error as e:
                print(e)

            if conn:
                self.conn = conn

    def execute(self, input_query):
        if self.conn_type == 'bitdotio':
            cur = self.engine.cursor()
            cur.execute(input_query)
            print(cur.fetchone())
            cur.close()

        else:
            print('conn_type is not bitdotio')

    #### --- Retired --- ####
    # def connection(self):
    #     conn = self.engine.raw_connection()
    #     return conn

    def get_table(self, table_name, cols=None, constraint='', limit=0):
        """
        Creates dataframe from the DB table.
        :return: dataframe object after query
        :param table_name:
        :param cols:
        :param constraint:
        :param limit:
        """

        # Select cols to query
        if cols:
            query_columns = cols[0]

            if cols[1:]:
                for col in cols[1:]:
                    query_columns += f',{col}'

        else:
            query_columns = '*'

        # Add if there are constraints:
        if constraint:
            constraint_str = ' WHERE ' + constraint

        else:
            constraint_str = ''

        limit_str = ''
        # Add limit:
        if limit > 0:
            limit_str = f' LIMIT {str(limit)}'

        # Create query to read table:
        table_query = f"SELECT " + query_columns + ' FROM ' + table_name + constraint_str + limit_str
        print(table_query)

        # Read table:
        table_df = pd.read_sql(table_query, self.engine)

        # Apply limit:
        if limit > 0:
            if limit > table_df.shape[0]:
                print('Limit defined is bigger than table size')
            else:
                table_df = table_df.iloc[:limit]

        return table_df

    def upload_table(self, input_df, table_name, batch_size=10000, reset_table=False, auto_id=False, data_append=True):
        """
        Uploads table to the database
        :param input_df:
        :param table_name:
        """
        current_df = self.get_table(table_name)

        if data_append:
            input_df.to_sql(table_name, con=self.engine, index=False, if_exists='append')

        else:
            if reset_table:
                upload_df = input_df.copy()

            else:
                upload_df = pd.concat([current_df, input_df])
                if auto_id:
                    upload_df = upload_df.reset_index(drop=True)
                    upload_df['id'] = upload_df.index


            print(f'Uploading table: {table_name}')
            if upload_df.shape[0] > batch_size:
                # Merges data to make upload process robust:
                number_of_batch = int(math.ceil(upload_df.shape[0] / batch_size))
                batch_list = np.array_split(upload_df, number_of_batch)
                print(f"Total number of batch: {str(len(batch_list))}")

                i = 0
                for batch in batch_list:
                    i = i + 1
                    if i == 1:
                        """
                        Upload first batch by replacing previous data.
                        """
                        batch.to_sql(table_name, con=self.engine, index=False, if_exists='replace')

                    else:
                        batch.to_sql(table_name, con=self.engine, index=False, if_exists='append')

            else:
                upload_df.to_sql(table_name, con=self.engine, index=False, if_exists='replace')



    def insert_data(self, input_df, table_name):
        """
        Uploads table to the database
        :param input_df:
        :param table_name:
        """

        df_columns = list(input_df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        # create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table_name, columns, values)

        cur = self.conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, input_df.values)
        self.conn.commit()
        cur.close()


        # # Use INSERT to upload data:
        # for index, row in input_df.iterrows():
        #     insert_query = f"INSERT INTO {table_name} VALUES ({row.to_json()})"
        #     with self.engine.connect() as conn:
        #         conn.execute(insert_query)




    def drop_view(self, view_name):
        """
        Drops view from the database
        :param view_name:
        """
        drop_view_query = f"DROP VIEW IF EXISTS {view_name}"
        with self.engine.connect() as conn:
            conn.execute(drop_view_query)

    def drop_table(self, table_name):
        """
        Drops table from the database
        :param table_name:
        """
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        with self.engine.connect() as conn:
            conn.execute(drop_table_query)

    def create_view_from_query(self, view_name, query):
        """
        Creates view in the database
        :param view_name:
        :param query:
        """
        create_view_query = f"CREATE VIEW {view_name} AS {query}"
        with self.engine.connect() as conn:
            conn.execute(create_view_query)

    def create_table_from_query(self, table_name, query):
        """
        Creates table in the database
        :param table_name:
        :param query:
        """
        create_table_query = f"CREATE TABLE {table_name} AS {query}"
        with self.engine.connect() as conn:
            conn.execute(create_table_query)

    def get_all_table_names(self):
        """
        Returns all table names in the database
        :return:
        """
        table_list = []

        inspector = inspect(self.engine)
        schemas = inspector.get_schema_names()
        for schema in schemas:
            if schema == 'public':
                for table_name in inspector.get_table_names(schema=schema):
                    table_list.append(table_name)

        return table_list
