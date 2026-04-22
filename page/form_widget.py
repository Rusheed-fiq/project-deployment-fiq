from ui.widgets import banner
import pandas as pd
import streamlit as st

from services import (
    DEFAULT_MESSAGE_API_BASE_URL,
    MessageService,
    MessageServiceError,
)


def render() -> None:
    banner(
        "Form Widget",
        "Demo form untuk mengirim dan mengambil data dari endpoint say-hello.",
    )

    st.subheader("Konfigurasi Endpoint")
    base_url = st.text_input(
        "Base URL API",
        value=DEFAULT_MESSAGE_API_BASE_URL,
        help="Default diarahkan ke endpoint training.",
    )
    api_key = st.text_input(
        "x-api-key",
        type="password",
        help="Isi API key jika endpoint mewajibkan autentikasi.",
    )

    service = MessageService(base_url=base_url, api_key=api_key or None)

    st.divider()
    st.subheader("1) Form Kirim Data (POST /api/say-hello)")

    with st.form("post_hello_form"):
        nama = st.text_input("Nama", placeholder="Budi")
        message = st.text_area("Message", placeholder="Halo dari Streamlit!")
        submit_post = st.form_submit_button("Kirim Data", type="primary")

    if submit_post:
        try:
            post_result = service.post_message(nama=nama, message=message)
            st.success("Data berhasil dikirim ke endpoint.")
            st.json(post_result)
        except MessageServiceError as err:
            st.error(str(err))

    st.divider()
    st.subheader("2) Ambil Data (GET /api/say-hello?limit=...)")

    col_limit, col_action = st.columns([2, 1])
    with col_limit:
        limit = st.slider("Limit data", min_value=1, max_value=100, value=20)
    with col_action:
        fetch = st.button("Ambil Data", width="stretch")

    if fetch:
        try:
            get_result = service.get_messages(limit=limit)
            st.success("Data berhasil diambil.")
            st.json(get_result)

            items = get_result.get("data", []) if isinstance(get_result, dict) else []
            if isinstance(items, list) and items:
                st.dataframe(pd.DataFrame(items), width="stretch")
            else:
                st.info("Belum ada data yang ditampilkan dari endpoint.")
        except MessageServiceError as err:
            st.error(str(err))

    st.divider()
    st.markdown(
        """
Contoh endpoint yang dipakai:
- `POST /api/say-hello` dengan body `{"nama":"Budi","message":"Halo dari Streamlit!"}`
- `GET /api/say-hello?limit=20`
"""
    )
