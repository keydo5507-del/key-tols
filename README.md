🔥 KEY GANTENG — TOOLS 

Tool Python untuk memindai jaringan Wi-Fi yang dapat dijangkau oleh adapter perangkat. Mendukung Linux, Windows, dan macOS dengan fitur pemindaian baca-saja.

✨ Fitur

- Tampilan terminal bertema KEY GANTENG.
- Menampilkan informasi jaringan Wi-Fi yang tersedia, sesuai dukungan sistem.
- Informasi SSID, BSSID, channel, sinyal, dan keamanan jika tersedia.
- Pemeriksaan sintaks Python sebelum dijalankan.
- Tidak memutus koneksi perangkat atau mencoba membobol kata sandi Wi-Fi.

📋 Persyaratan

- Git
- Python 3
- Adapter Wi-Fi yang didukung dan dapat diakses sistem
- Linux: "nmcli" atau "iwlist" untuk pemindaian

🚀 Instalasi di Linux melalui Termius

1. Perbarui paket sistem

apt update
apt install -y git python3 network-manager wireless-tools

2. Clone repository

cd ~
git clone https://github.com/keydo5507-del/key-tols.git

3. Masuk ke folder proyek

cd ~/key-tols

4. Periksa file proyek

ls -la

5. Jalankan pemeriksaan sintaks

python3 -m py_compile keywifi.py

Jika tidak ada pesan error, sintaks file berhasil diperiksa.

6. Jalankan tool

python3 keywifi.py

🔄 Memperbarui Repository

Jika repository sudah pernah di-clone:

cd ~/key-tols
git pull
python3 -m py_compile keywifi.py
python3 keywifi.py

Jika kamu ingin menggunakan versi file terbaru yang disediakan terpisah, upload file tersebut melalui SFTP Termius ke folder proyek, lalu pastikan nama akhirnya "keywifi.py".

🛠️ Mengatasi Error Wi-Fi

Jika muncul pesan "Tidak menemukan interface WiFi", periksa interface yang tersedia:

ip -br link

Periksa apakah perintah pemindaian tersedia:

command -v nmcli
command -v iwlist

Jika "nmcli" tersedia, periksa perangkat jaringan:

nmcli device status

Catatan penting: VPS dan container biasanya hanya menyediakan interface virtual seperti "lo", "eth0", atau "tun0". Interface tersebut bukan adapter Wi-Fi fisik. Memasang paket tambahan tidak otomatis membuat VPS bisa mendeteksi jaringan Wi-Fi di sekitar. Jalankan tool pada perangkat dengan adapter Wi-Fi yang didukung dan akses sistem yang sesuai.

🖥️ Sistem Operasi

- Linux: menggunakan "nmcli" atau "iwlist" jika tersedia.
- Windows: menggunakan "netsh wlan".
- macOS: menggunakan utilitas pemindaian yang tersedia pada sistem.

Ketersediaan fitur bergantung pada versi sistem operasi, izin, driver, dan adapter jaringan.

⚠️ Penggunaan yang Bertanggung Jawab

Gunakan tool untuk memeriksa jaringan yang kamu miliki atau diizinkan untuk kamu periksa. Tool ini hanya untuk pemindaian informasi jaringan secara baca-saja; tool tidak menyediakan fungsi untuk memutus koneksi pengguna lain atau membobol kata sandi.

👨‍💻 Developer

KEY GANTENG

Repository: https://github.com/keydo5507-del/key-tols
