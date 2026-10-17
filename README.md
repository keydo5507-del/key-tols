🔥 KEY GANTENG — TOOLS

Tool Python untuk memindai jaringan Wi-Fi yang tersedia dan dapat dijangkau oleh adapter perangkat. Mendukung Linux, Windows, dan macOS sesuai dukungan sistem.

✨ Fitur

- Tampilan terminal bertema KEY GANTENG.
- Menampilkan jaringan Wi-Fi yang tersedia.
- Menampilkan SSID, BSSID, channel, sinyal, dan keamanan jika tersedia.
- Pemeriksaan sintaks Python.
- Pemindaian baca-saja, tanpa mencoba membobol kata sandi Wi-Fi.

📋 Persyaratan

- Git
- Python 3
- Adapter Wi-Fi yang didukung.
- Linux: "nmcli" atau "iwlist", jika tersedia.

🚀 Instalasi di Linux melalui Termius

1. Perbarui daftar paket

``apt update``

2. Instal kebutuhan sistem

`apt install -y git python3 network-manager wireless-tools`

3. Masuk ke direktori home

`cd ~`

4. Clone repository GitHub

Jalankan hanya jika repository belum tersedia.

`git clone https://github.com/keydo5507-del/key-tols.git`

5. Masuk ke folder proyek

`cd ~/key-tols`

6. Periksa file proyek

`ls -la`

Pastikan file "keywifi.py" tersedia.

7. Periksa sintaks Python

`python3 -m py_compile keywifi.py`

Jika tidak muncul pesan error, pemeriksaan sintaks berhasil.

8. Jalankan tool

`python3 keywifi.py`

🔄 Memperbarui Repository

1. Masuk ke folder proyek

`cd ~/key-tols`

2. Ambil pembaruan terbaru

`git pull`

3. Periksa sintaks Python

`python3 -m py_compile keywifi.py`

4. Jalankan kembali tool

`python3 keywifi.py`

🛠️ Mengatasi Error Wi-Fi

Error: Tidak menemukan interface Wi-Fi

Periksa interface jaringan:

`ip -br link`

Periksa perangkat NetworkManager:

`nmcli device status`

Periksa apakah "nmcli" tersedia:

`command -v nmcli`

Periksa apakah "iwlist" tersedia:

`command -v iwlist`

Catatan: VPS dan container umumnya hanya menyediakan interface virtual seperti "lo", "eth0", atau "tun0". Memasang paket tambahan tidak otomatis membuat VPS dapat mendeteksi jaringan Wi-Fi di sekitar.

Jalankan tool pada perangkat dengan adapter Wi-Fi yang didukung dan izin sistem yang sesuai.

🖥️ Sistem Operasi

- Linux: "nmcli" atau "iwlist", jika tersedia.
- Windows: "netsh wlan", jika didukung.
- macOS: utilitas pemindaian yang tersedia pada sistem.

Ketersediaan fitur bergantung pada sistem operasi, izin, driver, dan adapter jaringan.

⚠️ Penggunaan yang Bertanggung Jawab

Gunakan tool hanya untuk memindai jaringan milik sendiri atau jaringan yang penggunaannya telah diizinkan. Tool ini ditujukan untuk melihat informasi jaringan, bukan memutus koneksi orang lain atau membobol kata sandi Wi-Fi.

👨‍💻 Developer

KEY GANTENG

Repository: `https://github.com/keydo5507-del/key-tols`
