import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="EuroTrip 2026 Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Para imitar el diseño de la imagen) ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 { color: #1E3A8A; }
    h2 { color: #3B82F6; font-size: 1.5rem; }
    h3 { font-size: 1.2rem; color: #4B5563; }
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #EFF6FF;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #BFDBFE;
    }
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- DATOS DEL VIAJE (Base de datos estructurada) ---
# He organizado la ruta optimizada geográficamente para reducir tiempos.
trip_data = {
    "1. Nápoles": {
        "days": "Llegada",
        "coords": [40.8518, 14.2681],
        "desc": "El alma vibrante de Italia. Pizza, historia y caos encantador.",
        "image": "https://images.unsplash.com/photo-1596811466030-9b3621495c6f?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Bueno Hotel B&B", "price": 120, "rating": 4.2, "type": "Hotel"},
            {"name": "Elite Rooms Napoli", "price": 140, "rating": 4.5, "type": "Hotel"},
            {"name": "Be Italian Flat San Felice", "price": 135, "rating": 4.3, "type": "Apartamento"},
            {"name": "Hostel of the Sun (Opción Económica)", "price": 80, "rating": 4.6, "type": "Hostal"},
            {"name": "La Controra Hostel Naples", "price": 75, "rating": 4.4, "type": "Hostal"}
        ],
        "transport_in": {"type": "Avión", "info": "Llegada Internacional", "cost": 0, "time": "N/A"},
        "must_see": [
            {"name": "Pompeya", "cost": "18€", "hours": "09:00 - 19:00"},
            {"name": "Vesubio", "cost": "10€", "hours": "09:00 - 17:00"},
            {"name": "Spaccanapoli", "cost": "Gratis", "hours": "24h"},
            {"name": "Museo Arqueológico", "cost": "15€", "hours": "09:00 - 19:30"},
            {"name": "Castel dell'Ovo", "cost": "Gratis", "hours": "09:00 - 18:00"},
            {"name": "Piazza del Plebiscito", "cost": "Gratis", "hours": "24h"},
            {"name": "Capilla Sansevero", "cost": "8€", "hours": "09:00 - 18:30"},
            {"name": "Catacumbas de San Gennaro", "cost": "9€", "hours": "10:00 - 17:00"},
            {"name": "Nápoles Subterránea", "cost": "10€", "hours": "10:00 - 18:00"},
            {"name": "Galería Umberto I", "cost": "Gratis", "hours": "24h"}
        ],
        "food": ["Sorbillo (Pizza)", "Da Michele (Pizza)", "Tandem Ragù", "Trattoria Nennella", "Sfogliatella Mary", "Pizzeria Starita", "Pescheria Azzurra", "Gran Caffè Gambrinus"]
    },
    "2. Roma": {
        "days": "2 Días",
        "coords": [41.9028, 12.4964],
        "desc": "La Ciudad Eterna. Un museo al aire libre.",
        "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Hotel Archimede", "price": 160, "rating": 4.0, "type": "Hotel"},
            {"name": "Grand Hotel Colony", "price": 150, "rating": 3.9, "type": "Hotel"},
            {"name": "LH Hotel Excel Roma", "price": 170, "rating": 4.1, "type": "Hotel"},
            {"name": "Pharma Luxury Hotel", "price": 190, "rating": 4.5, "type": "Hotel"},
            {"name": "The RomeHello (Económico)", "price": 100, "rating": 4.8, "type": "Hostal"},
            {"name": "YellowSquare Rome", "price": 90, "rating": 4.5, "type": "Hostal"}
        ],
        "transport_in": {"type": "Tren Alta Velocidad", "info": "Frecciarossa desde Nápoles", "cost": 25, "time": "1h 10m"},
        "must_see": [
            {"name": "Coliseo", "cost": "16€", "hours": "08:30 - 19:00"},
            {"name": "Foro Romano", "cost": "Incluido", "hours": "08:30 - 19:00"},
            {"name": "Vaticano (Museos)", "cost": "17€", "hours": "09:00 - 18:00"},
            {"name": "Basílica de San Pedro", "cost": "Gratis", "hours": "07:00 - 19:00"},
            {"name": "Panteón", "cost": "5€", "hours": "09:00 - 19:00"},
            {"name": "Fontana di Trevi", "cost": "Gratis", "hours": "24h"},
            {"name": "Plaza Navona", "cost": "Gratis", "hours": "24h"},
            {"name": "Plaza de España", "cost": "Gratis", "hours": "24h"},
            {"name": "Castillo Sant'Angelo", "cost": "15€", "hours": "09:00 - 19:30"},
            {"name": "Trastevere (Barrio)", "cost": "Gratis", "hours": "24h"}
        ],
        "food": ["Tonnarello (Pasta)", "Da Enzo al 29", "Roscioli", "Pizzeria Ai Marmi", "Trapizzino", "Osteria da Fortunata", "Giolitti (Helado)", "Supplizio"]
    },
    "3. Florencia (y Pisa)": {
        "days": "2 Días",
        "coords": [43.7696, 11.2558],
        "desc": "Cuna del Renacimiento. Pisa se visita de camino en tren.",
        "image": "https://images.unsplash.com/photo-1543429776-2782fc8e1acd?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Florera Cinque (Referencia usuario)", "price": 180, "rating": 4.2, "type": "Hotel"},
            {"name": "Plus Florence", "price": 110, "rating": 4.5, "type": "Hostal/Hotel"},
            {"name": "Archi Rossi Hostel", "price": 95, "rating": 4.6, "type": "Hostal"}
        ],
        "transport_in": {"type": "Tren", "info": "Roma -> Florencia", "cost": 30, "time": "1h 30m"},
        "must_see": [
            {"name": "Torre de Pisa (Escala)", "cost": "20€ (subir)", "hours": "09:00 - 18:00"},
            {"name": "Catedral (Duomo)", "cost": "Gratis", "hours": "10:00 - 16:30"},
            {"name": "Cúpula de Brunelleschi", "cost": "20€", "hours": "08:15 - 19:00"},
            {"name": "Galería Uffizi", "cost": "25€", "hours": "08:15 - 18:30"},
            {"name": "Galería de la Academia (David)", "cost": "12€", "hours": "08:15 - 18:50"},
            {"name": "Ponte Vecchio", "cost": "Gratis", "hours": "24h"},
            {"name": "Piazzale Michelangelo", "cost": "Gratis", "hours": "24h"},
            {"name": "Palazzo Vecchio", "cost": "12.50€", "hours": "09:00 - 19:00"},
            {"name": "Jardines de Boboli", "cost": "10€", "hours": "08:15 - 18:30"},
            {"name": "Mercado Central", "cost": "Gratis", "hours": "10:00 - 00:00"}
        ],
        "food": ["All'Antico Vinaio (Sandwiches)", "Trattoria Za Za", "Mercato Centrale", "Osteria Santo Spirito", "Gusta Pizza", "I'Pizzacchiere", "Gelateria La Carraia", "Trattoria Mario"]
    },
    "4. Génova (y Cinque Terre)": {
        "days": "2 Días",
        "coords": [44.4056, 8.9463],
        "desc": "Puerto histórico. Base estratégica para visitar Cinque Terre.",
        "image": "https://images.unsplash.com/photo-1596323089406-8d697818df4d?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Hotel Bellevue", "price": 130, "rating": 4.0, "type": "Hotel"},
            {"name": "Hotel Nuovo Nord", "price": 125, "rating": 3.9, "type": "Hotel"},
            {"name": "Riva Superior", "price": 145, "rating": 4.3, "type": "Hotel"},
            {"name": "Manena Hostel", "price": 70, "rating": 4.7, "type": "Hostal"},
            {"name": "Ostello Bello Genova", "price": 85, "rating": 4.6, "type": "Hostal"}
        ],
        "transport_in": {"type": "Tren", "info": "Florencia -> Pisa -> Génova", "cost": 20, "time": "2h 45m"},
        "must_see": [
            {"name": "Cinque Terre (Día completo)", "cost": "18€ (Tren)", "hours": "Todo el día"},
            {"name": "Acuario de Génova", "cost": "27€", "hours": "09:00 - 20:00"},
            {"name": "Boccadasse", "cost": "Gratis", "hours": "24h"},
            {"name": "Palazzi dei Rolli", "cost": "Varía", "hours": "10:00 - 18:00"},
            {"name": "Catedral de San Lorenzo", "cost": "Gratis", "hours": "08:00 - 19:00"},
            {"name": "Galata Museo del Mar", "cost": "17€", "hours": "10:00 - 19:00"},
            {"name": "Spianata Castelletto", "cost": "Gratis", "hours": "24h"},
            {"name": "Via Garibaldi", "cost": "Gratis", "hours": "24h"},
            {"name": "Lanterna (Faro)", "cost": "8€", "hours": "14:30 - 18:30"},
            {"name": "Puerto Antiguo", "cost": "Gratis", "hours": "24h"}
        ],
        "food": ["Il Genovese (Pesto)", "Sa Pesta", "Gran Ristoro", "Cavour 21", "Zimino", "Mugugno", "Trattoria Rosmarino", "Panificio Mario"]
    },
    "5. Niza (Costa Azul)": {
        "days": "1 Día",
        "coords": [43.7102, 7.2620],
        "desc": "El glamour de la Riviera Francesa. Mónaco está a 20 min en tren.",
        "image": "https://images.unsplash.com/photo-1533634064038-1634623719b3?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Adonis Mouia Zenoa (Cannes area)", "price": 140, "rating": 3.8, "type": "Hotel"},
            {"name": "Hotel Modern Waikiki (Cannes)", "price": 150, "rating": 4.0, "type": "Hotel"},
            {"name": "B&B Hotel Cannes La Bocca", "price": 110, "rating": 3.9, "type": "Hotel"},
            {"name": "Villa Saint Exupery Beach", "price": 90, "rating": 4.4, "type": "Hostal"},
            {"name": "Meyerbeer Beach", "price": 85, "rating": 4.3, "type": "Hostal"}
        ],
        "transport_in": {"type": "Autobús / Tren", "info": "FlixBus o Thello desde Génova", "cost": 20, "time": "3h"},
        "must_see": [
            {"name": "Promenade des Anglais", "cost": "Gratis", "hours": "24h"},
            {"name": "Colina del Castillo", "cost": "Gratis", "hours": "08:30 - 20:00"},
            {"name": "Mercado Cours Saleya", "cost": "Gratis", "hours": "06:00 - 17:30"},
            {"name": "Monaco (Excursión)", "cost": "5€ (Tren)", "hours": "Medio día"},
            {"name": "Vieille Ville", "cost": "Gratis", "hours": "24h"},
            {"name": "Museo Chagall", "cost": "10€", "hours": "10:00 - 18:00"},
            {"name": "Museo Matisse", "cost": "10€", "hours": "10:00 - 18:00"},
            {"name": "Plaza Masséna", "cost": "Gratis", "hours": "24h"},
            {"name": "Playa de Niza", "cost": "Gratis", "hours": "24h"},
            {"name": "Catedral San Nicolás", "cost": "Gratis", "hours": "09:00 - 18:00"}
        ],
        "food": ["Chez Acchiardo", "La Rossettisserie", "Chez Pipo (Socca)", "Le Plongeoir (Caro/Vista)", "Voyageur Nissart", "Lou Pilha Leva", "Fenocchio (Helados)", "Bistrot d'Antoine"]
    },
    "6. Marsella": {
        "days": "2 Días",
        "coords": [43.2965, 5.3698],
        "desc": "Puerto histórico, calanques y cultura mediterránea.",
        "image": "https://images.unsplash.com/photo-1549280965-0e2384a7d4f9?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Toyoko Inn Marseille", "price": 100, "rating": 4.1, "type": "Hotel"},
            {"name": "Montempo Marseille Centre", "price": 95, "rating": 3.9, "type": "Hotel"},
            {"name": "B&B Marseille Port", "price": 90, "rating": 4.0, "type": "Hotel"},
            {"name": "The People Hostel - Marseille", "price": 80, "rating": 4.6, "type": "Hostal"},
            {"name": "Vertigo Vieux-Port", "price": 75, "rating": 4.4, "type": "Hostal"}
        ],
        "transport_in": {"type": "Tren/Bus", "info": "TGV o Bus desde Niza", "cost": 25, "time": "2h 30m"},
        "must_see": [
            {"name": "Basílica Notre-Dame", "cost": "Gratis", "hours": "07:00 - 18:15"},
            {"name": "Vieux Port", "cost": "Gratis", "hours": "24h"},
            {"name": "MuCEM", "cost": "11€", "hours": "10:00 - 19:00"},
            {"name": "Le Panier (Barrio)", "cost": "Gratis", "hours": "24h"},
            {"name": "Parque Nacional Calanques", "cost": "Gratis", "hours": "Día completo"},
            {"name": "Château d'If", "cost": "6€", "hours": "10:00 - 17:00"},
            {"name": "Catedral de la Mayor", "cost": "Gratis", "hours": "10:00 - 19:00"},
            {"name": "Palacio Longchamp", "cost": "Gratis", "hours": "08:00 - 19:00"},
            {"name": "Abadía de San Víctor", "cost": "Gratis", "hours": "09:00 - 19:00"},
            {"name": "La Corniche", "cost": "Gratis", "hours": "24h"}
        ],
        "food": ["Chez Fonfon (Bouillabaisse)", "Toinou (Marisco)", "Le Mirza", "Pizzeria Etienne", "La Boîte à Sardine", "L'Epuisette", "Le Bouchon Provençal", "Vanille Noire"]
    },
    "7. Barcelona": {
        "days": "2 Días",
        "coords": [41.3851, 2.1734],
        "desc": "Gaudí, playa y tapas. Arquitectura modernista única.",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Hostal Debmates (Ref usuario)", "price": 110, "rating": 4.0, "type": "Hostal/Pensión"},
            {"name": "Generator Barcelona", "price": 100, "rating": 4.4, "type": "Hostal Premium"},
            {"name": "Yeah Hostel Barcelona", "price": 95, "rating": 4.7, "type": "Hostal"},
            {"name": "St Christopher's Inn", "price": 90, "rating": 4.3, "type": "Hostal"}
        ],
        "transport_in": {"type": "Tren Alta Vel / Avión", "info": "Renfe/SNCF desde Marsella", "cost": 50, "time": "4h 30m"},
        "must_see": [
            {"name": "Sagrada Familia", "cost": "26€", "hours": "09:00 - 18:00"},
            {"name": "Parque Güell", "cost": "10€", "hours": "09:30 - 19:30"},
            {"name": "Casa Batlló", "cost": "35€", "hours": "09:00 - 20:00"},
            {"name": "Barrio Gótico", "cost": "Gratis", "hours": "24h"},
            {"name": "La Rambla / Boquería", "cost": "Gratis", "hours": "08:00 - 20:30"},
            {"name": "Playa de la Barceloneta", "cost": "Gratis", "hours": "24h"},
            {"name": "Montjuïc (Fuente Mágica)", "cost": "Gratis", "hours": "Noche"},
            {"name": "La Pedrera (Casa Milà)", "cost": "25€", "hours": "09:00 - 20:30"},
            {"name": "Catedral de Barcelona", "cost": "9€", "hours": "10:00 - 18:30"},
            {"name": "Bunkers del Carmel", "cost": "Gratis", "hours": "24h"}
        ],
        "food": ["Cervecería Catalana", "El Xampanyet", "La Cova Fumada", "Bar Cañete", "Can Paixano", "Bacoa (Hamburguesas)", "Bo de B", "Els Sortidors del Parlament"]
    },
    "8. Valencia": {
        "days": "2 Días",
        "coords": [39.4699, -0.3763],
        "desc": "Ciudad de las Artes, Paella y playas inmensas.",
        "image": "https://images.unsplash.com/photo-1560965319-a67500366606?q=80&w=1000&auto=format&fit=crop",
        "stay": [
            {"name": "Borran Suites El Cabañal", "price": 120, "rating": 4.3, "type": "Apartamento"},
            {"name": "Hotel Turia Valencia", "price": 110, "rating": 4.0, "type": "Hotel"},
            {"name": "Cantagua Hostel", "price": 80, "rating": 4.8, "type": "Hostal"},
            {"name": "The River Hostel", "price": 75, "rating": 4.2, "type": "Hostal"}
        ],
        "transport_in": {"type": "Tren Euromed", "info": "Barcelona -> Valencia", "cost": 25, "time": "3h"},
        "must_see": [
            {"name": "Ciudad de las Artes", "cost": "Gratis (Exterior)", "hours": "24h"},
            {"name": "Oceanogràfic", "cost": "35€", "hours": "10:00 - 18:00"},
            {"name": "Mercado Central", "cost": "Gratis", "hours": "07:30 - 15:00"},
            {"name": "La Lonja de la Seda", "cost": "2€", "hours": "10:00 - 19:00"},
            {"name": "Catedral y El Miguelete", "cost": "8€", "hours": "10:00 - 18:30"},
            {"name": "Torres de Serranos", "cost": "2€", "hours": "10:00 - 19:00"},
            {"name": "Playa de la Malvarrosa", "cost": "Gratis", "hours": "24h"},
            {"name": "Barrio del Carmen", "cost": "Gratis", "hours": "24h"},
            {"name": "Jardines del Turia", "cost": "Gratis", "hours": "24h"},
            {"name": "Bioparc", "cost": "26€", "hours": "10:00 - 18:00"}
        ],
        "food": ["Casa Carmela (Paella)", "La Pepica", "Central Bar", "Horchatería Santa Catalina", "Bar Ricart", "Bodega Casa Montaña", "Restaurante Navarro", "La Pilareta"]
    }
}

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=80)
    st.title("EuroTrip 2026")
    st.caption("Planificador Interactivo • 4 Viajeros")
    
    st.markdown("### 🗺️ Tu Ruta")
    
    # Selector de destino
    selected_city_name = st.radio(
        "Selecciona parada:",
        list(trip_data.keys()),
        index=0
    )
    
    st.divider()
    
    # Resumen de Costos Estimados (Global)
    total_hotel_min = sum([min([h['price'] for h in data['stay']]) for data in trip_data.values()]) * 2 # Estimado x días promedio
    
    st.markdown("### 💶 Estimación Total")
    st.metric("Hoteles (Aprox)", f"€{total_hotel_min * 2}", delta="Para 4 personas")
    st.caption("*Precios estimados para 2026 con inflación*")
    
    st.info("💡 Consejo: Reserva los trenes con 3 meses de antelación para ahorrar un 40%.")

