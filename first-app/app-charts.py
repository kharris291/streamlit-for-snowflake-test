import urllib.parse

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.title('Hierarchical Data Charts')

df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()
# st.dataframe(df)

labels = df[df.columns[0]]
parents = df[df.columns[1]]

data = go.Treemap(
    ids=labels,
    labels=labels,
    parents=parents,
    root_color='lightgrey',
)
fig = go.Figure(data)

st.plotly_chart(fig, use_container_width=True)

data2 = go.Icicle(
    ids=labels,
    labels=labels,
    parents=parents,
    root_color='lightgrey',
)
fig2 = go.Figure(data2)
st.plotly_chart(fig2, use_container_width=True)

data3 = go.Sunburst(
    ids=labels,
    labels=labels,
    parents=parents,
    root_color='lightgrey',
)
fig3 = go.Figure(data3)
st.plotly_chart(fig3, use_container_width=True)

data = go.Sankey(
    node=dict(label=labels),
    link=dict(
        source=[list(labels).index(x) for x in labels],
        target=[-1 if pd.isna(x) else list(labels).index(x) for x in parents],
        label=labels,
        value=list(range(1, len(labels)))))
fig = go.Figure(data)
st.plotly_chart(fig, use_container_width=True)

