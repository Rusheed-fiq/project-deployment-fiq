import pandas as pd
import streamlit as st


@st.cache_data
def generate_dummy_kpi_data() -> pd.DataFrame:
    """Placeholder data untuk latihan dashboard."""
    return pd.DataFrame(
        [
            {"unit": "DJP", "layanan": "NPWP", "jumlah_permohonan": 120, "success_rate": 0.95},
            {"unit": "DJBC", "layanan": "Billing", "jumlah_permohonan": 80, "success_rate": 0.91},
            {"unit": "DJPb", "layanan": "Perbendaharaan", "jumlah_permohonan": 65, "success_rate": 0.93},
        ]
    )


@st.cache_data
def slow_aggregate(data: pd.DataFrame, by_col: str) -> pd.DataFrame:
    """Placeholder agregasi sederhana untuk demo cache."""
    if by_col not in data.columns:
        return pd.DataFrame()

    return (
        data.groupby(by_col, as_index=False)
        .agg(
            total_permohonan=("jumlah_permohonan", "sum"),
            rata_success_rate=("success_rate", "mean"),
        )
        .sort_values("total_permohonan", ascending=False)
    )
