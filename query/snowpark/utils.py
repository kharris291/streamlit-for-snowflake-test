import os

from snowflake.snowpark import Session


def get_connector():
    # Create a session
    connection_parameters = {
        "account": "xc75649.eu-west-2.aws",
        "user": "kevinharrisdiaceutics",
        "password": os.environ["SNOWSQL_PWD"],
        "database": "TESTS",
        "schema": "PUBLIC",
        "warehouse": "COMPUTE_WH",
        "role": "ACCOUNTADMIN",
    }

    return Session.builder.configs(connection_parameters).create()
