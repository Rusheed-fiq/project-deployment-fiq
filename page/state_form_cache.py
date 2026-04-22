import streamlit as st

from services.dummy_data import generate_dummy_kpi_data, slow_aggregate
from ui.widgets import show_banner


def render() -> None:
    show_banner(
        "State, Form, dan Cache",
        "Versi ini hanya berisi contoh dasar yang mudah diperluas saat demo.",
    )

    if "klik_counter" not in st.session_state:
        st.session_state.klik_counter = 0

    if st.button("Tambah counter"):
        st.session_state.klik_counter += 1

    st.write(f"Counter: **{st.session_state.klik_counter}**")

    with st.form("form_demo"):
        nama_proyek = st.text_input("Nama proyek")
        submit = st.form_submit_button("Simpan")

    if submit:
        st.success(f"Placeholder form tersimpan: {nama_proyek}")

    data = generate_dummy_kpi_data()
    agg = slow_aggregate(data, "unit")
    st.dataframe(agg, use_container_width=True)

    st.caption("TODO kelas: tambah field form, session_state lain, dan demo cache lebih jelas.")
