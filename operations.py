from fenster.profile.configuration import xsc01_connection_string, e0ape002_connection_string, \
    display_database_logging_in_terminal, secret
from fenster.security.encryption.ciphers import xor_cipher
from fenster.database.common.models import StatisticalDataTableModels, CustomDataTableModels
from fenster.uttilties.exceptions import DatabaseConnectionCannotBeSpawned
from sqlalchemy_utils import database_exists
from sqlalchemy.engine import create_engine
from sqlalchemy import inspect


class CommonDatabaseContextManager(StatisticalDataTableModels, CustomDataTableModels):
    """

    """
    @staticmethod
    def spawn_engine(logical_database_name: str) -> object:
        """
        Will spawn and engine which can be used to control the target database.
        :param logical_database_name: The logical database name
        :return: an SQLAlchemy engine object to create a connection
        """
        if logical_database_name == "---":
            connection_url = xsc01_connection_string

        elif logical_database_name == "---":
            connection_url = e0ape002_connection_string

        else:
            raise DatabaseConnectionCannotBeSpawned()

        return create_engine(
            xor_cipher(
                string=connection_url,
                key=secret
            ),
            echo=display_database_logging_in_terminal,
            max_identifier_length=128
        )

    @staticmethod
    def close_connection(connection: object) -> None:
        """
        Will close the connection and give it back to the connection pool.
        :param connection: The active connection object.
        """
        connection.close()

    @staticmethod
    def execute_statement(connection: object, payload: list, bulk_insert=False) -> tuple:
        """
        Will shoot a SQLAlchemy query or raw sql over an active SQL connection.
        :param bulk_insert:
        :param connection: An open connection object.
        :param payload: The payload either a SQLAlchemy statement or query
        :return: The results object.
        """
        if bulk_insert:
            connection.execute(payload[0], payload[1])

        else:
            return connection.execute(payload)

    def check_if_table_exists(self, logical_database_name: str, table_name: str) -> bool:
        """
        Will verify if a table exists in the target database
        :param logical_database_name: The logical database name
        :param table_name:
        :return: a bool which is either true or false
        """
        engine = self.spawn_engine(logical_database_name)
        return inspect(engine).has_table(table_name)

    def check_if_database_exists(self, logical_database_name: str) -> bool:
        """
        Will verify if a table exists in the target database platform.
        :param logical_database_name: The logical database name.
        :return: a bool which is either true or false
        """
        engine = self.spawn_engine(logical_database_name)
        database_exists(repr(engine.url))

    def spawn_table(self, logical_database_name: str, schema: object) -> None:
        """
        Spawn an table in the target database.
        :param logical_database_name: The logical database name
        :param schema: The table schema which is used to describe the table.
        :return:
        """
        engine = self.spawn_engine(logical_database_name)
        schema.metadata.create_all(engine)
        engine.dispose()

    def drop_table(self, logical_database_name: str, schema: object) -> None:
        """
        Drop a table in the target database.
        :param logical_database_name: The logical database name
        :param schema: The table schema which is used to describe the table.
        :return:
        """
        engine = self.spawn_engine(logical_database_name)
        schema.drop(engine)
        engine.dispose()

    def spawn_connection(self, logical_database_name) -> tuple:
        """
        Will spawn an connection to the database.
        :param logical_database_name: The logical database name
        :return: An active connection.
        """
        engine = self.spawn_engine(logical_database_name)
        return engine, engine.connect()


class CommonDatabaseOperations(CommonDatabaseContextManager):
    """

    """
    def select(self, logical_database_name: str, query: object) -> object:
        """
        Will perform an generic read statement on the selected database
        and return the results object.
        :return: an sqlalchemy results object.
        """
        # Creating connection
        engine, connection = self.spawn_connection(logical_database_name)

        # Executing statement and binding results to variable
        results = self.execute_statement(connection, query)

        # Closing connection
        self.close_connection(connection)
        return results

    def insert(self, logical_database_name: str, table: object, payload: list) -> None:
        """
        Will use bulk insert to insert data into a database.
        :param table: The table where the data needs to go.
        :param logical_database_name: The logical database name
        :param payload: A list of dictionaries that gets inserted into a database.
        """
        # Creating connection
        engine, connection = self.spawn_connection(logical_database_name)

        # Building insert command.
        statement = table.insert()

        # Executing inserting payload.
        self.execute_statement(connection, [statement, payload], bulk_insert=True)

        # Closing connection.
        self.close_connection(connection)
