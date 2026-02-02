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

# --- 2. CSS FORZADO (MODO CLARO + CORRECCIONES) ---
st.markdown("""
<style>
    /* FORZAR MODO CLARO EN TEXTOS */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Fondo principal */
    .stApp {
        background-color: #F0F2F6;
    }
    
    /* Forzar color de texto negro para que no se pierda en fondos blancos */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #1F2937 !important;
    }
    
    /* Excepción: Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Tarjetas blancas (Cards) */
    div.css-1r6slb0, .stDataFrame, .stMap, div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #E5E7EB;
    }
    
    /* Botones y Enlaces */
    a { color: #2563EB !important; text-decoration: none; }
    a:hover { text-decoration: underline; }
    
    /* Botón primario */
    .stButton>button {
        color: #FFFFFF !important;
        background-color: #2563EB;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Métricas */
    div[data-testid="metric-container"] {
        background-color: #EFF6FF !important;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 10px;
    }
    div[data-testid="metric-container"] label {
        color: #3B82F6 !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1E40AF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES INTELIGENTES ---

def generar_link_hotel(nombre_hotel, ciudad, pais):
    """Búsqueda precisa incluyendo el país"""
    query = f"{nombre_hotel} {ciudad} {pais} hotel price".replace(" ", "+")
    return f"https://www.google.com/search?q={query}"

def generar_link_vuelo(origen, destino):
    return f"https://www.google.com/travel/flights?q=flights+from+{origen}+to+{destino}"

# --- 4. BASE DE DATOS MEJORADA (IMÁGENES ESTABLES) ---
trip_data = {
    "1. Nápoles": {
        "days": "Llegada",
        "country": "Italia",
        "coords": [40.8518, 14.2681],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Posillipo_Italy.jpg/1280px-Posillipo_Italy.jpg",
        "desc": "El alma vibrante del sur. Pizza auténtica, caos encantador y vistas al Vesubio.",
        "stay": [
            {"name": "Bueno Hotel B&B", "price_est": 120, "type": "Hotel"},
            {"name": "Elite Rooms Napoli", "price_est": 140, "type": "Hotel"},
            {"name": "Hostel of the Sun", "price_est": 80, "type": "Hostal"}
        ],
        "transport": {"type": "Avión", "detail": "Llegada Intl.", "cost": 0},
        "must_see": [
            {"name": "Parque Arqueológico de Pompeya", "cost": "18€", "time": "09:00 - 19:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Pompeii_Forum.jpg/800px-Pompeii_Forum.jpg"},
            {"name": "Monte Vesubio", "cost": "10€", "time": "09:00 - 17:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Mount_Vesuvius_as_seen_from_Pompeii.jpg/800px-Mount_Vesuvius_as_seen_from_Pompeii.jpg"},
            {"name": "Spaccanapoli y Centro Histórico", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Spaccanapoli_dal_Vomero.jpg/800px-Spaccanapoli_dal_Vomero.jpg"},
            {"name": "Cristo Velado (Capilla Sansevero)", "cost": "10€", "time": "09:00 - 18:30", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Cristo_velato_Napoli_2017.jpg/640px-Cristo_velato_Napoli_2017.jpg"}
        ]
    },
    "2. Roma": {
        "days": "2 Días",
        "country": "Italia",
        "coords": [41.9028, 12.4964],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/St_Peter%27s_Square%2C_Vatican_City_-_April_2007.jpg/1280px-St_Peter%27s_Square%2C_Vatican_City_-_April_2007.jpg",
        "desc": "La Ciudad Eterna. Un museo al aire libre donde cada piedra cuenta una historia.",
        "stay": [
            {"name": "Hotel Archimede", "price_est": 160, "type": "Hotel"},
            {"name": "Grand Hotel Colony", "price_est": 150, "type": "Hotel"},
            {"name": "The RomeHello", "price_est": 90, "type": "Hostal Top"}
        ],
        "transport": {"type": "Tren", "detail": "Frecciarossa (1h 10m)", "cost": 25},
        "must_see": [
            {"name": "Coliseo Romano", "cost": "16€", "time": "08:30 - 19:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/800px-Colosseo_2020.jpg"},
            {"name": "Fontana di Trevi", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Trevi_Fountain%2C_Rome%2C_Italy_2_-_May_2007.jpg/800px-Trevi_Fountain%2C_Rome%2C_Italy_2_-_May_2007.jpg"},
            {"name": "Museos Vaticanos y Capilla Sixtina", "cost": "17€", "time": "09:00 - 18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Creaci%C3%B3n_de_Ad%C3%A1n.jpg/800px-Creaci%C3%B3n_de_Ad%C3%A1n.jpg"},
            {"name": "Panteón de Agripa", "cost": "5€", "time": "09:00 - 19:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Pantheon_Rome_BM.jpg/800px-Pantheon_Rome_BM.jpg"}
        ]
    },
    "3. Florencia": {
        "days": "2 Días",
        "country": "Italia",
        "coords": [43.7696, 11.2558],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Florence_montage_1.jpg/800px-Florence_montage_1.jpg",
        "desc": "Cuna del Renacimiento. Arte, arquitectura y la mejor carne de la Toscana.",
        "stay": [
            {"name": "Florera Cinque", "price_est": 180, "type": "Hotel"},
            {"name": "Plus Florence", "price_est": 110, "type": "Hostal con Piscina"}
        ],
        "transport": {"type": "Tren", "detail": "Tren rápido (1h 30m)", "cost": 30},
        "must_see": [
            {"name": "Catedral Santa María del Fiore (Duomo)", "cost": "Gratis", "time": "10:00 - 16:30", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Santa_Maria_del_Fiore_retouched.jpg/800px-Santa_Maria_del_Fiore_retouched.jpg"},
            {"name": "Galería Uffizi", "cost": "25€", "time": "08:15 - 18:30", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Florence_Uffizi_View.jpg/800px-Florence_Uffizi_View.jpg"},
            {"name": "Ponte Vecchio", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Ponte_Vecchio_Florence.jpg/800px-Ponte_Vecchio_Florence.jpg"},
            {"name": "Torre de Pisa (Excursión)", "cost": "20€ (subir)", "time": "Medio día", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/The_Leaning_Tower_of_Pisa_SB.jpeg/800px-The_Leaning_Tower_of_Pisa_SB.jpeg"}
        ]
    },
    "4. Génova": {
        "days": "2 Días",
        "country": "Italia",
        "coords": [44.4056, 8.9463],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Genoa_collage.jpg/800px-Genoa_collage.jpg",
        "desc": "Puerto laberíntico. El punto de partida perfecto para Cinque Terre.",
        "stay": [
            {"name": "Hotel Bellevue", "price_est": 130, "type": "Hotel"},
            {"name": "Manena Hostel", "price_est": 70, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "detail": "Intercity (2h 45m)", "cost": 20},
        "must_see": [
            {"name": "Cinque Terre (Riomaggiore, Manarola)", "cost": "18€ (Tren)", "time": "Día Completo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Cinque_Terre_Manarola_Italy.jpg/800px-Cinque_Terre_Manarola_Italy.jpg"},
            {"name": "Boccadasse", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Boccadasse_genova.jpg/800px-Boccadasse_genova.jpg"},
            {"name": "Acuario de Génova", "cost": "27€", "time": "09:00 - 20:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Acquario_di_Genova_esterno.JPG/800px-Acquario_di_Genova_esterno.JPG"}
        ]
    },
    "5. Niza": {
        "days": "1 Día",
        "country": "Francia",
        "coords": [43.7102, 7.2620],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Nice-baie-des-anges.jpg/1280px-Nice-baie-des-anges.jpg",
        "desc": "La joya de la Costa Azul. Playas de guijarros y proximidad a Mónaco.",
        "stay": [
            {"name": "Hotel Modern Waikiki", "price_est": 150, "type": "Hotel"},
            {"name": "Villa Saint Exupery Beach", "price_est": 90, "type": "Hostal"}
        ],
        "transport": {"type": "Bus/Tren", "detail": "FlixBus (3h)", "cost": 20},
        "must_see": [
            {"name": "Promenade des Anglais", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Promenade_des_Anglais_Nice.jpg/800px-Promenade_des_Anglais_Nice.jpg"},
            {"name": "Excursión a Mónaco / Montecarlo", "cost": "5€ (Tren)", "time": "Tarde", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Monaco_Monte_Carlo_1.jpg/800px-Monaco_Monte_Carlo_1.jpg"},
            {"name": "Colina del Castillo (Vistas)", "cost": "Gratis", "time": "08:30 - 20:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Nice_Colline_du_Chateau_Wasserfall.jpg/800px-Nice_Colline_du_Chateau_Wasserfall.jpg"}
        ]
    },
    "6. Marsella": {
        "days": "2 Días",
        "country": "Francia",
        "coords": [43.2965, 5.3698],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Vieux_Port_Marseille.jpg/1280px-Vieux_Port_Marseille.jpg",
        "desc": "Puerto histórico y puerta a las impresionantes Calanques.",
        "stay": [
            {"name": "Toyoko Inn Marseille", "price_est": 100, "type": "Hotel"},
            {"name": "Vertigo Vieux-Port", "price_est": 75, "type": "Hostal"}
        ],
        "transport": {"type": "Tren/Bus", "detail": "TGV o Bus (2h 30m)", "cost": 25},
        "must_see": [
            {"name": "Basílica Notre-Dame de la Garde", "cost": "Gratis", "time": "07:00 - 18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Marseille_Notre-Dame_de_la_Garde.jpg/800px-Marseille_Notre-Dame_de_la_Garde.jpg"},
            {"name": "Parque Nacional de Calanques", "cost": "Gratis (Barco 30€)", "time": "Día Completo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Calanque_d%27En-Vau.jpg/800px-Calanque_d%27En-Vau.jpg"},
            {"name": "Vieux Port (Puerto Viejo)", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Vieux_Port_Marseille_soir.jpg/800px-Vieux_Port_Marseille_soir.jpg"}
        ]
    },
    "7. Barcelona": {
        "days": "2 Días",
        "country": "España",
        "coords": [41.3851, 2.1734],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Barcelona_collage.JPG/800px-Barcelona_collage.JPG",
        "desc": "Arquitectura de Gaudí, tapas increíbles y ambiente mediterráneo.",
        "stay": [
            {"name": "Generator Barcelona", "price_est": 100, "type": "Hostal Premium"},
            {"name": "Hostal Debmates", "price_est": 110, "type": "Pensión"}
        ],
        "transport": {"type": "Tren/Avión", "detail": "Larga distancia (4h+)", "cost": 50},
        "must_see": [
            {"name": "La Sagrada Familia", "cost": "26€", "time": "09:00 - 18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Sagrada_Familia_01.jpg/800px-Sagrada_Familia_01.jpg"},
            {"name": "Parque Güell", "cost": "10€", "time": "09:30 - 19:30", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Park_Guell_02.jpg/800px-Park_Guell_02.jpg"},
            {"name": "Barrio Gótico", "cost": "Gratis", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Carrer_del_Bisbe_in_Barcelona.jpg/800px-Carrer_del_Bisbe_in_Barcelona.jpg"}
        ]
    },
    "8. Valencia": {
        "days": "2 Días",
        "country": "España",
        "coords": [39.4699, -0.3763],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Ciutat_de_les_Arts_i_les_Ci%C3%A8ncies_%28Valencia%29.jpg/1280px-Ciutat_de_les_Arts_i_les_Ci%C3%A8ncies_%28Valencia%29.jpg",
        "desc": "La ciudad de la luz, la paella original y arquitectura futurista.",
        "stay": [
            {"name": "Borran Suites", "price_est": 120, "type": "Apto"},
            {"name": "Cantagua Hostel", "price_est": 80, "type": "Hostal"}
        ],
        "transport": {"type": "Tren", "detail": "Euromed (3h)", "cost": 25},
        "must_see": [
            {"name": "Ciudad de las Artes y las Ciencias", "cost": "Gratis (Ext)", "time": "24h", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/L%27Hemisf%C3%A8ric_y_el_Palau_de_les_Arts_Reina_Sof%C3%ADa_%28Valencia%29.jpg/800px-L%27Hemisf%C3%A8ric_y_el_Palau_de_les_Arts_Reina_Sof%C3%ADa_%28Valencia%29.jpg"},
            {"name": "Oceanogràfic", "cost": "35€", "time": "10:00 - 18:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Oceanogr%C3%A0fic_Valencia.jpg/800px-Oceanogr%C3%A0fic_Valencia.jpg"},
            {"name": "Mercado Central", "cost": "Gratis", "time": "07:30 - 15:00", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Mercado_Central_de_Valencia_03.jpg/800px-Mercado_Central_de_Valencia_03.jpg"}
        ]
    }
}

# --- 5. SIDEBAR (NAVEGACIÓN) ---
with st.sidebar:
    st.title("🇪🇺 EuroTrip 2026")
    st.markdown("Planificador Inteligente")
    
    city_list = list(trip_data.keys())
    selected_city_name = st.radio("Tu Ruta:", city_list)
    
    st.divider()
    
    st.markdown("### 💰 Presupuesto Hoteles")
    total_est = sum([min([h['price_est'] for h in data['stay']]) for data in trip_data.values()]) * 2
    st.metric("Total Estimado (4 Pax)", f"{total_est}€", delta="Solo alojamiento")
    
    st.caption("ℹ️ Precios estimados. Usa los enlaces 'Ver Oferta' para precios reales.")

# --- 6. ÁREA PRINCIPAL ---
city = trip_data[selected_city_name]
prev_city_index = city_list.index(selected_city_name) - 1
prev_city_name = city_list[prev_city_index] if prev_city_index >= 0 else None

# Layout
col_info, col_map = st.columns([1.5, 1], gap="medium")

with col_info:
    # IMAGEN HERO PRINCIPAL
    st.image(city['image'], use_container_width=True)
    
    st.markdown(f"## {selected_city_name.split('. ')[1]}")
    st.markdown(f"**{city['days']}** • *{city['desc']}*")
    
    st.divider()
    
    # PESTAÑAS
    tab_stay, tab_move, tab_do = st.tabs(["🏨 Dormir", "🚆 Moverse", "📸 Conocer"])
    
    with tab_stay:
        st.info(f"💡 Buscando ofertas en **{city['country']}**. Haz clic en 'Ver Oferta' para precios reales.")
        for hotel in city['stay']:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1.5])
                with c1:
                    st.markdown(f"**{hotel['name']}**")
                    st.caption(hotel['type'])
                with c2:
                    st.markdown(f"**~{hotel['price_est']}€**")
                    st.caption("por noche")
                with c3:
                    # Link inteligente con PAÍS incluido
                    link = generar_link_hotel(hotel['name'], selected_city_name.split(". ")[1], city['country'])
                    st.link_button("🔎 Ver Oferta", link)
                st.divider()

    with tab_move:
        tr = city['transport']
        st.success(f"Logística de llegada")
        m1, m2, m3 = st.columns(3)
        m1.metric("Medio", tr['type'])
        m2.metric("Tiempo", tr['detail'].split('(')[-1].replace(')', '') if '(' in tr['detail'] else "N/A")
        m3.metric("Costo", f"{tr['cost']}€")
        
        st.markdown(f"**Detalle:** {tr['detail']}")
        
        if prev_city_name:
            origin = prev_city_name.split(". ")[1]
            dest = selected_city_name.split(". ")[1]
            link_vuelo = generar_link_vuelo(origin, dest)
            st.link_button(f"✈️ Buscar trayecto {origin} -> {dest}", link_vuelo)

    with tab_do:
        st.markdown("### Lugares Imperdibles")
        # Diseño visual de actividades con imagen
        for place in city['must_see']:
            with st.expander(f"📍 {place['name']}", expanded=False):
                col_img, col_txt = st.columns([1, 1.5])
                with col_img:
                    st.image(place['img'], use_container_width=True)
                with col_txt:
                    st.markdown(f"**Costo:** {place['cost']}")
                    st.markdown(f"**Horario:** {place['time']}")
                    st.caption("Sugerencia inteligente basada en popularidad y cercanía.")

with col_map:
    st.markdown("### 📍 Ubicación")
    m = folium.Map(location=city['coords'], zoom_start=12, tiles="CartoDB positron")
    
    # Marcador de ciudad
    folium.Marker(
        city['coords'],
        popup=selected_city_name,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # Ruta completa
    points = [data['coords'] for data in trip_data.values()]
    folium.PolyLine(points, color="#2563EB", weight=4, opacity=0.7).add_to(m)
    
    st_folium(m, width="100%", height=450)
    
    with st.container():
        st.markdown("#### 🎒 Tips de Viaje")
        st.info("Guarda una copia digital de tu pasaporte. En Italia y Francia se cobra tasa turística en hoteles (aprox 2-5€ por noche/persona) que se paga en el sitio.")
