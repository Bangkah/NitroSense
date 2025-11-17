# Linux NitroSense

**Linux NitroSense V3** adalah aplikasi monitoring dan kontrol hardware khusus untuk laptop **Acer Nitro V16** di Linux.  
Aplikasi ini memungkinkan kamu memonitor suhu CPU/GPU, performa, dan kontrol fan langsung dari desktop Linux menggunakan AppImage.
Aplikasi ini dibuat agar saya tetap bisa menggunakan nitrosense walaupun saya menggunakan linux

---

## Fitur
- Monitoring suhu CPU dan GPU
- Kontrol kecepatan fan
- Mode performa Nitro (normal, gaming, silent)
- Ringan dan portabel (tidak perlu install, hanya jalankan AppImage)
- Kompatibel dengan distribusi Linux x86_64

---

## Instalasi

1. Download AppImage dari GitHub:

```
wget https://github.com/Bangkah/NitroSense/releases/download/v3/Linux_NitroSense_V3-x86_64.AppImage -O Linux_NitroSense_V3-x86_64.AppImage
````


2. Beri izin eksekusi:

```bash
chmod +x Linux_NitroSense_V3-x86_64.AppImage
```

3. Jalankan aplikasi:

```bash
./Linux_NitroSense_V3-x86_64.AppImage
```

---

## Cara Menggunakan

* Klik ikon NitroSense di menu aplikasi, atau jalankan langsung dari terminal.
* Pastikan kamu memiliki hak akses **sudo** jika ingin mengubah setting fan atau performa.

---

## Struktur Repository

```
nitrosense/
├── dist/                        # Folder hasil build PyInstaller
├── NitroSense.AppDir/            # Struktur AppDir untuk AppImage
├── Linux_NitroSense_V3-x86_64.AppImage
├── nitrosense_v1.py              # Script Python versi awal
├── nitrosense_v2.py
├── nitrosense_v3.py              # Script Python utama
├── nitro_icon.png                # Icon aplikasi
└── README.md
```
