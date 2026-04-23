from __future__ import annotations

import io
import warnings
from datetime import datetime
from typing import Any, cast

import pandas as pd
import requests
import streamlit as st
from urllib3.exceptions import InsecureRequestWarning
from ui.widgets import banner

# Suppress SSL warnings for development
warnings.simplefilter("ignore", InsecureRequestWarning)

ENDPOINT = "https://training.ekos.my.id/api/tax-revenue-dashboard"


@st.cache_data
def load_data(
    province: str | None = None,
    tax_type: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
) -> pd.DataFrame:
    """
    Load data dari API dengan caching.
    
    Args:
        province: Filter provinsi (opsional)
        tax_type: Filter jenis pajak (opsional)
        year_min: Tahun minimum (opsional)
        year_max: Tahun maksimum (opsional)
    
    Returns:
        DataFrame dengan data yang sudah dinormalisasi
    """
    try:
        # Build parameters
        params: dict[str, Any] = {}
        if province and province != "Semua":
            params["province"] = province
        if tax_type and tax_type != "Semua":
            params["type"] = tax_type
        if year_min:
            params["year"] = year_min

        # Call API (disable SSL verification untuk development)
        response = requests.get(ENDPOINT, params=params, timeout=30, verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract and normalize data
        rows = data.get("data", [])
        df = pd.DataFrame(rows)
        
        if df.empty:
            return df
        
        # Parse date columns
        date_columns = ["tahun_pajak", "bulan"]
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
                except Exception:
                    pass
        
        # Cast numeric columns
        numeric_columns = [
            "penerimaan_bruto_idr",
            "restitusi_idr",
            "penerimaan_neto_idr",
            "jumlah_wp",
        ]
        for col in numeric_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
                except Exception:
                    pass
        
        # Filter by year range if provided
        if year_min and year_max and "tahun_pajak" in df.columns:
            df = df[(df["tahun_pajak"] >= year_min) & (df["tahun_pajak"] <= year_max)]
        elif year_min and "tahun_pajak" in df.columns:
            df = df[df["tahun_pajak"] >= year_min]
        
        return df
    
    except Exception as e:
        st.error(f"Gagal mengambil data dari API: {str(e)}")
        return pd.DataFrame()


def get_available_filters(df: pd.DataFrame) -> dict[str, list[str | int]]:
    """
    Extract available filter values from DataFrame.
    
    Args:
        df: DataFrame dengan data
    
    Returns:
        Dictionary dengan daftar unique values untuk setiap filter
    """
    filters: dict[str, list[str | int]] = {}
    
    if not df.empty:
        if "provinsi" in df.columns:
            filters["provinsi"] = ["Semua"] + sorted(df["provinsi"].unique().tolist())
        if "jenis_pajak" in df.columns:
            filters["jenis_pajak"] = ["Semua"] + sorted(df["jenis_pajak"].unique().tolist())
        if "tahun_pajak" in df.columns:
            years = sorted(df["tahun_pajak"].unique().astype(int).tolist())
            filters["tahun"] = years
        if "sektor" in df.columns:
            filters["sektor"] = ["Semua"] + sorted(df["sektor"].unique().tolist())
    
    return filters


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """
    Calculate main KPIs from DataFrame.
    
    Args:
        df: DataFrame dengan data
    
    Returns:
        Dictionary dengan KPI values
    """
    kpis: dict[str, float | int] = {
        "total_bruto": 0,
        "total_restitusi": 0,
        "total_neto": 0,
        "jumlah_wp": 0,
        "rasio_restitusi": 0,
    }
    
    if df.empty:
        return kpis
    
    if "penerimaan_bruto_idr" in df.columns:
        kpis["total_bruto"] = df["penerimaan_bruto_idr"].sum()
    
    if "restitusi_idr" in df.columns:
        kpis["total_restitusi"] = df["restitusi_idr"].sum()
    
    if "penerimaan_neto_idr" in df.columns:
        kpis["total_neto"] = df["penerimaan_neto_idr"].sum()
    
    if "jumlah_wp" in df.columns:
        kpis["jumlah_wp"] = int(df["jumlah_wp"].sum())
    
    # Calculate restitution ratio
    if kpis["total_bruto"] > 0:
        kpis["rasio_restitusi"] = (kpis["total_restitusi"] / kpis["total_bruto"]) * 100
    
    return kpis


def apply_filters(
    df: pd.DataFrame,
    provinsi: str | None = None,
    jenis_pajak: str | None = None,
    tahun_min: int | None = None,
    tahun_max: int | None = None,
    threshold_neto: float | None = None,
) -> pd.DataFrame:
    """
    Apply filters to DataFrame.
    
    Args:
        df: DataFrame dengan data
        provinsi: Filter provinsi
        jenis_pajak: Filter jenis pajak
        tahun_min: Tahun minimum
        tahun_max: Tahun maksimum
        threshold_neto: Threshold penerimaan neto
    
    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()
    
    if provinsi and provinsi != "Semua" and "provinsi" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["provinsi"] == provinsi]
    
    if jenis_pajak and jenis_pajak != "Semua" and "jenis_pajak" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["jenis_pajak"] == jenis_pajak]
    
    if tahun_min and "tahun_pajak" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["tahun_pajak"] >= tahun_min]
    
    if tahun_max and "tahun_pajak" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["tahun_pajak"] <= tahun_max]
    
    if threshold_neto and threshold_neto > 0 and "penerimaan_neto_idr" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["penerimaan_neto_idr"] >= threshold_neto]
    
    return filtered_df


def render() -> None:
    """Render fiqri mini project page."""
    
    # Initialize session state
    if "raw_data" not in st.session_state:
        st.session_state.raw_data = None
    if "insights_history" not in st.session_state:
        st.session_state.insights_history = []
    
    # Display banner
    banner(
        "Fiqri Mini Project - Tax Revenue Dashboard",
        "Analisis data penerimaan pajak dengan filter interaktif, KPI, dan visualisasi.",
    )
    
    # Display project objective
    st.subheader("📊 Tujuan Mini Project")
    st.info(
        """
        Membangun dashboard analisis penerimaan pajak dengan fitur:
        - Pengambilan data dari API
        - Filter interaktif (provinsi, jenis pajak, tahun, threshold)
        - Kalkulasi KPI utama
        - Visualisasi tren dan breakdown sektor
        - Export hasil analisis
        - Simpan insight analis
        """
    )
    
    # Initial action button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Muat Data", use_container_width=True):
            with st.spinner("Mengambil data dari API..."):
                st.session_state.raw_data = load_data()
                st.success("Data berhasil dimuat!")
    
    with col2:
        st.caption("Klik tombol untuk mengambil data dari API pertama kali")
    
    # Show raw data in expander
    if st.session_state.raw_data is not None:
        with st.expander("📋 Data Mentah (Validasi)", expanded=False):
            raw_df = st.session_state.raw_data
            st.write(f"Total baris: {len(raw_df)}")
            st.dataframe(raw_df, use_container_width=True)
        
        # Filter section
        st.subheader("🔍 Filter Data")
        
        # Get available filters
        available_filters = get_available_filters(st.session_state.raw_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            selected_provinsi = st.selectbox(
                "Provinsi",
                options=available_filters.get("provinsi", []),
                key="filter_provinsi",
            )
        
        with col2:
            selected_tax_type = st.selectbox(
                "Jenis Pajak",
                options=available_filters.get("jenis_pajak", []),
                key="filter_tax_type",
            )
        
        with col3:
            tahun_range = available_filters.get("tahun", [])
            if tahun_range:
                tahun_min = st.selectbox(
                    "Tahun Awal",
                    options=tahun_range,
                    key="filter_tahun_min",
                )
                tahun_max = st.selectbox(
                    "Tahun Akhir",
                    options=tahun_range,
                    index=len(tahun_range) - 1,
                    key="filter_tahun_max",
                )
            else:
                tahun_min = None
                tahun_max = None
        
        with col4:
            threshold_neto = st.number_input(
                "Threshold Penerimaan Neto (IDR)",
                min_value=0.0,
                step=1000000.0,
                key="filter_threshold_neto",
            )
        
        # Apply filters
        filtered_df = apply_filters(
            st.session_state.raw_data,
            provinsi=selected_provinsi,
            jenis_pajak=selected_tax_type,
            tahun_min=tahun_min if tahun_range else None,
            tahun_max=tahun_max if tahun_range else None,
            threshold_neto=threshold_neto if threshold_neto > 0 else None,
        )
        
        # Display KPIs
        st.subheader("📈 KPI Utama")
        kpis = calculate_kpis(filtered_df)
        
        kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
        
        with kpi_col1:
            st.metric(
                "Total Bruto",
                f"Rp {kpis['total_bruto']:,.0f}",
            )
        
        with kpi_col2:
            st.metric(
                "Total Restitusi",
                f"Rp {kpis['total_restitusi']:,.0f}",
            )
        
        with kpi_col3:
            st.metric(
                "Total Neto",
                f"Rp {kpis['total_neto']:,.0f}",
            )
        
        with kpi_col4:
            st.metric(
                "Jumlah WP",
                f"{kpis['jumlah_wp']:,}",
            )
        
        with kpi_col5:
            st.metric(
                "Rasio Restitusi",
                f"{kpis['rasio_restitusi']:.2f}%",
            )
        
        # Visualizations
        if not filtered_df.empty:
            st.subheader("📊 Visualisasi Data")
            
            tab1, tab2, tab3 = st.tabs(["Tabel Data", "Tren Waktu", "Breakdown Sektor"])
            
            with tab1:
                # Display filtered data table
                display_cols = [
                    col for col in [
                        "provinsi",
                        "jenis_pajak",
                        "tahun_pajak",
                        "bulan",
                        "penerimaan_bruto_idr",
                        "restitusi_idr",
                        "penerimaan_neto_idr",
                        "jumlah_wp",
                        "sektor",
                    ]
                    if col in filtered_df.columns
                ]
                
                if display_cols:
                    st.dataframe(
                        filtered_df[display_cols],
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            with tab2:
                # Time trend visualization
                if "tahun_pajak" in filtered_df.columns and "penerimaan_neto_idr" in filtered_df.columns:
                    trend_data = filtered_df.groupby("tahun_pajak")["penerimaan_neto_idr"].sum().reset_index()
                    st.line_chart(
                        trend_data.set_index("tahun_pajak"),
                        use_container_width=True,
                    )
                else:
                    st.info("Data tidak cukup untuk menampilkan tren waktu")
            
            with tab3:
                # Sector breakdown visualization
                if "sektor" in filtered_df.columns and "penerimaan_neto_idr" in filtered_df.columns:
                    sector_data = filtered_df.groupby("sektor")["penerimaan_neto_idr"].sum().reset_index()
                    sector_data = sector_data.sort_values("penerimaan_neto_idr", ascending=False)
                    st.bar_chart(
                        sector_data.set_index("sektor"),
                        use_container_width=True,
                    )
                else:
                    st.info("Data tidak cukup untuk menampilkan breakdown sektor")
        else:
            st.warning("Tidak ada data yang sesuai dengan filter yang dipilih")
        
        # Analyst Insight Form
        st.subheader("💡 Form Insight Analis")
        
        with st.form("analyst_insight_form"):
            insight_title = st.text_input(
                "Judul Insight",
                placeholder="Contoh: Tren Peningkatan Penerimaan Pajak di Jawa Timur",
            )
            
            insight_description = st.text_area(
                "Deskripsi Insight",
                placeholder="Jelaskan temuan atau analisis Anda...",
                height=100,
            )
            
            insight_recommendation = st.text_area(
                "Rekomendasi",
                placeholder="Berikan rekomendasi berdasarkan analisis...",
                height=80,
            )
            
            submitted = st.form_submit_button("💾 Simpan Insight", use_container_width=True)
            
            if submitted:
                # Validation
                if not insight_title.strip():
                    st.error("Judul insight tidak boleh kosong")
                elif not insight_description.strip():
                    st.error("Deskripsi insight tidak boleh kosong")
                elif not insight_recommendation.strip():
                    st.error("Rekomendasi tidak boleh kosong")
                elif len(insight_title) < 5:
                    st.error("Judul insight minimal 5 karakter")
                elif len(insight_description) < 10:
                    st.error("Deskripsi insight minimal 10 karakter")
                else:
                    # Save insight
                    insight_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "title": insight_title,
                        "description": insight_description,
                        "recommendation": insight_recommendation,
                        "data_summary": {
                            "total_rows": len(filtered_df),
                            "kpis": kpis,
                        }
                    }
                    st.session_state.insights_history.append(insight_entry)
                    st.success("✅ Insight berhasil disimpan!")
        
        # Display saved insights
        if st.session_state.insights_history:
            st.subheader("📚 Riwayat Insight")
            
            for idx, insight in enumerate(st.session_state.insights_history, 1):
                with st.expander(f"{idx}. {insight['title']} ({insight['timestamp'][:10]})"):
                    st.write("**Deskripsi:**")
                    st.write(insight["description"])
                    st.write("**Rekomendasi:**")
                    st.write(insight["recommendation"])
                    
                    with st.expander("Ringkasan Data"):
                        st.write(f"Total baris data: {insight['data_summary']['total_rows']}")
                        st.json(insight['data_summary']['kpis'])
        
        # Export section
        st.subheader("📥 Export Hasil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export filtered data as CSV
            if not filtered_df.empty:
                csv_buffer = io.StringIO()
                filtered_df.to_csv(csv_buffer, index=False)
                csv_content = csv_buffer.getvalue()
                
                st.download_button(
                    label="📊 Download Data CSV",
                    data=csv_content,
                    file_name=f"tax_revenue_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            else:
                st.info("Tidak ada data untuk diunduh")
        
        with col2:
            # Export insights as JSON
            if st.session_state.insights_history:
                insights_json = pd.DataFrame(st.session_state.insights_history).to_json(
                    orient="records",
                    indent=2,
                    default_handler=str,
                )
                
                st.download_button(
                    label="💡 Download Insights JSON",
                    data=insights_json,
                    file_name=f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                )
            else:
                st.info("Belum ada insight untuk diunduh")
    
    else:
        st.info("👆 Klik tombol 'Muat Data' di atas untuk memulai")
