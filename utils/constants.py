"""
Constantes del juego
"""

# Colores del tema - Paleta más amigable y moderna
COLORS = {
    'bg_main': '#0f172a',           # Azul oscuro profundo
    'bg_secondary': '#1e293b',      # Azul grisáceo
    'bg_card': '#334155',           # Gris azulado
    'accent_primary': '#3b82f6',    # Azul brillante
    'accent_secondary': '#8b5cf6',  # Púrpura
    'accent_gold': '#fbbf24',       # Dorado
    'text_primary': '#f1f5f9',      # Blanco suave
    'text_secondary': '#94a3b8',    # Gris claro
    'red_card': '#ef4444',          # Rojo para cartas
    'green_highlight': '#10b981',   # Verde para resaltado
    'green_dark': '#059669',        # Verde oscuro
    'card_back': '#6366f1',         # Índigo para reverso
    'card_back_accent': '#a78bfa',  # Púrpura claro
    'hand_bg': '#1e293b'            # Fondo para carta en mano
}

# Posiciones de las pilas en el canvas (x, y)
# Organizadas en un diseño más compacto y balanceado
# Calculadas para que todas las pilas con 4 cartas apiladas quepan completamente
PILE_POSITIONS = [
    (120, 150),   # 0 - esquina superior izquierda
    (270, 150),   # 1 - superior
    (420, 150),   # 2 - superior
    (570, 150),   # 3 - esquina superior derecha
    (570, 320),   # 4 - derecha
    (570, 490),   # 5 - derecha
    (570, 660),   # 6 - esquina inferior derecha (ajustado)
    (420, 660),   # 7 - inferior (ajustado)
    (270, 660),   # 8 - inferior (ajustado)
    (120, 660),   # 9 - esquina inferior izquierda (ajustado)
    (120, 490),   # 10 - izquierda
    (120, 320),   # 11 - izquierda
    (345, 405)    # 12 - centro
]

# Dimensiones de las cartas y ventana
CARD_WIDTH = 70
CARD_HEIGHT = 100
WINDOW_WIDTH = 1400  # Aumentado para incluir panel de carta en mano
WINDOW_HEIGHT = 900  # Suficiente para todas las cartas
GAME_AREA_WIDTH = 700  # Área del juego (izquierda)
HAND_AREA_WIDTH = 700  # Área de la carta en mano (derecha)

# Offset vertical entre cartas en una pila
CARD_OFFSET_FACE_UP = 12  # Separación para cartas boca arriba
CARD_OFFSET_FACE_DOWN = 2  # Separación para cartas boca abajo

# Tiempos de animación en milisegundos
ANIMATION_TIMES = {
    'shuffle_wait': 3000,       # Tiempo de animación de mezcla
    'shuffle_iterations': 20,   # Número de iteraciones de mezcla visual
    'shuffle_interval': 100,    # Intervalo entre iteraciones de mezcla
    'flip_delay': 400,          # Tiempo antes de voltear carta
    'auto_play_delay': 500,     # Tiempo entre movimientos automáticos
    'place_card_delay': 300     # Tiempo al colocar carta
}