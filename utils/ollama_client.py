DEFAULT_OLLAMA_HOST = "http://localhost:11434"


class OllamaError(Exception):
    """Raised when Ollama API calls fail."""


def list_models(host: str = DEFAULT_OLLAMA_HOST) -> list[str]:
    """Placeholder daftar model untuk demo."""
    return ["llama3.2-demo"]


def generate_text(prompt: str, model: str, host: str = DEFAULT_OLLAMA_HOST, timeout: int = 60) -> str:
    if not prompt.strip():
        raise OllamaError("Prompt tidak boleh kosong.")

    return (
        "Placeholder Ollama response. "
        f"model={model}, host={host}, timeout={timeout}, prompt={prompt}"
    )
