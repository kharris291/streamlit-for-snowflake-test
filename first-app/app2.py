import streamlit as st

st.title('Hierarchical Data Viewer')
st.header('Data Viewer')
st.subheader('subheader')
st.caption('caption')

st.write('this is write')
st.text('text')
st.code('v = variable()\nanother_call', "python")
st.markdown('**bold**')
st.divider()

st.latex('...')

st.error('this is error')
st.warning('this is warning')
st.info('this is information')
st.success('this is information')

st.balloons()
st.snow()