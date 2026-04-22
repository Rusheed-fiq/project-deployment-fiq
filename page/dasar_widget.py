import streamlit as st

from ui.widgets import show_banner


def render() -> None:
    show_banner(
        "Modul Dasar dan Widget",
        "Halaman ini disiapkan sebagai kanvas latihan widget dasar.",
    )

    st.markdown("### Contoh widget minimal")
    nama = st.text_input("Nama peserta", value="")
    setuju = st.checkbox("Saya siap praktik")
    level = st.slider("Level pemahaman Streamlit", 1, 10, 5)

    if st.button("Tampilkan hasil", type="primary"):
        st.write({"nama": nama, "siap": setuju, "level": level})

    st.caption("TODO kelas: tambah selectbox, multiselect, columns, dan expander.")
