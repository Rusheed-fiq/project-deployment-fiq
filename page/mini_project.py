import streamlit as st

from services.dummy_data import generate_dummy_kpi_data
from ui.widgets import show_banner


def render() -> None:
    show_banner(
        "Mini Project",
        "Template dashboard sederhana untuk dikembangkan bersama peserta.",
    )

    data = generate_dummy_kpi_data()
    unit_options = sorted(data["unit"].unique())
    unit_filter = st.multiselect("Filter unit", unit_options, default=unit_options)

    filtered = data[data["unit"].isin(unit_filter)]

    st.metric("Total permohonan", int(filtered["jumlah_permohonan"].sum()))
    st.dataframe(filtered, use_container_width=True)

    st.caption("TODO kelas: tambah chart, filter layanan, download CSV, dan metrics tambahan.")
