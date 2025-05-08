import os

from snowflake.snowpark import Session

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

session = Session.builder.configs(connection_parameters).create()

df = session.sql("SELECT * FROM EMPLOYEES")
rows = df.collect()
for row in rows:
    print(row)


dfp = df.to_pandas()
print(dfp)