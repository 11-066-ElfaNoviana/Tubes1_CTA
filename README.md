# Tubes-STIMA-CTA

> by CTA

## Table of Contents

- [General Information](#general-information)
- [File Structures](#file-structures)
- [Requirement](#requirement)
- [Setup and Usage](#setup-and-usage)
- [Authors](#authors)

## General Information

Bot otomatis untuk permainan Diamonds dengan strategi greedy<br>
Terkait permainan dapat dilihat pada pranala [ini](https://drive.google.com/file/d/17_d7sRWhr0TspjS0ZqIIQCnQnElPaeDR/view)<br>

Algoritma greedy yang digunakan sebagai berikut:
1. Memilih diamond terdekat untuk meminimalkan jarak tempuh.
2. Memilih diamond bernilai tertinggi dengan mempertimbangkan jarak.
3. Optimasi pengumpulan diamond dalam kondisi papan dinamis.
4. Menggunakan teleporter untuk akses cepat ke blok kaya diamond.
5. Melakukan Kembali ke base saat inventory penuh.

## File Structures

├── doc
│└── cta.pdf
├── src
│ ├── pycache
│ │ ├── decode.cpython-311.pyc
│ │ ├── api.cpython-311.pyc
│ │ ├── board_handler.cpython-311.pyc
│ │ ├── bot_handler.cpython-311.pyc
│ │ ├── models.cpython-311.pyc
│ │ └── util.cpython-311.pyc
│ ├── decode.py
│ ├── api.py
│ ├── board_handler.py
│ ├── bot_handler.py
│ ├── logic
│ │ ├── init.py
│ │ ├── pycache
│ │ │ ├── base.cpython-311.pyc
│ │ │ ├── mybot.cpython-311.pyc
│ │ │ └── random.cpython-311.pyc
│ │ ├── base.py
│ │ ├── mybot.py
│ │ └── random.py
│ ├── models.py
│ └── util.py
├── .gitignore
├── decode.py
├── jeno.py
├── main.py
├── README.md
├── requirements.txt
├── run-bots.bat
└── run-bots.sh

## Requirement

- Python 3.X
- Node.js install pada pranala [berikut](https://nodejs.org/en)
- Docker dekstop install pada pranala [berikut](https://www.docker.com/products/docker-desktop/)
- Instalasi library python pada src/requirement.txt
- Yarn, install dengan perintah berikut

npm install --global yarn


## Setup and Usage

1. Download dan lakukan instalasi game engine dengan mengikuti instruksi pada pranala [berikut](https://docs.google.com/spreadsheets/d/1FJ0SS6AtDuOtYBe7_bViBHV0cmOipCHIhLPDQMhwvlE/edit?gid=0#gid=0)
2. Clone repository berikut git clone https://github.com/11-066-ElfaNoviana/Tubes1_CTA
3. Ganti ke root directory folder src dengan perintah cd src
4. Install package python dengan perintah pip install -r requirement.txt
5. Untuk menjalankan bot, nyalakan terlebih dahulu game engine
6. Untuk menjalankan satu bot, jalankan perintah


python main.py --logic MyBot --email=your_email@example.com --name=your_name --password=your_password --team etimo


Untuk menjalankan beberapa bot sekaligus jalankan perintah berikut
- Untuk Windows
./run-bots.bat

- Untuk Linux
./run-bots.sh

7. Bot sudah dapat berjalan

## Authors

|    NIM    |      Nama Lengkap        |
| --------- | ------------------------ |
| 123140063 | Pradana Figo Ariasya     |
| 123140064 | Miftahul Khoiriyah       |
| 123140066 | Elfa Noviana Sari        |
