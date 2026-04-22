import streamlit as st

from ui.widgets import show_banner


def render() -> None:
    show_banner(
        "Pelatihan Project Deployment dengan Streamlit",
        "Versi main branch sengaja dibuat sederhana untuk live coding.",
    )

    st.markdown("### Tujuan sesi")
    st.markdown(
        """
        - Kenali struktur project
        - Jalankan aplikasi Streamlit
        - Isi placeholder sedikit demi sedikit saat demo
        """
    )

    st.info("TODO kelas: tambahkan metric, highlight, atau alur materi di halaman ini.")
