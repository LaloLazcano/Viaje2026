import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="EuroTrip 2026",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PARA ESTILO "DASHBOARD / TARJETA" ---
# Esto hace que se parezca a la imagen de referencia (blanco, limpio, sombras)
st.markdown("""
<style>
    /* Fondo general gris suave */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Títulos */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #111827;
    }
    
    /* Sidebar personalizado */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Contenedores tipo tarjeta (Cards) */
    .css-1r6slb0, .stDataFrame, .stMap {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        padding: 1rem;
    }
    
    /* Botones primarios */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        border: 1px solid #E5E7EB;
    }
    
    /* Métrica destacada */
    div[data-testid="metric-container"] {
        background-color: #EFF6FF;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #BFDBFE;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES AUXILIARES (INTELIGENCIA) ---

def generar_link_hotel(nombre_hotel, ciudad):
    """Genera un link de búsqueda en Google Hotels"""
    query = f"{nombre_hotel} {ciudad} price".replace(" ", "+")
    return f"https://www.google.com/search?q={query}"

def generar_link_vuelo(origen, destino):
    """Genera link a Google Flights"""
    return f"https://www.google.com/travel/flights?q=flights+from+{origen}+to+{destino}"

# --- 4. BASE DE DATOS DEL VIAJE ---
# Nota: Las imágenes son de Unsplash (libres). Los precios son estimados base.
trip_data = {
    "1. Nápoles": {
        "days": "Llegada",
        "coords": [40.8518, 14.2681],
        "image": "https://images.unsplash.com/photo-1596811466030-9b3621495c6f?auto=format&fit=crop&w=800&q=80",
        "desc": "Caos, pizza y el alma real de Italia.",
        "stay": [
            {"name": "Bueno Hotel B&B", "price_est": 120, "type": "Hotel"},
            {"name": "Elite Rooms Napoli", "price_est": 140, "type": "Hotel"},
            {"name": "Hostel of the Sun", "price_est": 80, "type": "Hostal"}
        ],
        "transport": {"type": "Avión", "detail": "Llegada Intl.", "cost": 0},
        "must_see": [
            {"Lugar": "Pompeya", "Costo": "18€", "Link": "https://pompeiisites.org/"},
            {"Lugar": "Vesubio", "Costo": "10€", "Link": "#"},
            {"Lugar": "Spaccanapoli", "Costo": "Gratis", "Link": "#"}
        ]
    },
    "2. Roma": {
        "days": "2 Días",
        "coords": [41.9028, 12.4964],
        "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80",
        "desc": "La ciudad eterna. Historia en cada esquina.",
        "stay": [
            {"name": "Hotel Archimede", "price_est": 160, "type": "Hotel"},
            {"name": "Grand Hotel Colony", "price_est": 150, "type": "Hotel"},
            {"name": "YellowSquare Rome", "price_est": 90, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "detail": "Frecciarossa (1h 10m)", "cost": 25},
        "must_see": [
            {"Lugar": "Coliseo", "Costo": "16€", "Link": "#"},
            {"Lugar": "Vaticano", "Costo": "17€", "Link": "#"},
            {"Lugar": "Fontana di Trevi", "Costo": "Gratis", "Link": "#"}
        ]
    },
    "3. Florencia": {
        "days": "2 Días (Pisa de paso)",
        "coords": [43.7696, 11.2558],
        "image": "https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=800&q=80",
        "desc": "Arte renacentista y la Toscana.",
        "stay": [
            {"name": "Florera Cinque", "price_est": 180, "type": "Hotel"},
            {"name": "Plus Florence", "price_est": 110, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "detail": "Tren rápido (1h 30m)", "cost": 30},
        "must_see": [
            {"Lugar": "Duomo", "Costo": "Gratis", "Link": "#"},
            {"Lugar": "Uffizi", "Costo": "25€", "Link": "#"},
            {"Lugar": "Ponte Vecchio", "Costo": "Gratis", "Link": "#"}
        ]
    },
    "4. Génova": {
        "days": "2 Días (Cinque Terre)",
        "coords": [44.4056, 8.9463],
        "image": "https://images.unsplash.com/photo-1596323089406-8d697818df4d?auto=format&fit=crop&w=800&q=80",
        "desc": "Puerto histórico y base para Cinque Terre.",
        "stay": [
            {"name": "Hotel Bellevue", "price_est": 130, "type": "Hotel"},
            {"name": "Manena Hostel", "price_est": 70, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "detail": "Intercity (2h 45m)", "cost": 20},
        "must_see": [
            {"Lugar": "Cinque Terre", "Costo": "18€ (Tren)", "Link": "#"},
            {"Lugar": "Acuario", "Costo": "27€", "Link": "#"},
            {"Lugar": "Boccadasse", "Costo": "Gratis", "Link": "#"}
        ]
    },
    "5. Niza": {
        "days": "1 Día (Mónaco)",
        "coords": [43.7102, 7.2620],
        "image": "https://images.unsplash.com/photo-1533634064038-1634623719b3?auto=format&fit=crop&w=800&q=80",
        "desc": "Costa Azul y glamour francés.",
        "stay": [
            {"name": "Hotel Modern Waikiki", "price_est": 150, "type": "Hotel"},
            {"name": "Villa Saint Exupery", "price_est": 90, "type": "Hostal"}
        ],
        "transport": {"type": "Bus/Tren", "detail": "FlixBus (3h)", "cost": 20},
        "must_see": [
            {"Lugar": "Promenade des Anglais", "Costo": "Gratis", "Link": "#"},
            {"Lugar": "Mónaco (Tren)", "Costo": "5€", "Link": "#"}
        ]
    },
    "6. Marsella": {
        "days": "2 Días",
        "coords": [43.2965, 5.3698],
        "image": "https://images.unsplash.com/photo-1549280965-0e2384a7d4f9?auto=format&fit=crop&w=800&q=80",
        "desc": "Puerto vibrante y Calanques.",
        "stay": [
            {"name": "Toyoko Inn", "price_est": 100, "type": "Hotel"},
            {"name": "Vertigo Vieux-Port", "price_est": 75, "type": "Hostal"}
        ],
        "transport": {"type": "Tren/Bus", "detail": "TGV o Bus (2h 30m)", "cost": 25},
        "must_see": [
            {"Lugar": "Notre-Dame", "Costo": "Gratis", "Link": "#"},
            {"Lugar": "Calanques", "Costo": "Gratis", "Link": "#"}
        ]
    },
    "7. Barcelona": {
        "days": "2 Días",
        "coords": [41.3851, 2.1734],
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=800&q=80",
        "desc": "Gaudí, playa y vida nocturna.",
        "stay": [
            {"name": "Generator Barcelona", "price_est": 100, "type": "Hostal Premium"},
            {"name": "Hostal Debmates", "price_est": 110, "type": "Pensión"}
        ],
        "transport": {"type": "Tren/Avión", "detail": "Larga distancia (4h+)", "cost": 50},
        "must_see": [
            {"Lugar": "Sagrada Familia", "Costo": "26€", "Link": "#"},
            {"Lugar": "Parque Güell", "Costo": "10€", "Link": "#"}
        ]
    },
    "8. Valencia": {
        "days": "2 Días",
        "coords": [39.4699, -0.3763],
        "image": "https://images.unsplash.com/photo-1560965319-a67500366606?auto=format&fit=crop&w=800&q=80",
        "desc": "Paella, playa y ciencias.",
        "stay": [
            {"name": "Borran Suites", "price_est": 120, "type": "Apto"},
            {"name": "Cantagua Hostel", "price_est": 80, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "detail": "Euromed (3h)", "cost": 25},
        "must_see": [
            {"Lugar": "Ciudad Artes", "Costo": "Gratis (Ext)", "Link": "#"},
            {"Lugar": "Oceanogràfic", "Costo": "35€", "Link": "#"}
        ]
    }
}

# --- 5. SIDEBAR (NAVEGACIÓN) ---
with st.sidebar:
    st.title("🇪🇺 EuroTrip 2026")
    st.markdown("Planificador Inteligente")
    
    # Menú de selección con estilo de radio
    city_list = list(trip_data.keys())
    selected_city_name = st.radio("Tu Ruta:", city_list)
    
    st.divider()
    
    # Cálculo rápido de presupuesto
    st.markdown("### 💰 Presupuesto Hoteles")
    total_est = sum([min([h['price_est'] for h in data['stay']]) for data in trip_data.values()]) * 2 # x2 noches promedio
    st.metric("Total Estimado (4 Pax)", f"{total_est}€", delta="Solo alojamiento")
    
    st.caption("ℹ️ Precios estimados. Usa los enlaces 'Ver Oferta' para precios reales.")

# --- 6. ÁREA PRINCIPAL ---
city = trip_data[selected_city_name]
prev_city_index = city_list.index(selected_city_name) - 1
prev_city_name = city_list[prev_city_index] if prev_city_index >= 0 else None

# Layout de columnas: 60% Info, 40% Mapa (Como la imagen de referencia)
col_info, col_map = st.columns([1.5, 1], gap="medium")

with col_info:
    # Encabezado visual
    st.image(city['image'], use_container_width=True)
    st.markdown(f"## {selected_city_name.split('. ')[1]}")
    st.markdown(f"**{city['days']}** • *{city['desc']}*")
    
    st.divider()
    
    # Pestañas para organizar la información limpia
    tab_stay, tab_move, tab_do = st.tabs(["🏨 Dormir", "🚆 Moverse", "📸 Conocer"])
    
    with tab_stay:
        st.info("💡 Haz clic en 'Ver Oferta' para buscar fechas exactas en Google.")
        for hotel in city['stay']:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1.5])
                c1.markdown(f"**{hotel['name']}**")
                c1.caption(hotel['type'])
                c2.markdown(f"~{hotel['price_est']}€")
                # Generador de Enlace Inteligente
                link = generar_link_hotel(hotel['name'], selected_city_name.split(". ")[1])
                c3.link_button("🔎 Ver Oferta", link)
                st.divider()

    with tab_move:
        tr = city['transport']
        st.success(f"Logística desde parada anterior")
        m1, m2, m3 = st.columns(3)
        m1.metric("Medio", tr['type'])
        m2.metric("Tiempo", tr['detail'].split('(')[-1].replace(')', ''))
        m3.metric("Costo Est.", f"{tr['cost']}€")
        
        if prev_city_name:
            origin = prev_city_name.split(". ")[1]
            dest = selected_city_name.split(". ")[1]
            link_vuelo = generar_link_vuelo(origin, dest)
            st.link_button(f"✈️ Buscar trayecto {origin} -> {dest}", link_vuelo)

    with tab_do:
        df = pd.DataFrame(city['must_see'])
        st.dataframe(
            df,
            column_config={
                "Link": st.column_config.LinkColumn("Info Web")
            },
            hide_index=True,
            use_container_width=True
        )

with col_map:
    st.markdown("### 📍 Ubicación")
    # Mapa limpio
    m = folium.Map(location=city['coords'], zoom_start=11, tiles="CartoDB positron") # CartoDB es más limpio/blanco
    
    # Marcador Actual
    folium.Marker(
        city['coords'],
        popup=selected_city_name,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # Línea de ruta
    points = [data['coords'] for data in trip_data.values()]
    folium.PolyLine(points, color="#3B82F6", weight=3, opacity=0.8).add_to(m)
    
    st_folium(m, width="100%", height=400)
    
    # Widget de clima simulado o consejos
    with st.container():
        st.markdown("#### 🎒 Tips de Viaje")
        st.markdown("""
        - **Agua:** En Roma y Nápoles es potable en las fuentes.
        - **Transporte:** Valida siempre el ticket antes de subir al tren.
        - **Seguridad:** Cuidado con carteristas en estaciones y metro.
        """)
