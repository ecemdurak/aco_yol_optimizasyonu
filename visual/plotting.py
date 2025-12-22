# visual/plotting.py
import matplotlib.pyplot as plt
import folium


def plot_convergence(history):
    """İterasyon vs Mesafe grafiği çizer"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(history, label="En Kısa Mesafe", color='blue')
    ax.set_title("ACO Yakınsama Grafiği (Convergence)")
    ax.set_xlabel("İterasyon Sayısı")
    ax.set_ylabel("Toplam Mesafe (km)")
    ax.grid(True)
    ax.legend()
    return fig


def plot_route_on_map(route_indices, locations, city_names):
    """Rotayı harita üzerinde çizer"""
    # Merkez başlangıç noktası
    start_city = city_names[route_indices[0]]
    start_coords = locations[start_city]

    # Harita oluştur
    m = folium.Map(location=start_coords, zoom_start=10)

    # Rota koordinatlarını hazırla
    route_coords = []
    for idx in route_indices:
        city = city_names[idx]
        coord = locations[city]
        route_coords.append(coord)

        # Marker ekle
        folium.Marker(
            location=coord,
            popup=f"{city}",
            tooltip=f"{city}",
            icon=folium.Icon(color="red" if idx == 0 else "blue", icon="info-sign")
        ).add_to(m)

    # Çizgiyi çiz (PolyLine)
    folium.PolyLine(
        route_coords,
        color="blue",
        weight=2.5,
        opacity=1
    ).add_to(m)

    return m