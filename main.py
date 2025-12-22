# main.py
import streamlit as st
import pandas as pd
from data.coordinates import get_coordinates
from core.matrix_utils import create_distance_matrix
from core.ant_algorithm import AntColonyOptimization
from visual.plotting import plot_convergence, plot_route_on_map
from streamlit_folium import st_folium

# Sayfa Ayarları
st.set_page_config(page_title="ACO Kargo/Sağlık Rotası", layout="wide")

st.title("🐜 Karınca Kolonisi Algoritması ile Rota Optimizasyonu")
st.markdown("""
Bu uygulama, **Isparta Sağlık Müdürlüğü** aşı dağıtım senaryosu için en kısa rotayı 
Karınca Kolonisi Algoritması (ACO) kullanarak bulur.
""")

# --- Sidebar (Parametreler) ---
st.sidebar.header("🛠 Algoritma Parametreleri")

col_ants = st.sidebar.slider("Karınca Sayısı", 5, 100, 20)
col_iter = st.sidebar.slider("İterasyon Sayısı", 10, 500, 50)
st.sidebar.markdown("---")
alpha = st.sidebar.slider("Alpha (Feromon Önemi)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta (Mesafe Önemi)", 0.1, 5.0, 2.0)
rho = st.sidebar.slider("Buharlaşma Oranı (Rho)", 0.01, 0.99, 0.1)

# --- Veri Hazırlığı ---
locations = get_coordinates()
city_names = list(locations.keys())

# Mesafeleri Hesapla (Cache mekanizması eklenebilir ama basit tutuyoruz)
with st.spinner('Mesafe matrisi hesaplanıyor...'):
    distance_matrix, _ = create_distance_matrix(locations)

# Şehirleri göster
if st.checkbox("Şehir Listesini ve Koordinatları Göster"):
    df_loc = pd.DataFrame.from_dict(locations, orient='index', columns=['Lat', 'Lon'])
    st.dataframe(df_loc)

# --- Çalıştırma Butonu ---
if st.button("🚀 Rotayı Optimize Et"):
    aco = AntColonyOptimization(
        distances=distance_matrix,
        n_ants=col_ants,
        n_iterations=col_iter,
        alpha=alpha,
        beta=beta,
        evaporation_rate=rho
    )

    with st.spinner('Karıncalar çalışıyor...'):
        best_route_indices, best_distance, history = aco.run()

    # --- Sonuçları Göster ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.success(f"📍 En Kısa Mesafe: **{best_distance:.2f} km**")
        st.subheader("Optimize Edilmiş Rota:")

        route_names = [city_names[i] for i in best_route_indices]
        # Ok ile görselleştirme
        st.markdown(" ➡️ ".join(route_names))

        # Yakınsama Grafiği
        st.subheader("İyileşme Grafiği")
        fig_conv = plot_convergence(history)
        st.pyplot(fig_conv)

    with col2:
        st.subheader("🗺️ Rota Haritası")
        map_obj = plot_route_on_map(best_route_indices, locations, city_names)
        st_folium(map_obj, width=700, height=500)