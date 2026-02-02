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

# --- 2. ESTILOS CSS (Solución de Visibilidad) ---
# En lugar de forzar colores fijos que chocan con el modo oscuro,
# usamos variables CSS nativas de Streamlit y estilos de tarjeta seguros.
st.markdown("""
<style>
    /* Estilo para las Tarjetas (Cards) */
    div.css-1r6slb0, .stDataFrame, .stMap, div[data-testid="stExpander"] {
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Imágenes redondeadas */
    img {
        border-radius: 8px;
    }

    /* Métrica destacada - Color de fondo suave que funciona en ambos modos */
    div[data-testid="metric-container"] {
        background-color: rgba(60, 150, 250, 0.1);
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(60, 150, 250, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES ---
def generar_link_hotel(nombre, ciudad, pais):
    query = f"{nombre} {ciudad} {pais} booking price".replace(" ", "+")
    return f"https://www.google.com/search?q={query}"

def generar_link_vuelo(origen, destino):
    return f"https://www.google.com/travel/flights?q=flights+from+{origen}+to+{destino}"

# --- 4. DATOS (Imágenes Actualizadas y Estables) ---
trip_data = {
    "1. Nápoles": {
        "days": "Llegada",
        "country": "Italia",
        "coords": [40.8518, 14.2681],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Napoli_da_Castel_Sant%27Elmo_01.jpg/800px-Napoli_da_Castel_Sant%27Elmo_01.jpg",
        "desc": "El alma vibrante del sur.",
        "stay": [
            {"name": "Bueno Hotel B&B", "price": 120, "type": "Hotel"},
            {"name": "Elite Rooms Napoli", "price": 140, "type": "Hotel"}
        ],
        "transport": {"type": "Avión", "info": "Llegada Internacional", "cost": 0},
        "must_see": [
            {"name": "Pompeya", "cost": "18€", "time": "09:00-19:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Pompeii_Forum.jpg/640px-Pompeii_Forum.jpg"},
            {"name": "Vesubio", "cost": "10€", "time": "09:00-17:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Mount_Vesuvius_as_seen_from_Pompeii.jpg/640px-Mount_Vesuvius_as_seen_from_Pompeii.jpg"}
        ]
    },
    "2. Roma": {
        "days": "2 Días",
        "country": "Italia",
        "coords": [41.9028, 12.4964],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Rome_Montage_2017.png/800px-Rome_Montage_2017.png",
        "desc": "La Ciudad Eterna.",
        "stay": [
            {"name": "Hotel Archimede", "price": 160, "type": "Hotel"},
            {"name": "The RomeHello", "price": 90, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "info": "Frecciarossa (1h 10m)", "cost": 25},
        "must_see": [
            {"name": "Coliseo", "cost": "16€", "time": "08:30-19:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/640px-Colosseo_2020.jpg"},
            {"name": "Fontana di Trevi", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Trevi_Fountain%2C_Rome%2C_Italy_2_-_May_2007.jpg/640px-Trevi_Fountain%2C_Rome%2C_Italy_2_-_May_2007.jpg"}
        ]
    },
    "3. Florencia": {
        "days": "2 Días",
        "country": "Italia",
        "coords": [43.7696, 11.2558],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Florence_montage_1.jpg/800px-Florence_montage_1.jpg",
        "desc": "Cuna del Renacimiento.",
        "stay": [
            {"name": "Florera Cinque", "price": 180, "type": "Hotel"},
            {"name": "Plus Florence", "price": 110, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "info": "Tren rápido (1h 30m)", "cost": 30},
        "must_see": [
            {"name": "Duomo", "cost": "Gratis", "time": "10:00-16:30", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Santa_Maria_del_Fiore_retouched.jpg/640px-Santa_Maria_del_Fiore_retouched.jpg"},
            {"name": "Ponte Vecchio", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Ponte_Vecchio_Florence.jpg/640px-Ponte_Vecchio_Florence.jpg"}
        ]
    },
    "4. Génova": {
        "days": "2 Días",
        "country": "Italia",
        "coords": [44.4056, 8.9463],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Genoa_collage.jpg/800px-Genoa_collage.jpg",
        "desc": "Puerto y Cinque Terre.",
        "stay": [
            {"name": "Hotel Bellevue", "price": 130, "type": "Hotel"},
            {"name": "Manena Hostel", "price": 70, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "info": "Intercity (2h 45m)", "cost": 20},
        "must_see": [
            {"name": "Cinque Terre", "cost": "18€", "time": "Día completo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Cinque_Terre_Manarola_Italy.jpg/640px-Cinque_Terre_Manarola_Italy.jpg"},
            {"name": "Acuario", "cost": "27€", "time": "09:00-20:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Acquario_di_Genova_esterno.JPG/640px-Acquario_di_Genova_esterno.JPG"}
        ]
    },
    "5. Niza": {
        "days": "1 Día",
        "country": "Francia",
        "coords": [43.7102, 7.2620],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Nice-baie-des-anges.jpg/800px-Nice-baie-des-anges.jpg",
        "desc": "Costa Azul y Mónaco.",
        "stay": [
            {"name": "Hotel Modern Waikiki", "price": 150, "type": "Hotel"},
            {"name": "Villa Saint Exupery", "price": 90, "type": "Hostal"}
        ],
        "transport": {"type": "Bus", "info": "FlixBus (3h)", "cost": 20},
        "must_see": [
            {"name": "Promenade des Anglais", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Promenade_des_Anglais_Nice.jpg/640px-Promenade_des_Anglais_Nice.jpg"},
            {"name": "Mónaco (Tren)", "cost": "5€", "time": "Tarde", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Monaco_Monte_Carlo_1.jpg/640px-Monaco_Monte_Carlo_1.jpg"}
        ]
    },
    "6. Marsella": {
        "days": "2 Días",
        "country": "Francia",
        "coords": [43.2965, 5.3698],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Vieux_Port_Marseille.jpg/800px-Vieux_Port_Marseille.jpg",
        "desc": "Puerto histórico.",
        "stay": [
            {"name": "Toyoko Inn", "price": 100, "type": "Hotel"},
            {"name": "Vertigo Vieux-Port", "price": 75, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "info": "TGV (2h 30m)", "cost": 25},
        "must_see": [
            {"name": "Notre-Dame", "cost": "Gratis", "time": "07:00-18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Marseille_Notre-Dame_de_la_Garde.jpg/640px-Marseille_Notre-Dame_de_la_Garde.jpg"},
            {"name": "Calanques", "cost": "Gratis", "time": "Día completo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Calanque_d%27En-Vau.jpg/640px-Calanque_d%27En-Vau.jpg"}
        ]
    },
    "7. Barcelona": {
        "days": "2 Días",
        "country": "España",
        "coords": [41.3851, 2.1734],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Barcelona_collage.JPG/800px-Barcelona_collage.JPG",
        "desc": "Gaudí y playa.",
        "stay": [
            {"name": "Generator", "price": 100, "type": "Hostal"},
            {"name": "Hostal Debmates", "price": 110, "type": "Pensión"}
        ],
        "transport": {"type": "Avión", "info": "Vuelo corto", "cost": 50},
        "must_see": [
            {"name": "Sagrada Familia", "cost": "26€", "time": "09:00-18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Sagrada_Familia_01.jpg/640px-Sagrada_Familia_01.jpg"},
            {"name": "Parque Güell", "cost": "10€", "time": "09:30-19:30", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Park_Guell_02.jpg/640px-Park_Guell_02.jpg"}
        ]
    },
    "8. Valencia": {
        "days": "2 Días",
        "country": "España",
        "coords": [39.4699, -0.3763],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Ciutat_de_les_Arts_i_les_Ci%C3%A8ncies_%28Valencia%29.jpg/800px-Ciutat_de_les_Arts_i_les_Ci%C3%A8ncies_%28Valencia%29.jpg",
        "desc": "Paella y Ciencias.",
        "stay": [
            {"name": "Borran Suites", "price": 120, "type": "Apto"},
            {"name": "Cantagua Hostel", "price": 80, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "info": "Euromed (3h)", "cost": 25},
        "must_see": [
            {"name": "Ciudad Artes", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/L%27Hemisf%C3%A8ric_y_el_Palau_de_les_Arts_Reina_Sof%C3%ADa_%28Valencia%29.jpg/640px-L%27Hemisf%C3%A8ric_y_el_Palau_de_les_Arts_Reina_Sof%C3%ADa_%28Valencia%29.jpg"},
            {"name": "Oceanogràfic", "cost": "35€", "time": "10:00-18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Oceanogr%C3%A0fic_Valencia.jpg/640px-Oceanogr%C3%A0fic_Valencia.jpg"}
        ]
    }
}

# --- 5. INTERFAZ PRINCIPAL ---
# Sidebar
with st.sidebar:
    st.title("🇪🇺 EuroTrip 2026")
    selected_city = st.radio("Destinos:", list(trip_data.keys()))
    
    st.divider()
    
    # --- PERSISTENCIA DE DATOS (NOTAS) ---
    st.markdown("### 📝 Notas de Viaje")
    st.caption("Escribe recordatorios aquí. (Se borran si cierras la pestaña)")
    
    # Inicializar estado si no existe
    if 'notas' not in st.session_state:
        st.session_state.notas = ""
    
    # Área de texto vinculada al estado
    notas = st.text_area("Tus apuntes:", value=st.session_state.notas, height=150)
    st.session_state.notas = notas # Guardar en memoria temporal

# Lógica Principal
city_data = trip_data[selected_city]

# Header con imagen de fondo segura
st.image(city_data['image'], use_container_width=True)
st.title(f"{selected_city.split('. ')[1]} - {city_data['country']}")
st.markdown(f"**{city_data['days']}** • {city_data['desc']}")

# Pestañas
tab1, tab2, tab3 = st.tabs(["🏨 Dormir", "🚆 Moverse", "📸 Conocer"])

with tab1:
    col_cards = st.columns(len(city_data['stay']))
    for i, hotel in enumerate(city_data['stay']):
        with col_cards[i if i < len(col_cards) else 0]:
            with st.container():
                st.subheader(hotel['name'])
                st.caption(hotel['type'])
                st.metric("Noche (4pax)", f"{hotel['price']}€")
                link = generar_link_hotel(hotel['name'], selected_city.split('. ')[1], city_data['country'])
                st.link_button("🔎 Ver Precio Real", link)

with tab2:
    t = city_data['transport']
    c1, c2, c3 = st.columns(3)
    c1.metric("Transporte", t['type'])
    c2.metric("Duración", t['info'].split('(')[-1].replace(')','') if '(' in t['info'] else "N/A")
    c3.metric("Costo Est.", f"{t['cost']}€")
    
    # Link inteligente de ejemplo
    if selected_city != "1. Nápoles":
        origin = "Origen Anterior" # Simplificación
        dest = selected_city.split('. ')[1]
        st.link_button(f"✈️ Buscar Rutas a {dest}", generar_link_vuelo("Roma", dest))

with tab3:
    st.subheader("Lugares Imperdibles")
    for place in city_data['must_see']:
        with st.expander(f"📍 {place['name']} - {place['cost']}"):
            cols = st.columns([1, 2])
            with cols[0]:
                st.image(place['img'], use_container_width=True)
            with cols[1]:
                st.write(f"**Horario:** {place['time']}")
                st.info("Tip: Compra entradas online para evitar filas.")

# Mapa
st.subheader("📍 Mapa de Ubicación")
m = folium.Map(location=city_data['coords'], zoom_start=12, tiles="CartoDB positron")
folium.Marker(city_data['coords'], popup=selected_city, icon=folium.Icon(color="blue")).add_to(m)
route = [data['coords'] for data in trip_data.values()]
folium.PolyLine(route, color="gray", weight=2, opacity=0.5, dash_array='5, 10').add_to(m)
st_folium(m, height=400, use_container_width=True)
