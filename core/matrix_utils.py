import numpy as np
import googlemaps
import os
from dotenv import load_dotenv
from core.haversine import calculate_haversine_distance

load_dotenv()


def create_distance_matrix(locations):
    """
    Şehirler arası mesafe matrisini oluşturur.
    API Key varsa Google Maps (Sürüş mesafesi), yoksa Haversine (Kuş uçuşu) kullanır.
    """
    city_names = list(locations.keys())
    coords = list(locations.values())
    n = len(city_names)
    matrix = np.zeros((n, n))

    api_key = os.getenv("GOOGLE_API_KEY")

    # API Kontrolü ve Kullanımı
    if api_key and api_key != "senin_google_maps_api_anahtarin_buraya":
        try:
            print("Google Maps API kullanılıyor...")
            gmaps = googlemaps.Client(key=api_key)

            # Google Maps Distance Matrix API (Maksimum limitlere dikkat edilmeli)
            # Burada basitleştirilmiş bir döngü kullanıyoruz.
            # Gerçek projede 'origins' ve 'destinations' listeleriyle batch istek atılır.
            for i in range(n):
                for j in range(n):
                    if i != j:
                        # origins=coords[i], destinations=coords[j]
                        result = gmaps.distance_matrix(coords[i], coords[j], mode="driving")
                        dist_text = result['rows'][0]['elements'][0]['distance']['value']  # Metre cinsinden
                        matrix[i][j] = dist_text / 1000.0  # Km'ye çevir
        except Exception as e:
            print(f"API Hatası: {e}. Haversine yöntemine dönülüyor.")
            return _create_haversine_matrix(coords)
    else:
        print("API Key bulunamadı. Haversine (Kuş uçuşu) kullanılıyor.")
        return _create_haversine_matrix(coords)

    return matrix, city_names


def _create_haversine_matrix(coords):
    n = len(coords)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = calculate_haversine_distance(coords[i], coords[j])
    # Şehir isimlerini return etmiyoruz çünkü sadece matrix lazım burada
    return matrix, None