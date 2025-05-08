import os

import snowflake.connector

conn = snowflake.connector.connect(
    account='xc75649.eu-west-2.aws',
    user='kevinharrisdiaceutics',
    password=os.environ['SNOWSQL_PWD'],
    database='TESTS',
    schema='PUBLIC',
    warehouse='COMPUTE_WH',
    role='ACCOUNTADMIN',
)

cur = conn.cursor()
cur.execute('SELECT * from tests.public.employees')

# for row in cur:
#     print(row)

df = cur.fetch_pandas_all()
print(df)
