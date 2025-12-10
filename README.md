# Cinema Project

Bu proje, sinema salonu için film, müşteri ve rezervasyon yönetimi yapmayı sağlayan basit bir web uygulamasıdır. Arayüz Flask ile yazıldı ve veriler SQL tabanlı bir veritabanında tutuluyor.

## Özellikler
- Film ekleme, silme ve güncelleme
- Koltuk seçme ve rezervasyon işlemleri
- Müşteri bilgileri yönetimi
- Satış ve raporlama sayfaları
- Öneri sistemi
- SQL kullanılarak veri kaydetme ve sorgulama

## Kullanılan Teknolojiler
- Python / Flask
- HTML – CSS – JavaScript
- SQL (SQLite)
- Jinja2 template yapısı

## Projeyi Çalıştırma

### 1. Gerekli paketleri yükleyin:
pip install -r requirements.txt

### 2. Uygulamayı başlatın:
python app.py

### 3. Tarayıcıdan açın:
http://127.0.0.1:5000/

## Dosya Yapısı
cinema_project/
│ app.py
│ db.py
│ requirements.txt
│
├── templates/
├── static/
└── README.md

## Veritabanı
Proje SQL kullandığı için tüm müşteri, film, koltuk ve rezervasyon bilgileri db.py içinde tanımlanan SQL sorguları ile yönetilir. Veritabanı dosyası proje klasöründe otomatik oluşturulur.
