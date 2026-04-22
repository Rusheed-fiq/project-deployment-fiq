import streamlit as st

from ui.widgets import show_banner


def render() -> None:
    show_banner(
        "Modul Deployment",
        "Checklist ini sengaja ringkas agar pengajar bisa melengkapinya saat sesi.",
    )

    st.markdown("### Checklist awal")
    st.markdown(
        """
        1. Pastikan `app.py` bisa dijalankan lokal.
        2. Pastikan dependency ada di `requirements.txt` atau `pyproject.toml`.
        3. Jangan commit file secret.
        4. Siapkan target deploy.
        """
    )

    st.code(
        "streamlit run app.py --server.port 8501 --server.address 0.0.0.0",
        language="bash",
    )

    st.info("TODO kelas: tambahkan opsi deploy, Dockerfile, atau langkah Streamlit Community Cloud.")
