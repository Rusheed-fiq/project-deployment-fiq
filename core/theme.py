import streamlit as st

KEMENKEU_BLUE = "#0F2D6B"
KEMENKEU_GOLD = "#F2B705"
KEMENKEU_BG = "#F6F8FC"


def setup_page() -> None:
    st.set_page_config(
        page_title="Pelatihan Streamlit - Kemenkeu",
        page_icon="🏛️",
        layout="wide",
    )


def apply_kemenkeu_theme() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {KEMENKEU_BG};
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        .kemenkeu-banner {{
            background: linear-gradient(90deg, {KEMENKEU_BLUE} 0%, #1F4AA8 100%);
            padding: 1rem 1.2rem;
            border-radius: 12px;
            color: white;
            border-top: 6px solid {KEMENKEU_GOLD};
            margin-bottom: 1rem;
        }}
        h1, h2, h3 {{
            color: {KEMENKEU_BLUE};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
