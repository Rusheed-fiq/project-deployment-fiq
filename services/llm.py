def dummy_llm_response(prompt: str, mode: str = "dummy") -> str:
    if not prompt.strip():
        return "Prompt masih kosong."
    return f"[Placeholder {mode}] Respons untuk: {prompt}"


def call_generic_endpoint(url: str, prompt: str, api_key: str, timeout: int) -> str:
    if not url.strip():
        return "URL endpoint belum diisi."
    return (
        "Placeholder integrasi endpoint aktif. "
        f"url={url}, timeout={timeout}, api_key={'ya' if api_key.strip() else 'tidak'}, prompt={prompt}"
    )
