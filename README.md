# Streamlit Kelas Praktik (Main Branch)

Repo ini adalah versi **skeleton / trimmed** untuk live coding.
Struktur project sengaja dipertahankan, tetapi isi modul dibuat lebih ringan agar peserta bisa mengisi sendiri saat demo.

## Tujuan

- Menunjukkan struktur project Streamlit modular
- Menyediakan titik awal yang mudah dijelaskan di kelas
- Memberi ruang untuk praktik langsung tanpa terlalu banyak distraksi

## Struktur Project

```text
.
├── app.py
├── core/
│   └── theme.py
├── ui/
│   └── widgets.py
├── services/
│   ├── dummy_data.py
│   └── llm.py
├── page/
│   ├── beranda.py
│   ├── dasar_widget.py
│   ├── state_form_cache.py
│   ├── mini_project.py
│   ├── endpoint_llm.py
│   └── deployment.py
├── utils/
│   └── ollama_client.py
├── data/
│   └── .gitkeep
└── .streamlit/
```

## Menjalankan Lokal

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Catatan

- Branch `example` berisi versi demo yang lebih lengkap.
- Branch `main` berisi versi latihan yang lebih kosong.
- Silakan isi placeholder sesuai alur kelas.