# --- LÓGICA PRINCIPAL ---
city_data = trip_data[selected_city_name]

# Título y Hero Image
col_hero, col_map = st.columns([1.5, 1])

with col_hero:
    st.image(city_data['image'], use_container_width=True)
    st.title(selected_city_name.split(". ")[1])
    st.markdown(f"**{city_data['days']}** • *{city_data['desc']}*")

    # Pestañas de información
    tab1, tab2, tab3, tab4 = st.tabs(["🏨 Alojamiento", "🚅 Trayecto", "📸 Lugares Top 10", "🍴 Restaurantes"])

    with tab1:
        st.subheader(f"Opciones de Alojamiento (4 Pax)")
        for hotel in city_data['stay']:
            with st.expander(f"{hotel['type']}: {hotel['name']} - ⭐ {hotel['rating']}"):
                c1, c2 = st.columns([3,1])
                with c1:
                    st.write(f"**Opción seleccionada/recomendada.**")
                    if hotel['type'] == "Hostal":
                        st.write("✅ Opción económica sugerida")
                with c2:
                    st.metric("Precio/Noche", f"€{hotel['price']}")
                st.button(f"Verificar disponibilidad {hotel['name']}", key=f"btn_{hotel['name']}")

    with tab2:
        st.subheader("Cómo llegar")
        transport = city_data['transport_in']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Medio", transport['type'], "Recomendado")
        c2.metric("Costo Promedio", f"€{transport['cost']}", "Por persona")
        c3.metric("Tiempo", transport['time'])
        
        st.write(f"**Detalle:** {transport['info']}")
        st.warning("⚠️ Los precios de 2026 pueden variar. Considera comprar Eurail Pass para el grupo.")

    with tab3:
        st.subheader("Imperdibles")
        df_places = pd.DataFrame(city_data['must_see'])
        st.dataframe(
            df_places, 
            column_config={
                "name": "Lugar",
                "cost": "Entrada",
                "hours": "Horario"
            },
            hide_index=True,
            use_container_width=True
        )

    with tab4:
        st.subheader("Gastronomía Local (Calidad/Precio)")
        # Mostrar en chips o lista limpia
        cols = st.columns(2)
        for i, resto in enumerate(city_data['food']):
            if i % 2 == 0:
                cols[0].success(f"🍽️ {resto}")
            else:
                cols[1].success(f"🍽️ {resto}")

# --- MAPA INTERACTIVO (Columna Derecha) ---
with col_map:
    st.subheader("📍 Mapa de Ruta")
    
    # Crear mapa centrado en la ciudad seleccionada
    m = folium.Map(location=city_data['coords'], zoom_start=10)
    
    # Añadir marcador de la ciudad actual
    folium.Marker(
        city_data['coords'],
        popup=selected_city_name,
        tooltip="Estás aquí",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # Dibujar la línea de la ruta completa
    route_coords = [data['coords'] for data in trip_data.values()]
    folium.PolyLine(
        route_coords,
        color="blue",
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    # Añadir puntos pequeños para el resto de ciudades
    for name, data in trip_data.items():
        if name != selected_city_name:
            folium.CircleMarker(
                location=data['coords'],
                radius=5,
                color="blue",
                fill=True,
                fill_color="blue",
                popup=name
            ).add_to(m)

    st_folium(m, width="100%", height=500)

# --- BOTÓN EXPORTAR ---
st.divider()
st.download_button(
    label="📥 Descargar Itinerario en Excel",
    data="Fecha,Ciudad,Hotel,Costo\n2026-06-01,Napoles,Bueno Hotel,120",
    file_name="eurotrip_2026.csv",
    mime="text/csv",
)
