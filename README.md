# Nama  : Amalia
# NIM   : F1D02310002
# Kelas : Pemrograman Visual C

# Tugas 5 — Threading & REST API

Aplikasi desktop Post Manager menggunakan PySide6 dan REST API. Aplikasi ini digunakan untuk mengelola data post dengan fitur CRUD lengkap yaitu menampilkan daftar post (GET), menambah post baru (POST), mengedit post (PUT), dan menghapus post (DELETE). Data post ditampilkan dalam tabel dengan informasi ID, title, author, dan status, serta detail post dapat dilihat pada panel samping saat salah satu data dipilih.

Aplikasi menerapkan konsep multi-threading menggunakan QThread sehingga seluruh proses request API berjalan di thread terpisah dan tampilan aplikasi tetap responsif tanpa freeze. Selain itu, aplikasi juga memiliki state handling dan error handling untuk menampilkan status loading, pesan error koneksi, timeout, serta validasi slug unik dari server.

## Fitur
- GET semua post
- Detail post
- Tambah post
- Edit post
- Hapus post
- Multi-threading menggunakan QThread
- Error handling timeout dan connection error

## Teknologi
- Python
- PySide6
- Requests
- REST API

## Cara Menjalankan

```bash
pip install -r requirements.txt
python main.py
```

## Screenshot

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Tambah Post
![Tambah](screenshots/add_post.png)

### Edit Post
![Edit](screenshots/edit_post.png)

### Delete Post
![Delete](screenshots/delete_post.png)