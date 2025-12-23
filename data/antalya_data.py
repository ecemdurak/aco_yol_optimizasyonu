# data/antalya_data.py

# Antalya Muratpaşa Kargo Dağıtım Noktaları (20 Nokta)
# Başlangıç: Kargo Dağıtım Merkezi (Meydan varsayıldı)

ANTALYA_LOCATIONS = {
    "Kargo Dağıtım Mrk. (Meydan)": (36.8856, 30.7302), # Başlangıç
    "MarkAntalya AVM": (36.8914, 30.7003),
    "TerraCity AVM": (36.8527, 30.7563),
    "Mall of Antalya": (36.9328, 30.7761),
    "Işıklar Caddesi": (36.8785, 30.7088),
    "Dedeman Otel Kavşağı": (36.8665, 30.7289),
    "Özel Yaşam Hastanesi": (36.8687, 30.7410),
    "Muratpaşa Belediyesi": (36.8592, 30.7265),
    "Kaleiçi (Üç Kapılar)": (36.8835, 30.7073),
    "Lara Plajı Girişi": (36.8488, 30.8033),
    "Düden Parkı (Şelale)": (36.8477, 30.7770),
    "Laura AVM": (36.8541, 30.7432),
    "Shemall AVM": (36.8550, 30.7439),
    "Medical Park Hastanesi": (36.8546, 30.7482),
    "Antalya Müzesi": (36.8845, 30.6806),
    "Akra Barut Otel": (36.8651, 30.7231),
    "Bülent Ecevit Kültür Mrk.": (36.8510, 30.7600),
    "Fener Mahallesi Muhtarlık": (36.8489, 30.7512),
    "Kırcami Bölgesi": (36.8720, 30.7550),
    "Yeşilbahçe Mahallesi": (36.8620, 30.7180)
}

def get_antalya_coordinates():
    return ANTALYA_LOCATIONS