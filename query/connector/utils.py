import os

import snowflake.connector


def get_connector ():
    return snowflake.connector.connect(
        account='xc75649.eu-west-2.aws',
        user='kevinharrisdiaceutics',
        password=os.environ['SNOWSQL_PWD'],
        database='TESTS',
        schema='PUBLIC',
        warehouse='COMPUTE_WH',
        role='ACCOUNTADMIN',
    )