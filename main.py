import streamlit as st
import pandas as pd
from data.antalya_data import get_antalya_coordinates
from core.matrix_utils import create_distance_matrix
from core.ant_algorithm import AntColonyOptimization
from visual.plotting import plot_convergence, plot_route_on_map
from streamlit_folium import st_folium

# Sayfa Ayarları
st.set_page_config(page_title="Antalya Kargo Rota Optimizasyonu", layout="wide")

st.title("📦 Antalya Muratpaşa Kargo Dağıtım Rotası")

# --- SESSION STATE BAŞLATMA (HAFIZA) ---
# Sayfa yenilense bile verilerin kaybolmaması için burası eklendi.
if 'results' not in st.session_state:
    st.session_state['results'] = None

# --- Sidebar (Parametreler) ---
st.sidebar.header("⚙️ Algoritma Ayarları")
col_ants = st.sidebar.slider("Karınca Sayısı", 10, 100, 40)
col_iter = st.sidebar.slider("İterasyon Sayısı", 10, 500, 100)
st.sidebar.markdown("---")
alpha = st.sidebar.slider("Alpha (Feromon)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta (Mesafe)", 0.1, 5.0, 3.0)
rho = st.sidebar.slider("Buharlaşma Oranı", 0.01, 0.99, 0.1)

# --- Veri Hazırlığı ---
locations = get_antalya_coordinates()
city_names = list(locations.keys())

st.info(f"📍 Toplam Teslimat Noktası: **{len(locations)}**")

# Mesafeleri Hesapla (Bunu cacheleyebiliriz ama şimdilik kalsın)
with st.spinner('Mesafe matrisi oluşturuluyor...'):
    distance_matrix, _ = create_distance_matrix(locations)

# Lokasyon Listesi
with st.expander("Teslimat Noktaları Listesi"):
    df_loc = pd.DataFrame.from_dict(locations, orient='index', columns=['Enlem', 'Boylam'])
    st.dataframe(df_loc)

# --- ÇALIŞTIRMA BUTONU ---
# Butona basınca hesaplama yapar ve sonucu HAFIZAYA kaydederiz.
if st.button("🚀 En Kısa Dağıtım Rotasını Hesapla"):
    aco = AntColonyOptimization(
        distances=distance_matrix,
        n_ants=col_ants,
        n_iterations=col_iter,
        alpha=alpha,
        beta=beta,
        evaporation_rate=rho
    )

    with st.spinner('Karıncalar Muratpaşa sokaklarında rotayı hesaplıyor...'):
        best_route_indices, best_distance, history = aco.run()

        # KRİTİK NOKTA: Sonuçları session_state içine sözlük olarak atıyoruz
        st.session_state['results'] = {
            'route': best_route_indices,
            'dist': best_distance,
            'history': history
        }

# --- SONUÇLARI GÖSTERME KISMI ---
# Artık "if button" bloğunun dışındayız.
# Eğer hafızada sonuç varsa, butona basılmasa bile ekrana basarız.
if st.session_state['results'] is not None:

    # Verileri hafızadan çek
    res = st.session_state['results']
    best_route_indices = res['route']
    best_distance = res['dist']
    history = res['history']

    col1, col2 = st.columns([1, 2])

    with col1:
        st.success(f"🏁 Toplam Rota Uzunluğu: **{best_distance:.2f} km**")

        st.subheader("📋 Dağıtım Sırası:")
        for i, idx in enumerate(best_route_indices):
            st.write(f"**{i + 1}.** {city_names[idx]}")

        st.subheader("Performans Grafiği")
        fig_conv = plot_convergence(history)
        st.pyplot(fig_conv)

    with col2:
        st.subheader("🗺️ Rota Haritası")
        # Harita her çizildiğinde Streamlit sayfayı yeniler,
        # session_state kullandığımız için artık grafik kaybolmaz.
        map_obj = plot_route_on_map(best_route_indices, locations, city_names)
        st_folium(map_obj, width=800, height=600)