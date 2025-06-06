import urllib.parse
from io import StringIO

import pandas as pd
import streamlit as st


def getGraph(df):
    edges = ''
    for _, row in df.iterrows():
        if not pd.isna(row.iloc[1]):
            edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'
    return f'digraph {{\n{edges}}}'


@st.cache_data
def loadFile(filename):
    return pd.read_csv(filename, header=0).convert_dtypes()


def OnShowList(filename):
    if "names" in st.session_state:
        these_filenames = st.session_state["names"]
        if filename in these_filenames:
            st.error("File already exists in the list.")
            st.stop()


st.title('Hierarchical Data Viewer')

if "names" in st.session_state:
    filenames = st.session_state["names"]
else:
    filenames = ["employees.csv"]
    st.session_state["names"] = filenames

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"], accept_multiple_files=False)
if uploaded_file is not None:
    filename = StringIO(uploaded_file.getvalue().decode('utf-8'))
    file = uploaded_file.name
    if file not in filenames:
        filenames.append(file)
        st.session_state["names"] = filenames
        st.sidebar.write("File uploaded successfully.")
else:
    file= 'employees.csv'
    filename = "data/employees.csv"

st.sidebar.write(file)

btn = st.sidebar.button("Show list",
                        on_click=OnShowList, args=(file,))
if btn:
    for f in filenames:
        st.sidebar.write(f)

df_original = loadFile(filename)
cols = list(df_original.columns)
with st.sidebar:
    child = st.selectbox("Child column name", cols, index=0)
    parent = st.selectbox("Parent column name", cols, index=1)
    df = df_original[[child, parent]].copy()

tabs = st.tabs(["Source", "Graph", "Dot Chart"])

chart = getGraph(df)

with tabs[0]:
    st.dataframe(df)

with tabs[1]:
    tabs[1].graphviz_chart(chart, use_container_width=True)

with tabs[2]:
    st.code(chart)
    url = f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(chart)}'
    st.link_button("Open in Graphviz Visual Editor", url=url)
