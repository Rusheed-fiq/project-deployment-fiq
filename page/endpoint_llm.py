import streamlit as st

from services.llm import call_generic_endpoint, dummy_llm_response
from ui.widgets import show_banner
from utils.ollama_client import DEFAULT_OLLAMA_HOST, generate_text, list_models


def render() -> None:
    show_banner(
        "Integrasi Endpoint Model / LLM",
        "Semua respons di branch main masih berupa placeholder agar mudah dijelaskan.",
    )

    mode = st.radio(
        "Mode integrasi",
        ["Dummy", "Ollama", "Generic REST endpoint"],
        horizontal=True,
    )
    prompt = st.text_area("Prompt", placeholder="Tulis prompt untuk demo...")

    if st.button("Kirim prompt", type="primary"):
        if mode == "Dummy":
            st.write(dummy_llm_response(prompt))
        elif mode == "Ollama":
            model = list_models(DEFAULT_OLLAMA_HOST)[0]
            st.write(generate_text(prompt=prompt, model=model, host=DEFAULT_OLLAMA_HOST))
        else:
            st.write(call_generic_endpoint(url="https://example.local/api", prompt=prompt, api_key="", timeout=30))

    st.caption("TODO kelas: ganti placeholder dengan endpoint nyata atau secrets lokal.")
