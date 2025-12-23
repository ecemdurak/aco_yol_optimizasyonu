# Antalya Muratpaşa Kargo Rota Optimizasyonu (ACO)

Bu proje, Antalya'nın Muratpaşa ilçesinde faaliyet gösteren bir kargo firmasının dağıtım rotasını optimize etmek için geliştirilmiş bir **Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO)** uygulamasıdır.

Senaryo gereği, dağıtım merkezi (Meydan) ve 20 farklı teslimat noktası (AVM'ler, hastaneler, önemli caddeler) arasındaki en kısa "Hamilton Döngüsü" hesaplanarak yakıt ve zaman tasarrufu hedeflenmiştir.

## 🏙️ Proje Kapsamı: Senaryo 4

**Konum:** Antalya, Muratpaşa İlçesi  
**Nokta Sayısı:** 21 (1 Merkez + 20 Teslimat Noktası)  
**Hedef:** Tüm noktalara birer kez uğrayıp merkeze dönen en kısa rotayı bulmak (Gezgin Satıcı Problemi).

**Teslimat Noktalarından Bazıları:**
* MarkAntalya & TerraCity AVM
* Medical Park & Yaşam Hastaneleri
* Düden Parkı & Lara Plajı
* Kaleiçi & Işıklar Caddesi

---

## 🚀 Teknik Özellikler

* **Gelişmiş Algoritma:** ACO (Ant Colony Optimization) kullanılarak NP-Hard bir problem olan TSP için optimuma yakın sonuçlar üretilir.
* **State Management (Hafıza Yönetimi):** Streamlit'in `session_state` özelliği kullanılarak, harita üzerinde gezinti yapıldığında hesaplama sonuçlarının kaybolması engellenmiştir.
* **Hibrit Mesafe Motoru:**
    * Google Maps API (Opsiyonel): Trafik ve yol durumuna göre gerçek sürüş mesafesi.
    * Haversine Formülü (Varsayılan): Koordinatlar arası kuş uçuşu mesafe hesaplama.
* **İnteraktif Arayüz:**
    * Parametre ayarı (Karınca sayısı, İterasyon, Feromon etkisi).
    * Folium tabanlı dinamik harita.
    * Matplotlib ile performans (yakınsama) grafiği.

## 📂 Dosya Yapısı

```text
antalya_kargo_aco/
│
├── main.py               # Antalya senaryosu için ana uygulama
├── requirements.txt      # Gerekli Python kütüphaneleri
├── .env                  # API Anahtarı (Opsiyonel)
│
├── data/
│   └── antalya_data.py   # Muratpaşa'daki 20 noktanın koordinatları
│
├── core/
│   ├── ant_algorithm.py  # ACO Algoritma Sınıfı
│   └── matrix_utils.py   # Mesafe matrisi hesaplayıcı
│
└── visual/
    └── plotting.py       # Harita ve grafik çizim fonksiyonları
