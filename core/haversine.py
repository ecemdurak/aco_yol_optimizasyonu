import math


def calculate_haversine_distance(coord1, coord2):
    """
    İki koordinat arası kuş uçuşu mesafeyi (km) hesaplar.
    coord: (lat, lon)
    """
    R = 6371  # Dünya yarıçapı (km)
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c