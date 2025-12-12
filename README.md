# 🎯 Product Review Analyzer
Aplikasi untuk menganalisis review produk secara otomatis menggunakan AI. Aplikasi ini menentukan sentimen (Positif/Negatif) dan mengekstrak poin-poin penting dari ulasan pengguna.

## 🚀 Fitur
* **Input Review:** Pengguna dapat memasukkan nama produk dan teks ulasan.
* **Sentiment Analysis:** Menggunakan **Hugging Face** untuk menentukan apakah ulasan bersifat Positif atau Negatif.
* **Key Point Extraction:** Menggunakan **Gemini AI** untuk merangkum poin-poin utama dari ulasan.
* **Database Storage:** Menyimpan hasil analisis ke database **PostgreSQL**.
* **History Display:** Menampilkan riwayat ulasan yang pernah dianalisis.

## 🛠️ Tools
**Backend:**
* Python (Pyramid Framework)
* SQLAlchemy (ORM)
* PostgreSQL (Database)
* Gemini AI API
* Hugging Face API

**Frontend:**
* React JS
* CSS

## ⚙️ How To Run
**Menjalankan Backend**
- cd ke folder backendnya
- aktifkan virtual environtment di folder backend: venv\Scripts\activate
- jalankan di folder backend: python app.py

**Menjalankan Frontend**
- cd ke folder backend dulu
- aktifkan virtual environtment di folder backend: venv\Scripts\activate
- pindah ke folder frontend: cd ..\frontend\
- jalankan di folder frontend: npm run dev

Note: Jalankan keduanya simultaneously! Jadi menggunakan 2 terminal untuk masing2.

## 🎨 Hasil
**Tampilan**

<img width="784" height="1260" alt="Screenshot 2025-12-12 170354" src="https://github.com/user-attachments/assets/e00916d0-6c43-4409-9e43-0d066e1d0420" />

#review negative hanya untuk percobaan, maaf jika kata-katanya termasuk kasar 🙏🏿

**Database**

<img width="1380" height="424" alt="Screenshot 2025-12-12 170410" src="https://github.com/user-attachments/assets/a1aed6ba-ca97-4d5e-99f5-eaa34b735b26" />
