import json
from io import StringIO

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from modules import formats, charts, graphs, utils

st.set_page_config(layout="wide")
st.title('Hierarchical Data Viewer')
st.caption("Display you hierarchical data with charts and graphs.")


@st.cache_data(show_spinner="Loading the CSV file...")
def loadFile(filename):
    return pd.read_csv(filename, header=0).convert_dtypes()


with st.sidebar:
    tableName = st.text_input("Table name")
    if tableName is not None and len(tableName) > 0:
        df_original = utils.getDataFrame(f"select * from {tableName}")
    else:
        uploaded_file = st.file_uploader(
            "Upload a CSV file", type=["csv"], accept_multiple_files=False)

        if uploaded_file is not None:
            filename = StringIO(uploaded_file.getvalue().decode("utf-8"))
        else:
            file = 'employees.csv'
            filename = "data/employees.csv"

        df_original = loadFile(filename)

    cols = list(df_original.columns)
    child = st.selectbox("Child Column Name", cols, index=0)
    parent = st.selectbox("Parent Column Name", cols, index=1)
    df = df_original[[child, parent]]

    if st.user is not None and 'email' in st.user:
        st.markdown(f"user: {st.user.email}")


def OnShowList(filename):
    if "names" in st.session_state:
        these_filenames = st.session_state["names"]
        if filename in these_filenames:
            st.error("File already exists in the list.")
            st.stop()


if "names" in st.session_state:
    filenames = st.session_state["names"]
else:
    filenames = ["employees.csv"]
    st.session_state["names"] = filenames

tabSource, tabFormat, tabGraph, tabChart, tabAnimated = st.tabs(["Source", "Format", "Graph", "Chart", "Animated"])

chart = graphs.getEdges(df_original)

with tabSource:
    st.dataframe(df_original, use_container_width=True)

# show in another data format
with tabFormat:
    sel = st.selectbox(
        "Select a data format:",
        ["JSON", "XML", "YAML", "JSON Path", "JSON Tree"])

    root = formats.getJson(df)
    if sel == "JSON":
        jsn = json.dumps(root, indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "XML":
        xml = formats.getXml(root)
        st.code(xml, language="xml", line_numbers=True)
    elif sel == "YAML":
        yaml = formats.getYaml(root)
        st.code(yaml, language="yaml", line_numbers=True)
    elif sel == "JSON Path":
        jsn = json.dumps(formats.getPath(root, []), indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "JSON Tree":
        st.json(root)

with tabGraph:
    graph = graphs.getEdges(df)
    url = graphs.getUrl(graph)
    try:
        st.link_button("Visualize Online", url)
    except:
        pass
    st.graphviz_chart(graph)

# show as Plotly chart
with tabChart:
    labels = df[df.columns[0]]
    parents = df[df.columns[1]]

    sel = st.selectbox(
        "Select a chart type:",
        ["Treemap", "Icicle", "Sunburst", "Sankey"])
    if sel == "Treemap":
        fig = charts.makeTreemap(labels, parents)
    elif sel == "Icicle":
        fig = charts.makeIcicle(labels, parents)
    elif sel == "Sunburst":
        fig = charts.makeSunburst(labels, parents)
    elif sel == "Sankey":
        fig = charts.makeSankey(labels, parents)
    st.plotly_chart(fig, use_container_width=True)

# show as D3 animated chart
with tabAnimated:
    try:
        import modules.animated as animated

        sel = st.selectbox(
            "Select a D3 chart type:",
            ["Collapsible Tree", "Linear Dendrogram", "Radial Dendrogram", "Network Graph"])
        if sel == "Collapsible Tree":
            filename = animated.makeCollapsibleTree(df)
        elif sel == "Linear Dendrogram":
            filename = animated.makeLinearDendrogram(df)
        elif sel == "Radial Dendrogram":
            filename = animated.makeRadialDendrogram(df)
        elif sel == "Network Graph":
            filename = animated.makeNetworkGraph(df)

        with open(filename, 'r', encoding='utf-8') as f:
            components.html(f.read(), height=2200, width=1000)
    except:
        st.warning("Not supported.")
