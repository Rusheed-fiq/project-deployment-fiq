from ui.layouts import three_columns_layout
from ui.widgets import banner, card_with_anchor


def render() -> None:
    banner(
        "Pelatihan Project Deployment dengan Streamlit",
        "Berkenalan dengan Streamlit, framework Python untuk membuat aplikasi web interaktif dengan mudah.",
    )

    col1, col2, col3 = three_columns_layout()

    with col1:
        card_with_anchor(
            title="Apa itu Streamlit?",
            content="Streamlit adalah framework open-source yang memungkinkan kamu membuat aplikasi web interaktif dengan cepat menggunakan Python.",
            anchor="https://streamlit.io/",
        )

    with col2:
        card_with_anchor(
            title="Streamlit Komponen",
            content="Reusable components seperti st.button, st.text_input, st.selectbox, dan banyak lagi untuk membangun UI aplikasi dengan mudah.",
            anchor="https://docs.streamlit.io/develop/api-reference",
            label="Lihat Komponen",
        )

    with col3:
        card_with_anchor(
            title="Galeri",
            content="Publikasi aplikasi Streamlit yang dibuat oleh komunitas di seluruh dunia, silakan gunakan sebagai inspirasi untuk proyekmu sendiri.",
            anchor="https://streamlit.io/gallery",
        )
