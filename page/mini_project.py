from ui.widgets import banner
import streamlit as st


def render() -> None:
    banner(
        "Mini Project",
        "Praktik langsung dengan membangun aplikasi dengan Streamlit.",
    )

    with st.expander("Instruksi Aktivitas"):
        st.subheader("Instruksi From Scratch (untuk peserta)")
        st.info(
            "Ikuti urutan langkah berikut saat live coding agar file mini project bisa dibangun dari nol secara bertahap."
        )
        st.markdown(
            """
    Urutan kerja yang disarankan:
    1. **Buat file halaman** `page/mini_project.py` lalu tambahkan import dasar: `streamlit`, `pandas`, `requests`, dan `banner` dari `ui.widgets`.
    2. **Definisikan endpoint API** ke variabel `ENDPOINT` dengan nilai default adalah: https://training.ekos.my.id/api/tax-revenue-dashboard.
    3. **Buat fungsi loader data** (gunakan `@st.cache_data`) untuk:
    - memanggil API,
    - membaca payload JSON,
    - normalisasi ke `DataFrame`,
    - parsing kolom tanggal,
    - casting kolom numerik.
    4. **Buat fungsi `render()`** lalu tampilkan banner, tujuan mini project, dan tombol aksi awal.
    5. **Tampilkan data mentah** dalam `st.expander` agar peserta bisa validasi hasil ambil data.
    6. **Tambahkan widget filter**: provinsi, jenis pajak, rentang tahun, dan threshold penerimaan neto.
    7. **Hitung KPI utama**: total bruto, restitusi, neto, jumlah wajib pajak, dan rasio restitusi.
    8. **Bangun visualisasi** dengan tab: tabel data, tren waktu, dan breakdown sektor.
    9. **Tambahkan form insight analis** + validasi sederhana sebelum simpan ringkasan.
    10. **Tambahkan export** hasil filter ke CSV via `st.download_button`.

    Checklist selesai:
    - Data API berhasil ditarik.
    - Filter bekerja sesuai input.
    - KPI dan chart tampil benar.
    - Ringkasan insight bisa disimpan.
    - Hasil analisis bisa diunduh.
    """
        )