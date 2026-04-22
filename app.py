import streamlit as st

from core.theme import apply_kemenkeu_theme, setup_page
from page import beranda, dasar_widget, deployment, endpoint_llm, mini_project, state_cache, form_widget

setup_page()
apply_kemenkeu_theme()

pages = [
    st.Page(beranda.render, title="Beranda", icon=":material/home:", url_path="beranda"),
    st.Page(dasar_widget.render, title="Dasar & Widget", icon=":material/widgets:", url_path="dasar-widget"),
    st.Page(state_cache.render, title="State & Cache", icon=":material/tune:", url_path="state-cache"),
    st.Page(form_widget.render, title="Form widget", icon=":material/note:", url_path="form-widget"),
    st.Page(mini_project.render, title="Mini Project", icon=":material/dashboard:", url_path="mini-project"),    
    st.Page(endpoint_llm.render, title="Endpoint LLM", icon=":material/smart_toy:", url_path="endpoint-llm"),
    st.Page(deployment.render, title="Deployment", icon=":material/rocket_launch:", url_path="deployment"),
]

st.navigation(pages, position="top").run()
