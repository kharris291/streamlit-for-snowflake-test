import configparser
import os

import pandas as pd
import streamlit as st
from snowflake.snowpark import Session


def getFullPath(filename):
    crtdir = os.path.dirname(__file__)
    pardir = os.path.abspath(os.path.join(crtdir, os.pardir))
    return f"{pardir}/{filename}"


# @st.cache_resource(max_entries=10)
def getSession():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser("~"), ".snowsql/config"))
    section = f"connections.demo_conn"
    print(os.path.join(os.path.expanduser("~"), ".snowsql/config"))
    pars = {
        "account": parser.get(section, "accountname"),
        "user": parser.get(section, "username"),
        "password": os.environ["SNOWSQL_PWD"],
        "database": parser.get(section, "database"),
        "schema": parser.get(section, "schema"),
        "role": parser.get(section, "role"),
        "warehouse": parser.get(section, "warehouse")
    }
    return Session.builder.configs(pars).create()


@st.cache_data(ttl=3600, show_spinner="Running a Snowflake query...")
def getDataFrame(query):
    conn = getSession()
    rows = conn.sql(query).collect()

    return pd.DataFrame(rows).convert_dtypes()
